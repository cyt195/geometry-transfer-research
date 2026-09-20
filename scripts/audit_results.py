"""Audit a future authoritative Gate-3 state table without redefining metrics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any
import warnings

import pandas as pd


EXPECTED_COLUMNS = (
    "seed",
    "checkpoint",
    "resolved",
    "math_valid",
    "predictor_family",
    "q_model_formal",
    "q_cont",
    "q_grid",
    "q_hvp",
    "q_real",
    "p_model_formal",
    "p_real",
    "reversal_formal",
    "source_file",
    "source_key",
)
PROVENANCE_COLUMNS = ("source_file", "source_key")
FORMAL_REVERSAL_WARNING = (
    "Do not reconstruct reversal_formal from q_cont, q_real, or manuscript prose. "
    "Its historical formal definition must be recovered from authoritative artifacts."
)


class AuditError(ValueError):
    """Raised when a table fails a hard audit check."""


def _counts(series: pd.Series) -> dict[str, int]:
    rendered = series.astype("string").fillna("<MISSING>")
    counts = rendered.value_counts(dropna=False).sort_index()
    return {str(key): int(value) for key, value in counts.items()}


def audit_dataframe(frame: pd.DataFrame) -> dict[str, Any]:
    """Validate schema, uniqueness, and provenance, then return simple counts.

    This function deliberately treats ``reversal_formal`` as an opaque supplied
    field. No value is derived from model or realized quantities.
    """

    warnings.warn(FORMAL_REVERSAL_WARNING, UserWarning, stacklevel=2)
    missing = [column for column in EXPECTED_COLUMNS if column not in frame.columns]
    if missing:
        raise AuditError(f"missing required columns: {missing}")

    duplicate_mask = frame.duplicated(subset=["seed", "checkpoint"], keep=False)
    if duplicate_mask.any():
        duplicate_rows = (
            frame.loc[duplicate_mask, ["seed", "checkpoint"]]
            .sort_values(["seed", "checkpoint"])
            .to_dict(orient="records")
        )
        raise AuditError(f"duplicate seed/checkpoint rows: {duplicate_rows}")

    for column in PROVENANCE_COLUMNS:
        values = frame[column].astype("string")
        missing_provenance = values.isna() | values.str.strip().eq("")
        if missing_provenance.any():
            indices = frame.index[missing_provenance].tolist()
            raise AuditError(f"missing {column} provenance at row indices {indices}")

    return {
        "rows": int(len(frame)),
        "unique_seeds": int(frame["seed"].nunique(dropna=False)),
        "checkpoints": _counts(frame["checkpoint"]),
        "resolved": _counts(frame["resolved"]),
        "math_valid": _counts(frame["math_valid"]),
        "predictor_family": _counts(frame["predictor_family"]),
        "reversal_formal_as_supplied": _counts(frame["reversal_formal"]),
    }


def audit_csv(path: str | Path) -> dict[str, Any]:
    input_path = Path(path)
    if not input_path.is_file():
        raise AuditError(f"input CSV does not exist: {input_path}")
    return audit_dataframe(pd.read_csv(input_path))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", help="Authoritative state-table CSV (read-only input)")
    parser.add_argument(
        "--output",
        help="Optional new JSON path. Existing files are never overwritten.",
    )
    args = parser.parse_args()

    print(f"WARNING: {FORMAL_REVERSAL_WARNING}", file=sys.stderr)
    try:
        summary = audit_csv(args.csv)
        rendered = json.dumps(summary, indent=2, sort_keys=True) + "\n"
        if args.output:
            output = Path(args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            try:
                with output.open("x", encoding="utf-8") as handle:
                    handle.write(rendered)
            except FileExistsError as error:
                raise AuditError(f"refusing to overwrite existing output: {output}") from error
        print(rendered, end="")
    except (AuditError, pd.errors.ParserError) as error:
        print(f"AUDIT FAILED: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
