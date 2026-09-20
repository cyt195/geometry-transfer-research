"""Fast deterministic smoke test for the collaboration workspace."""

from __future__ import annotations

import sys

try:
    from scripts.theorem_stress import (
        format_summary,
        run_stress,
        save_violation,
        underestimated_m_diagnostic,
    )
except ModuleNotFoundError:
    from theorem_stress import (
        format_summary,
        run_stress,
        save_violation,
        underestimated_m_diagnostic,
    )


SMOKE_CASES = 2_000
SMOKE_SEED = 1729


def main() -> int:
    print("SMOKE TEST: known-M finite numerical checks; not a theorem proof")
    summary = run_stress(cases=SMOKE_CASES, seed=SMOKE_SEED)
    print(format_summary(summary))
    if summary.violation is not None:
        path = save_violation(summary.violation, seed=SMOKE_SEED)
        print(f"Under-assumption violation saved to {path}", file=sys.stderr)
        return 1

    diagnostic = underestimated_m_diagnostic()
    if diagnostic.passed:
        print("Expected underestimated-M diagnostic failure was absent.", file=sys.stderr)
        return 2
    print(
        "OUT-OF-ASSUMPTION diagnostic behaved as expected: "
        f"error={diagnostic.absolute_error:.6g} > radius={diagnostic.paired_radius:.6g}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
