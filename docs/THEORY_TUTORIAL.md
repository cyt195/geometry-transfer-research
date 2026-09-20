# Theory tutorial

## From absolute to paired control

The standard third-order remainder bound gives `|rho(s)| <= M||s||^3/6`. Applying it twice yields

```text
|rho(s1)-rho(s0)| <= M/6 (||s1||^3 + ||s0||^3).
```

That bound ignores the relationship between the actions. The paired proof instead differentiates the remainder with respect to the action and integrates along the segment from `s0` to `s1`.

The two integrations have distinct roles:

1. integrating the Hessian difference from `w` to `w+s` gives `M/2 ||s||^2`;
2. integrating the squared norm along the action segment gives the quadratic expression divided by three.

Together they yield `M/6`, the cross term, and the separation factor.

## Geometry checks

- `s1=s0`: exact zero paired radius and exact zero remainder difference.
- `s0=0`: the paired radius reduces to the usual `M||s1||^3/6` bound.
- `s1=-s0`: the quadratic factor becomes `||s0||^2`, while separation becomes `2||s0||`.
- `s0` orthogonal to `s1`: the cross term vanishes.
- near-collinear same-direction actions: scalar cubic examples approach or attain equality.

## Norm choice

The proof is written for Euclidean vector norms and their induced matrix operator norm. Substituting Frobenius norms or coordinatewise constants changes the argument and possibly the coefficient. Such variants require a separate statement and audit.

## Random actions

Calling actions frozen is a conditioning statement, not a magic independence assumption. Document what information generated the actions and what randomness remains. If `M` is estimated, distinguish a deterministic upper bound from an empirical estimate that can fail.

For the complete derivation, see [PAIRED_TRANSFER_THEOREM.md](../theory/PAIRED_TRANSFER_THEOREM.md).
