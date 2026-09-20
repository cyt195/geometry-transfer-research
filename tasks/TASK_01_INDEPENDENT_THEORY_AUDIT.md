# Task 01: Independent theorem and proof audit

## Goal

Re-derive the paired transfer theorem independently. The existing prose is a claim under audit, not an instruction to reproduce its conclusion.

## Required checks

1. Derive the action-gradient of the quadratic Taylor remainder.
2. Recover the `1/2` factor from the Hessian-Lipschitz integral and the `1/3` factor from the action-segment integral.
3. Verify the resulting `1/6` constant and the coefficient/sign of `<s0,s1>`.
4. State the minimal convex-region requirement and whether the proof needs convexity of `f`.
5. Audit candidate-1-minus-candidate-0 signs for objective differences and for any gain convention.
6. State a correct conditional formulation when the training state and actions are stochastic.
7. Test tightness in one dimension and search for missing assumptions.

Use [the proof checklist](../theory/PROOF_AUDIT_CHECKLIST.md), but write the derivation without copying the existing proof.

## Deliverable

A short audit note containing assumptions, a line-by-line derivation, edge cases, any counterexample, and one of: `SUPPORTED_AS_STATED`, `SUPPORTED_WITH_REVISIONS`, or `COUNTEREXAMPLE_FOUND`.

If a counterexample is found, preserve the smallest exact case and do not modify the claim merely to obtain a passing check. A numerical search is not itself a proof.
