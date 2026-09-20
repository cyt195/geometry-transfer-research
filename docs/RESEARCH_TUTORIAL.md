# Research tutorial

## Why two stages?

Intrinsic valuation and finite-step transfer answer different questions. The intrinsic objective optimizes a scalar step size inside a stochastic quadratic model. Its value can be unchanged by rescaling `P`, even though a downstream grid, clipping rule, trust region, or discrete action generator selects a different finite step.

Once two actions are fixed, the transfer question is relative: does the local quadratic model rank those two actions correctly? Bounding `|rho(s0)|` and `|rho(s1)|` separately is valid but can be wasteful when the actions share a large common component. The paired theorem follows the remainder *between* the actions and exposes `||s1-s0||`.

## A diagnostic example

Let `s0=a` and `s1=a+epsilon u`. A separate absolute cubic-radius bound scales roughly like `M||a||^3`, even as `epsilon` tends to zero. The paired radius scales roughly like `M||a||^2 |epsilon|`. This is the scientifically distinctive candidate-differential effect.

The paired radius can still be large if the shared action is large; closeness alone is not a universal guarantee. Both the common magnitude and the separation matter.

## What certification says

With objective differences oriented candidate 1 minus candidate 0:

- negative means candidate 1 has a lower objective;
- positive means candidate 0 has a lower objective;
- `|Delta_Q|>Xi_01` certifies that the realized difference has the same sign;
- failure of that inequality is only unresolved.

Certification is sufficient, not necessary. A model may rank correctly without being certified.

## Research workflow

1. Freeze the training state, candidate-generation rule, and actions.
2. Record the model and realized sign conventions.
3. Justify or estimate `M` without outcome-driven redefinition.
4. Compute the paired geometry and model margin.
5. Preserve every state, including negative gains and unresolved certificates.
6. Separate exploratory diagnostics from later confirmatory protocols.

The historical Gate-3 study predates this theorem work. Do not retroactively describe the theorem as preregistered.
