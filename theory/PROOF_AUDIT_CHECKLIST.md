# Independent proof-audit checklist

Record conclusions and counterexamples without editing the theorem to match desired outcomes.

## Definitions and signs

- [ ] Confirm that both `Delta_Q` and `Delta_real` use candidate 1 minus candidate 0.
- [ ] Verify `Delta_real-Delta_Q = rho(s1)-rho(s0)` algebraically.
- [ ] Check whether any downstream code uses gain (objective decrease) rather than objective difference.
- [ ] Keep historical `reversal_formal` separate from newly defined transfer labels.

## Regularity and region

- [ ] State the differentiability assumptions needed for both fundamental-theorem steps.
- [ ] Verify the Hessian-Lipschitz norm is the Euclidean induced operator norm.
- [ ] Confirm that `conv{w,w+s0,w+s1}` contains every `w+tau gamma(t)` used in the proof.
- [ ] Do not accidentally assume convexity of `f`; only the domain region needs to be convex.
- [ ] For constrained domains, verify that all relevant line segments remain inside the domain.

## Constants and geometry

- [ ] Re-derive `||grad R(s)|| <= (M/2)||s||^2`.
- [ ] Integrate `||(1-t)s0+t s1||^2` and recover the `1/3` factor.
- [ ] Confirm the combined constant is `1/6`.
- [ ] Recover the cross term `+<s0,s1>` with coefficient one.
- [ ] Check identical, opposite, orthogonal, collinear, and one-zero actions.
- [ ] Examine the one-dimensional equality case before asserting a sharper constant.

## Stochastic interpretation

- [ ] Identify the conditioning sigma-algebra under which actions and local quantities are frozen.
- [ ] State whether `M` is deterministic, almost-sure, estimated, or high-probability.
- [ ] Audit dependence between action selection, model fitting, and realized evaluation.
- [ ] Keep finite-sample confidence statements separate from the deterministic theorem.

## Evidence language

- [ ] Call a complete derivation a proof only after independent audit.
- [ ] Call finite computation a numerical check or falsification attempt, never a proof.
- [ ] Label post-Gate3 theory or analysis as post-hoc unless a later protocol establishes a new confirmatory stage.
- [ ] Preserve the smallest reproducible counterexample if any assumption-respecting failure is found.
