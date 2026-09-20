# Collaborator onboarding

This is the quickest route from a clean checkout to an independent contribution.

## First hour

1. Read the repository [README](../README.md) and [project overview](../PROJECT_OVERVIEW.md).
2. Read the [paired theorem](../theory/PAIRED_TRANSFER_THEOREM.md) with the [proof-audit checklist](../theory/PROOF_AUDIT_CHECKLIST.md) beside it.
3. Install the four dependencies and run:

   ```bash
   pytest -q
   python scripts/smoke_test.py
   ```

4. Inspect `scripts/math_utils.py` and `scripts/theorem_stress.py`. Verify that code, tests, and prose use the same candidate-1-minus-candidate-0 convention.

Expected outcome: the tests and known-`M` smoke checks pass; the deliberately underestimated-`M` example fails its bound and is labelled out of assumption.

## First independent task

Start with [TASK 02: Numerical theorem stress test](../tasks/TASK_02_NUMERICAL_STRESS_TEST.md). It requires no private artifacts, has a deterministic acceptance criterion, and can falsify the current theorem implementation. Do not tune tolerances or distributions after seeing failures without recording the original result.

## What not to assume

- This repository is not the authoritative manuscript repository.
- It contains no authoritative Gate-3 conclusions or raw evidence.
- Seed 0, if encountered later, is pilot-only.
- `reversal_formal` is an opaque historical field until its definition is recovered from authoritative artifacts.
- An unresolved transfer certificate is not automatically an observed reversal.
- Passing 50,000 or 50 million checks does not prove a theorem.

## Useful contribution shape

A strong pull request is small enough to audit and includes:

- the precise question;
- assumptions and sign conventions;
- deterministic code and tests;
- exact commands and seeds;
- a new output namespace for generated results;
- an honest result label, including negative or unresolved outcomes.

Before review, follow [CONTRIBUTING.md](../CONTRIBUTING.md) and run the anonymity scan.
