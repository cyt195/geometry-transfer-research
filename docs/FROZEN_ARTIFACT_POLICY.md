# Frozen artifact policy

The completed Gate-3 study is historical frozen evidence. This repository does not contain that evidence and is not authorized to modify it. The authoritative M0 audit is handled separately.

## Rules

1. Mount or copy intentionally supplied artifacts read-only whenever possible.
2. Never overwrite an input artifact or write generated files beside it.
3. Seed 0 remains pilot-only.
4. Preserve negative gains, unresolved states, missingness, and invalid states explicitly.
5. Do not redefine a metric after inspecting outcomes.
6. Treat `reversal_formal` as opaque until its formal definition is recovered from authoritative artifacts.
7. Label theorem work developed after Gate-3 as post-Gate3, not preregistered.
8. Treat finite numerical checks as checks, not proofs.
9. Write each analysis to a fresh namespace with provenance.
10. Preserve assumption-respecting counterexamples.

## Provenance minimum

Every derived artifact should identify input filenames or stable keys, content hashes where feasible, code revision, command, seed, and generation time. Do not embed personal local paths.

## Missing action tensors

Candidate-differential diagnostics require the actual frozen actions. If they were not persisted, they cannot be recovered faithfully from aggregate metrics. Do not rerun a changed training or action-selection law and present the outputs as historical actions.

The mandated status for that case is:

```text
NOT_RECOVERABLE_FROM_FROZEN_ARTIFACTS
```
