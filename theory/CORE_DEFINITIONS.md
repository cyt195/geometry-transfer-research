# Core definitions

## Frozen stochastic-quadratic valuation

Let `h` be the relevant gradient-like vector, `K` a curvature-like matrix, `Omega` a stochastic covariance term, and `P` a frozen symmetric positive-definite preconditioner. Define

```text
A_P = h^T P h,
B_P = h^T P K P h + tr(K P Omega P),
G_P(eta) = eta A_P - (eta^2/2) B_P.
```

When `B_P > 0`, maximizing over unconstrained scalar `eta` gives

```text
eta*(P) = A_P / B_P,
V_P^cont = A_P^2 / (2 B_P).
```

The implementation rejects `B_P <= 0`; it does not clip or reinterpret it.

For `c > 0`, `A_(cP)=c A_P` and `B_(cP)=c^2 B_P`, hence

```text
V_(cP)^cont = V_P^cont.
```

This intrinsic scale invariance concerns the optimized continuous valuation. It does not by itself say that two finite actions are equal or equally reliable.

## Frozen finite actions

At a shared base point `w`, let `s0` and `s1` be the two actions being compared. They are frozen before the relative-transfer calculation. Define the local quadratic objective model

```text
Q(s) = f(w) + grad f(w)^T s + 1/2 s^T H(w) s
```

and its Taylor remainder

```text
rho(s) = f(w+s) - Q(s).
```

All candidate differences in this repository have the orientation **candidate 1 minus candidate 0**:

```text
Delta_Q    = Q(s1) - Q(s0),
Delta_real = f(w+s1) - f(w+s0).
```

Therefore

```text
Delta_real - Delta_Q = rho(s1) - rho(s0).
```

This is an objective-difference convention. If another component works with *gains* defined as objective decrease, both differences change sign. Mixing the two conventions invalidates ranking statements.

## Paired radius

Given a nonnegative Hessian-Lipschitz constant `M`, define

```text
Xi_01 = M/6
        * (||s0||^2 + <s0,s1> + ||s1||^2)
        * ||s1-s0||.
```

The quantity is symmetric under swapping candidates and is nonnegative. It is zero for identical actions. Its important feature is the explicit action separation `||s1-s0||`; bounding each remainder separately loses that pairing information.

## Transfer labels

- **Certified:** `|Delta_Q| > Xi_01`; the strict signs of `Delta_Q` and `Delta_real` agree under the theorem assumptions.
- **Unresolved:** `|Delta_Q| <= Xi_01`; the theorem does not determine the realized ranking.
- **Observed agreement/disagreement:** a statement about supplied realized outcomes, distinct from certification.
- **Historical reversal:** only whatever the authoritative frozen protocol formally defined. It must not be reconstructed from these definitions.
