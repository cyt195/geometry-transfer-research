# Task 02: Numerical theorem stress test

**Recommended first task.** It is independent of frozen Gate-3 evidence.

## Goal

Attempt to falsify the paired bound on the analytic known-`M` cubic family and probe numerical stability near special geometries.

## Protocol

Run at least 50,000 deterministic seeded cases across several dimensions. Include:

- ordinary random pairs;
- `s1=s0+epsilon u` over several orders of magnitude;
- identical and opposite actions;
- large common components with tiny disagreement;
- orthogonal and near-collinear actions;
- one action near zero;
- positive and negative cubic coefficients.

Start with:

```bash
python scripts/numerical_theorem_check.py --cases 50000 --seed 2027
python scripts/counterexample_search.py --cases 50000 --seed 2027
```

Add independent cases rather than relying only on the bundled generator. Report near-tight cases by error-to-radius ratio, including the exact seed and vectors. Separate mathematical violations from floating-point cancellation and from deliberately underestimated-`M` cases.

## Acceptance criteria

- Any valid under-assumption violation exits nonzero and is preserved exactly.
- Special geometry coverage is explicit.
- At least one known tight or near-tight scalar case is reported.
- Tolerances are justified before outcome-driven changes.
- The report says “finite numerical check,” not “proof.”

Write outputs to a new `results/theorem_stress/<run-id>/` namespace. Do not overwrite an earlier run.
