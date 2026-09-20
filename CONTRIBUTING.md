# Contributing

## Scientific conduct

- Preserve negative, null, unresolved, and counterexample results.
- Never change a metric, filter, tolerance, seed rule, or label to improve an outcome.
- Distinguish theorem, numerical check, synthetic calibration, post-hoc analysis, and confirmatory analysis.
- Do not infer the historical definition of `reversal_formal` from manuscript prose or from other columns.
- Do not call post-Gate3 work preregistered.
- Do not describe finite numerical testing as proof.

## Data and outputs

Frozen Gate-3 artifacts are read-only and are not committed here. New scripts must write to a new namespaced directory, refuse accidental overwrites, and retain provenance. If required action tensors are absent, report the specified non-recoverability state rather than reconstructing them under a different law.

Do not commit identity information, local absolute paths, secrets, submission PDFs, private data, raw frozen evidence, or current empirical headline results.

## Code changes

Use Python 3.10+ and keep dependencies minimal. Add deterministic tests for mathematical behavior and failure paths. A genuine under-assumption theorem violation must remain visible and reproducible.

Before submitting a pull request, run:

```bash
pytest -q
python scripts/smoke_test.py
python scripts/anonymity_scan.py .
```

Summarize exact commands and results without overstating what they establish.
