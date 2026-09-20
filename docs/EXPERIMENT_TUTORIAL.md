# Experiment tutorial

## Synthetic known-`M` calibration

The included cubic family has a global, analytic Hessian-Lipschitz constant. It is useful for checking constants, signs, action geometries, and program behavior without estimating `M` from samples.

Run the quick suite:

```bash
python scripts/smoke_test.py
```

Run the deeper deterministic attack:

```bash
python scripts/numerical_theorem_check.py --cases 50000 --seed 2027
```

The harness cycles through ordinary random pairs, tiny separations, identical actions, opposite actions, large shared components, orthogonal actions, near-collinear actions, and one action near zero across several dimensions. It reports the largest observed error-to-radius ratio.

If an under-assumption violation occurs, the command exits nonzero and writes the exact seed, matrix, coefficient, base point, actions, radius, and tolerance to a fresh directory. Keep that artifact. Do not adjust the test merely to make it pass.

## Out-of-assumption diagnostic

The scripts also evaluate a fixed scalar cubic with a deliberately underestimated `M`. The failure demonstrates only that a false bound on curvature variation can invalidate the certificate. It is not a counterexample to the theorem.

## Future frozen-state analysis

Do not start action-level transfer diagnostics until authoritative read-only artifacts are supplied. Validate schema and provenance first:

```bash
python scripts/audit_results.py path/to/state_table.csv
```

If action tensors were not persisted, use the exact non-recoverability marker specified in [TASK 03](../tasks/TASK_03_TRANSFER_DIAGNOSTICS.md). Never regenerate purported historical actions under a new experimental law.

## Reproducible figures

For a supplied authoritative CSV, write figures to a new directory:

```bash
python scripts/reproduce_figures.py \
  --input path/to/state_table.csv \
  --output-dir results/figure_reproduction/run_001
```

The utility validates the state table, hashes the input, stores only the input filename (not a local absolute path), and refuses to overwrite an existing result directory.
