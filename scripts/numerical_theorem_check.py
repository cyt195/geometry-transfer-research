"""Deterministically attack, but do not claim to prove, the paired bound."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
import sys

try:
    from scripts.theorem_stress import (
        DEFAULT_DIMENSIONS,
        format_summary,
        run_stress,
        save_violation,
        underestimated_m_diagnostic,
    )
except ModuleNotFoundError:
    from theorem_stress import (
        DEFAULT_DIMENSIONS,
        format_summary,
        run_stress,
        save_violation,
        underestimated_m_diagnostic,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=int, default=50_000)
    parser.add_argument("--seed", type=int, default=2027)
    parser.add_argument(
        "--dimensions", type=int, nargs="+", default=list(DEFAULT_DIMENSIONS)
    )
    parser.add_argument("--failure-root", default="results/theorem_stress")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = run_stress(
        cases=args.cases, seed=args.seed, dimensions=tuple(args.dimensions)
    )
    print("KNOWN-M NUMERICAL CHECK (finite testing; not a proof)")
    print(format_summary(summary))
    if summary.violation is not None:
        path = save_violation(
            summary.violation, seed=args.seed, root=args.failure_root
        )
        print(json.dumps(asdict(summary.violation), indent=2))
        print(f"Saved exact under-assumption violation: {path}", file=sys.stderr)
        return 1

    diagnostic = underestimated_m_diagnostic()
    print("OUT-OF-ASSUMPTION DIAGNOSTIC (M deliberately underestimated)")
    print(
        f"expected_failure={not diagnostic.passed} "
        f"error={diagnostic.absolute_error:.12g} "
        f"radius={diagnostic.paired_radius:.12g} M_used={diagnostic.M:.12g}"
    )
    if diagnostic.passed:
        print("The constructed out-of-assumption diagnostic did not fail.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
