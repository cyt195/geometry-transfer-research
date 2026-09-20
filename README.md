# Relative finite-step transfer of frozen optimization geometries

This repository is the sanitized collaboration, audit, reproducibility, theorem-stress-test, and onboarding layer for an ICLR 2027 research project. It is **not** the authoritative manuscript repository and does not contain the frozen Gate-3 evidence.

The project separates two questions that must not be conflated:

1. **Intrinsic valuation:** how valuable is a frozen SPD preconditioner under a stochastic quadratic model?
2. **Finite-step transfer:** does a local quadratic model rank two particular frozen actions in the same order as the realized objective?

For candidate actions `s0` and `s1`, all differences use the orientation candidate 1 minus candidate 0. With `rho(s) = f(w+s) - Q(s)`,

```text
Delta_real - Delta_Q = rho(s1) - rho(s0).
```

If the Hessian is `M`-Lipschitz on the relevant convex region, the paired radius is

```text
Xi_01 = M/6 * (||s0||^2 + <s0,s1> + ||s1||^2) * ||s1-s0||.
```

Thus `|Delta_Q| > Xi_01` is a sufficient condition for strict ranking transfer. Passing numerical checks is evidence about an implementation, not a mathematical proof.

## Start here

New collaborators should read, in order:

1. [GETTING_STARTED.md](GETTING_STARTED.md)
2. [docs/ZHOU_ONBOARDING.md](docs/ZHOU_ONBOARDING.md)
3. [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
4. [theory/PAIRED_TRANSFER_THEOREM.md](theory/PAIRED_TRANSFER_THEOREM.md)

Then run:

```bash
python -m venv .venv
python -m pip install -r requirements.txt
pytest -q
python scripts/smoke_test.py
```

The recommended first independent contribution is [TASK 02: numerical theorem stress test](tasks/TASK_02_NUMERICAL_STRESS_TEST.md).

## Repository map

- `docs/`: research tutorials, experiment guidance, AI-use guidance, and frozen-artifact policy.
- `theory/`: definitions, theorem statement and derivation, and a proof-audit checklist.
- `scripts/`: mathematical utilities, deterministic theorem attacks, auditing, reproduction, and sanitization checks.
- `tests/`: unit and randomized regression tests.
- `tasks/`: four bounded independent collaborator tasks.
- `figures/`: conceptual TikZ source only; no empirical headline values.

## Scientific boundaries

- The distinctive object is the **candidate-differential** geometry in `Xi_01`, not the generic observation that local quadratics can fail at finite steps.
- Seed 0 is pilot-only in any future study that adopts that convention.
- Negative gains and unresolved states are preserved.
- Historical metrics, including `reversal_formal`, are never reconstructed or redefined from manuscript prose.
- New analyses write to new namespaces; frozen evidence is read-only.

See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.
