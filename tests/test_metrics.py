from pathlib import Path

import pandas as pd
import pytest

from scripts.audit_results import (
    AuditError,
    EXPECTED_COLUMNS,
    FORMAL_REVERSAL_WARNING,
    audit_dataframe,
)
from scripts.reproduce_figures import reproduce


def _row(**overrides: object) -> dict[str, object]:
    row: dict[str, object] = {
        "seed": 1,
        "checkpoint": "checkpoint_a",
        "resolved": True,
        "math_valid": True,
        "predictor_family": "declared_family",
        "q_model_formal": 0.2,
        "q_cont": 0.3,
        "q_grid": 0.25,
        "q_hvp": 0.2,
        "q_real": -0.1,
        "p_model_formal": 0.15,
        "p_real": 0.05,
        # Deliberately supplied as an opaque value inconsistent with q columns.
        "reversal_formal": "authoritative_label",
        "source_file": "artifact.json",
        "source_key": "records/1/checkpoint_a",
    }
    row.update(overrides)
    return row


def test_expected_schema_is_complete() -> None:
    assert tuple(_row()) == EXPECTED_COLUMNS


def test_audit_preserves_supplied_reversal_label() -> None:
    frame = pd.DataFrame([_row()])
    with pytest.warns(UserWarning, match="Do not reconstruct reversal_formal"):
        summary = audit_dataframe(frame)
    assert summary["reversal_formal_as_supplied"] == {"authoritative_label": 1}
    assert "q_real" not in summary
    assert "authoritative artifacts" in FORMAL_REVERSAL_WARNING


def test_audit_rejects_duplicates_and_missing_provenance() -> None:
    duplicates = pd.DataFrame([_row(), _row(q_real=99.0)])
    with pytest.warns(UserWarning):
        with pytest.raises(AuditError, match="duplicate seed/checkpoint"):
            audit_dataframe(duplicates)

    missing_provenance = pd.DataFrame([_row(source_key="")])
    with pytest.warns(UserWarning):
        with pytest.raises(AuditError, match="missing source_key"):
            audit_dataframe(missing_provenance)


def test_audit_rejects_missing_column() -> None:
    frame = pd.DataFrame([_row()]).drop(columns=["reversal_formal"])
    with pytest.warns(UserWarning):
        with pytest.raises(AuditError, match="missing required columns"):
            audit_dataframe(frame)


def test_figure_reproduction_uses_new_directory(tmp_path: Path) -> None:
    input_csv = tmp_path / "authoritative.csv"
    pd.DataFrame(
        [
            _row(),
            _row(seed=2, checkpoint="checkpoint_b", resolved=False),
        ]
    ).to_csv(input_csv, index=False)
    output_dir = tmp_path / "new_namespace"
    with pytest.warns(UserWarning):
        outputs = reproduce(input_csv, output_dir)
    assert all(path.is_file() for path in outputs)
    with pytest.raises(FileExistsError, match="refusing to reuse"):
        reproduce(input_csv, output_dir)
