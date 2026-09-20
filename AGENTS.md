# Guidance for AI agents

The scientific objective is to study relative finite-step ranking transfer between two frozen optimization geometries, with special attention to the candidate-differential paired radius.

- This is a sanitized collaboration layer, not the authoritative manuscript or Gate-3 evidence repository.
- Never overwrite or reinterpret frozen evidence. Seed 0 is pilot-only. Never silently clip negative gains, remove unresolved states, reconstruct `reversal_formal`, or alter metrics to improve outcomes.
- Preserve counterexamples and negative results. If a theorem appears false, save the smallest reproducible case and document the ambiguity.
- Label theorem, numerical check, post-hoc analysis, and confirmatory analysis accurately. Tests do not prove a theorem, and post-Gate3 work is not preregistered.
- Write generated results into a new namespaced directory. Do not commit raw frozen/private data, identity details, absolute local paths, or unsupported empirical claims.
- Keep candidate differences consistently oriented as candidate 1 minus candidate 0.
- Before a pull request, run `pytest -q`, `python scripts/smoke_test.py`, and `python scripts/anonymity_scan.py .`.
