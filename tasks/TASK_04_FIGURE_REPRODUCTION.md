# Task 04: Independent figure reproduction and provenance audit

## Goal

Reproduce each eligible collaboration figure from an authoritative supplied table and audit the chain from source keys to plotted marks.

## Procedure

1. Run `scripts/audit_results.py` on the input table.
2. Record the content hash, code revision, command, environment, and output namespace.
3. Run `scripts/reproduce_figures.py` into a new directory.
4. Independently recompute simple row counts and spot-check plotted coordinates.
5. Confirm that unresolved and negative values remain present.
6. Confirm that no current headline values are hard-coded in source.
7. Run the anonymity scan on all intended committed outputs.

## Deliverable

A reproduction note, exact commands, provenance manifest, generated figures, and a discrepancy table. Label values copied from a manuscript as transcribed rather than independently reproduced. Do not revise source metrics in response to discrepancies.
