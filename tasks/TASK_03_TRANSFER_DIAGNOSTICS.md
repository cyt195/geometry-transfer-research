# Task 03: Frozen transfer diagnostics

## Start condition

Begin only after authoritative action-level frozen artifacts are intentionally supplied read-only. Do not use manuscript prose or aggregate tables to recreate missing actions.

## Goal

For each eligible frozen state, compare:

1. observed differential transfer error `|Delta_real-Delta_Q|`;
2. the paired action-geometry proxy
   `(||s0||^2 + <s0,s1> + ||s1||^2)||s1-s0||`;
3. the separate absolute cubic-radius proxy `||s0||^3+||s1||^3`.

Retain negative gains, unresolved states, invalid states, seed 0 pilot status, and provenance. Do not infer `reversal_formal`.

## Non-recoverability rule

If the frozen artifacts do not contain the required action tensors, the result must be exactly:

```text
NOT_RECOVERABLE_FROM_FROZEN_ARTIFACTS
```

Do not reconstruct the actions by rerunning a different experimental or stochastic law.

## Deliverable

A provenance-audited table and diagnostic figures in a new namespace, plus a methods note separating declared-before-analysis checks from post-hoc exploration. No source artifact may be modified.
