"""Reproduce provenance-labelled diagnostics from a supplied authoritative CSV."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
    from scripts.audit_results import audit_dataframe
except ModuleNotFoundError:
    from audit_results import audit_dataframe


def _truthy(series: pd.Series) -> pd.Series:
    return series.astype("string").str.strip().str.lower().isin({"true", "1", "yes"})


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def reproduce(input_csv: Path, output_dir: Path) -> tuple[Path, Path, Path]:
    """Create figures in a new directory; never overwrite prior results."""

    if output_dir.exists():
        raise FileExistsError(f"refusing to reuse existing output directory: {output_dir}")
    frame = pd.read_csv(input_csv)
    summary = audit_dataframe(frame)
    output_dir.mkdir(parents=True, exist_ok=False)

    checkpoint_order = list(dict.fromkeys(frame["checkpoint"].astype(str)))
    grouped = frame.assign(
        _resolved=_truthy(frame["resolved"]),
        _math_valid=_truthy(frame["math_valid"]),
    ).groupby(frame["checkpoint"].astype(str), sort=False)
    totals = grouped.size().reindex(checkpoint_order, fill_value=0)
    resolved = grouped["_resolved"].sum().reindex(checkpoint_order, fill_value=0)
    valid = grouped["_math_valid"].sum().reindex(checkpoint_order, fill_value=0)

    figure, axes = plt.subplots(1, 2, figsize=(11, 4.2), constrained_layout=True)
    positions = np.arange(len(checkpoint_order))
    width = 0.26
    axes[0].bar(positions - width, totals, width, label="all rows")
    axes[0].bar(positions, resolved, width, label="resolved")
    axes[0].bar(positions + width, valid, width, label="math-valid")
    axes[0].set_xticks(positions, checkpoint_order, rotation=30, ha="right")
    axes[0].set_ylabel("row count")
    axes[0].set_title("State-table coverage")
    axes[0].legend(frameon=False)

    plotted = False
    for prefix, color in (("q", "tab:blue"), ("p", "tab:orange")):
        model_values = pd.to_numeric(frame[f"{prefix}_model_formal"], errors="coerce")
        real_values = pd.to_numeric(frame[f"{prefix}_real"], errors="coerce")
        mask = model_values.notna() & real_values.notna()
        if mask.any():
            axes[1].scatter(
                model_values[mask],
                real_values[mask],
                alpha=0.7,
                label=prefix.upper(),
                color=color,
            )
            plotted = True
    axes[1].axhline(0.0, color="0.7", linewidth=0.8)
    axes[1].axvline(0.0, color="0.7", linewidth=0.8)
    axes[1].set_xlabel("formal model quantity (as supplied)")
    axes[1].set_ylabel("realized quantity (as supplied)")
    axes[1].set_title("Formal-model versus realized values")
    if plotted:
        axes[1].legend(frameon=False)
    else:
        axes[1].text(
            0.5,
            0.5,
            "No numeric formal/realized pairs",
            ha="center",
            va="center",
            transform=axes[1].transAxes,
        )

    figure_path = output_dir / "gate3_diagnostics.png"
    figure.savefig(figure_path, dpi=180)
    plt.close(figure)

    summary_path = output_dir / "audit_summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    provenance_path = output_dir / "provenance.json"
    provenance = {
        "input_filename": input_csv.name,
        "input_sha256": _file_sha256(input_csv),
        "rows": int(len(frame)),
        "note": "Generated from supplied data; no empirical headline values are encoded in source.",
    }
    provenance_path.write_text(
        json.dumps(provenance, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return figure_path, summary_path, provenance_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    for path in reproduce(args.input, args.output_dir):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
