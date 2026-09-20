# Paired finite-step transfer theorem

## Statement

Let `f: R^d -> R` be twice continuously differentiable on an open set containing the convex hull

```text
D = conv{w, w+s0, w+s1}.
```

Assume its Hessian is `M`-Lipschitz in operator norm on `D`:

```text
||H(x)-H(y)||_op <= M ||x-y||_2    for all x,y in D.
```

Define `Q`, `rho`, `Delta_Q`, and `Delta_real` as in [CORE_DEFINITIONS.md](CORE_DEFINITIONS.md), with every difference oriented as candidate 1 minus candidate 0. Then

```text
|rho(s1)-rho(s0)|
  = |Delta_real-Delta_Q|
  <= M/6
     * (||s0||^2 + <s0,s1> + ||s1||^2)
     * ||s1-s0||.
```

Consequently, `|Delta_Q| > Xi_01` implies `sign(Delta_real)=sign(Delta_Q)` and both are nonzero.

The assumption is convexity of the **region**, not convexity of `f`.

## Derivation

Write the quadratic remainder as a function of the action:

```text
R(s) = f(w+s) - f(w) - grad f(w)^T s - 1/2 s^T H(w) s.
```

Its action-gradient is

```text
grad_s R(s)
  = grad f(w+s) - grad f(w) - H(w)s
  = integral_0^1 [H(w+tau s)-H(w)] s d tau.
```

The Hessian-Lipschitz condition gives

```text
||grad_s R(s)||
  <= integral_0^1 M tau ||s||^2 d tau
  = M/2 ||s||^2.
```

Now set `d=s1-s0` and connect the two actions with `gamma(t)=s0+t d`. The fundamental theorem of calculus and Cauchy-Schwarz yield

```text
|R(s1)-R(s0)|
  = |integral_0^1 <grad R(gamma(t)), d> d t|
  <= M/2 ||d|| integral_0^1 ||gamma(t)||^2 d t.
```

The remaining integral is exact:

```text
integral_0^1 ||(1-t)s0 + t s1||^2 d t
  = 1/3 (||s0||^2 + <s0,s1> + ||s1||^2).
```

Multiplying `M/2` by `1/3` produces the factor `M/6` and the cross term shown in the theorem.

The points used above have the form

```text
w + tau ((1-t)s0 + t s1),    tau,t in [0,1],
```

which lie in `conv{w,w+s0,w+s1}`. This is why the stated convex-region condition is sufficient.

## Ranking consequence

Let `e=Delta_real-Delta_Q`. If `|e|<=Xi_01<|Delta_Q|`, then perturbing `Delta_Q` by `e` cannot cross zero. The conclusion is strict. When `|Delta_Q|=Xi_01`, the realized difference may reach zero, so equality remains unresolved.

## Stochastic conditioning

The displayed theorem is deterministic. In a stochastic pipeline, it may be applied conditionally on a sigma-algebra with respect to which `w`, `s0`, `s1`, the local model, and the claimed `M` are fixed. If action selection reuses randomness or outcome information, that dependence must be stated; it is not removed by calling the actions frozen. A probabilistic guarantee additionally needs justified almost-sure or high-probability assumptions for `M` and the relevant region.

## Known-`M` cubic family

For

```text
f(x) = 1/2 x^T A x + lambda/6 sum_i x_i^3,
```

with symmetric `A`,

```text
H(x) = A + lambda diag(x),
||H(x)-H(y)||_op
  = |lambda| max_i |x_i-y_i|
  <= |lambda| ||x-y||_2.
```

Thus `M=|lambda|` is globally valid. The exact remainder is

```text
rho(s) = lambda/6 sum_i s_i^3.
```

In one dimension with same-direction nonnegative actions, the paired inequality can attain equality. Numerical checks on this family test transcription, implementation, special geometries, and floating-point behavior; they do not replace the proof.
