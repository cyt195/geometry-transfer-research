"""Search for an under-assumption counterexample without suppressing failures."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json

try:
    from scripts.theorem_stress import format_summary, run_stress, save_violation
except ModuleNotFoundError:
    from theorem_stress import format_summary, run_stress, save_violation


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=int, default=50_000)
    parser.add_argument("--seed", type=int, default=2027)
    parser.add_argument("--failure-root", default="results/theorem_stress")
    args = parser.parse_args()

    summary = run_stress(cases=args.cases, seed=args.seed)
    print("COUNTEREXAMPLE SEARCH (finite falsification attempt; not a proof)")
    print(format_summary(summary))
    if summary.violation is None:
        print("No under-assumption violation found in the finite search.")
        return 0

    path = save_violation(summary.violation, seed=args.seed, root=args.failure_root)
    print(json.dumps(asdict(summary.violation), indent=2))
    print(f"Counterexample preserved at {path}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
