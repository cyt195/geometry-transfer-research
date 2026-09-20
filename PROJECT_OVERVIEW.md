# Project overview

## Research question

Two optimization geometries can each look favorable under an intrinsic stochastic-quadratic valuation and yet induce particular finite actions whose relative ranking is not transferred reliably by the local quadratic model. The project studies when the ranking of two **frozen actions** is certified.

The intended scientific positioning is narrow: quadratic models may be informative, but model accuracy alone does not guarantee reliable relative ranking of two frozen geometries at a particular finite action. The project does not claim first discovery of finite-step model failure, wrong-step phenomena, or curvature-variation effects.

## Pipeline

For each frozen SPD preconditioner `P`, the intrinsic model uses

```text
A_P = h^T P h
B_P = h^T P K P h + tr(K P Omega P)
G_P(eta) = eta A_P - 1/2 eta^2 B_P.
```

When `B_P > 0`, the continuous optimum is `eta*(P) = A_P/B_P` and

```text
V_P^cont = A_P^2 / (2 B_P).
```

This value is invariant under `P -> cP` for `c > 0`. The pipeline then selects finite candidate actions `s0` and `s1`; the selection law must be recorded rather than inferred later.

At a shared training state `w`, define

```text
Q(s) = f(w) + grad f(w)^T s + 1/2 s^T Hessian(f)(w) s
rho(s) = f(w+s) - Q(s)
Delta_Q = Q(s1) - Q(s0)
Delta_real = f(w+s1) - f(w+s0).
```

Then `Delta_real - Delta_Q = rho(s1)-rho(s0)`. Under the stated Hessian-Lipschitz assumptions,

```text
|Delta_real - Delta_Q| <= Xi_01,
Xi_01 = M/6 * (||s0||^2 + <s0,s1> + ||s1||^2) * ||s1-s0||.
```

If `|Delta_Q| > Xi_01`, both differences have the same strict sign. Equality or a smaller model margin is unresolved, not a reversal.

## Evidence layers

- **Theorem:** a mathematical statement supported by a complete audited proof under explicit assumptions.
- **Numerical check:** a finite implementation stress test that can falsify a claim or expose a bug, but cannot prove a universal theorem.
- **Synthetic calibration:** controlled experiments such as the known-`M` cubic family.
- **Confirmatory study:** an analysis declared before viewing the relevant outcomes and executed under a frozen protocol.
- **Post-hoc analysis:** a useful exploratory analysis labelled as such.

The completed Gate-3 study is frozen historical evidence. Its authoritative M0 audit is outside this repository.

## Immediate goals

1. Independently audit the paired theorem and all constants/signs.
2. Attack it numerically across adversarial action geometries.
3. Prepare provenance-safe diagnostics for future read-only artifacts.
4. Make every conceptual and empirical figure reproducible from declared inputs.
