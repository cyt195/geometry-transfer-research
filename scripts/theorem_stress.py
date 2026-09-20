"""Deterministic case generation and checking for the paired transfer bound."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

try:
    from scripts.math_utils import KnownMCubic, paired_radius
except ModuleNotFoundError:  # Direct execution from the scripts directory.
    from math_utils import KnownMCubic, paired_radius


FloatArray = NDArray[np.float64]
CASE_KINDS = (
    "ordinary",
    "small_separation",
    "identical",
    "opposite",
    "large_common_tiny_disagreement",
    "orthogonal",
    "near_collinear",
    "one_near_zero",
)
DEFAULT_DIMENSIONS = (1, 2, 3, 5, 8, 13)


@dataclass(frozen=True)
class CaseResult:
    index: int
    kind: str
    dimension: int
    lambda_: float
    M: float
    base: list[float]
    s0: list[float]
    s1: list[float]
    A: list[list[float]]
    remainder_difference: float
    absolute_error: float
    paired_radius: float
    ratio: float
    tolerance: float
    passed: bool


@dataclass(frozen=True)
class StressSummary:
    seed: int
    requested_cases: int
    checked_cases: int
    dimensions: tuple[int, ...]
    case_counts: dict[str, int]
    maximum_ratio: float
    maximum_ratio_case: CaseResult | None
    violation: CaseResult | None


def _unit(vector: FloatArray) -> FloatArray:
    norm = float(np.linalg.norm(vector))
    if norm == 0.0:
        result = np.zeros_like(vector)
        result[0] = 1.0
        return result
    return vector / norm


def _orthogonal_unit(rng: np.random.Generator, direction: FloatArray) -> FloatArray:
    if direction.size == 1:
        return np.ones(1)
    candidate = rng.normal(size=direction.size)
    candidate = candidate - float(candidate @ direction) * direction
    if np.linalg.norm(candidate) < 1e-12:
        candidate = np.roll(direction, 1)
        candidate = candidate - float(candidate @ direction) * direction
    return _unit(candidate)


def generate_case(
    rng: np.random.Generator, index: int, dimensions: Iterable[int]
) -> tuple[str, KnownMCubic, FloatArray, FloatArray, FloatArray]:
    """Generate one deterministic case from the supplied RNG state."""

    dimensions_tuple = tuple(int(value) for value in dimensions)
    if not dimensions_tuple or any(value <= 0 for value in dimensions_tuple):
        raise ValueError("dimensions must contain positive integers")
    dimension = dimensions_tuple[index % len(dimensions_tuple)]
    kind = CASE_KINDS[index % len(CASE_KINDS)]

    raw = rng.normal(size=(dimension, dimension))
    matrix = 0.5 * (raw + raw.T)
    lambda_magnitude = float(np.exp(rng.uniform(np.log(0.1), np.log(3.0))))
    lambda_ = lambda_magnitude * (-1.0 if rng.random() < 0.5 else 1.0)
    model = KnownMCubic(matrix, lambda_)
    base = rng.normal(size=dimension)

    scale = float(10.0 ** rng.uniform(-2.0, 2.0))
    if kind == "ordinary":
        s0 = scale * rng.normal(size=dimension)
        s1 = scale * rng.normal(size=dimension)
    elif kind == "small_separation":
        s0 = scale * rng.normal(size=dimension)
        epsilon = scale * float(10.0 ** rng.uniform(-10.0, -3.0))
        s1 = s0 + epsilon * _unit(rng.normal(size=dimension))
    elif kind == "identical":
        s0 = scale * rng.normal(size=dimension)
        s1 = s0.copy()
    elif kind == "opposite":
        s0 = scale * rng.normal(size=dimension)
        s1 = -s0
    elif kind == "large_common_tiny_disagreement":
        common = 100.0 * scale * _unit(rng.normal(size=dimension))
        epsilon = scale * float(10.0 ** rng.uniform(-9.0, -4.0))
        s0 = common
        s1 = common + epsilon * _unit(rng.normal(size=dimension))
    elif kind == "orthogonal":
        direction0 = _unit(rng.normal(size=dimension))
        direction1 = _orthogonal_unit(rng, direction0)
        s0 = scale * direction0
        s1 = 0.7 * scale * direction1
    elif kind == "near_collinear":
        direction = _unit(rng.normal(size=dimension))
        transverse = _orthogonal_unit(rng, direction)
        s0 = scale * direction
        s1 = 1.3 * scale * direction + 1e-7 * scale * transverse
    else:  # one_near_zero
        s0 = 1e-10 * scale * rng.normal(size=dimension)
        s1 = scale * rng.normal(size=dimension)
    return kind, model, base, s0, s1


def evaluate_case(
    index: int,
    kind: str,
    model: KnownMCubic,
    base: FloatArray,
    s0: FloatArray,
    s1: FloatArray,
    *,
    M: float | None = None,
    rtol: float = 5e-12,
    atol: float = 5e-13,
) -> CaseResult:
    """Evaluate one paired-bound case with a scale-aware numerical tolerance."""

    m_value = model.hessian_lipschitz_constant if M is None else float(M)
    # Use a factored difference of cubes. This is algebraically identical to
    # rho(s1)-rho(s0) but avoids subtracting nearly equal large remainders in
    # the large-common-component stress family.
    difference = s1 - s0
    remainder_difference = float(
        (model.lambda_ / 6.0)
        * np.sum(difference * (s1 * s1 + s1 * s0 + s0 * s0))
    )
    absolute_error = abs(remainder_difference)
    radius = paired_radius(s0, s1, m_value)
    tolerance = atol + rtol * max(absolute_error, radius)
    passed = absolute_error <= radius + tolerance
    if radius > 0.0:
        ratio = absolute_error / radius
    elif absolute_error <= tolerance:
        ratio = 0.0
    else:
        ratio = float("inf")
    return CaseResult(
        index=index,
        kind=kind,
        dimension=model.dimension,
        lambda_=model.lambda_,
        M=m_value,
        base=base.tolist(),
        s0=s0.tolist(),
        s1=s1.tolist(),
        A=model.A.tolist(),
        remainder_difference=float(remainder_difference),
        absolute_error=float(absolute_error),
        paired_radius=float(radius),
        ratio=float(ratio),
        tolerance=float(tolerance),
        passed=bool(passed),
    )


def run_stress(
    *,
    cases: int,
    seed: int,
    dimensions: Iterable[int] = DEFAULT_DIMENSIONS,
    stop_on_violation: bool = True,
) -> StressSummary:
    """Run deterministic known-``M`` cases and return the full summary."""

    if cases <= 0:
        raise ValueError("cases must be positive")
    dimensions_tuple = tuple(int(value) for value in dimensions)
    rng = np.random.default_rng(seed)
    counts: Counter[str] = Counter()
    maximum: CaseResult | None = None
    violation: CaseResult | None = None
    checked = 0

    for index in range(cases):
        kind, model, base, s0, s1 = generate_case(rng, index, dimensions_tuple)
        result = evaluate_case(index, kind, model, base, s0, s1)
        checked += 1
        counts[kind] += 1
        if np.isfinite(result.ratio) and (
            maximum is None or result.ratio > maximum.ratio
        ):
            maximum = result
        if not result.passed:
            violation = result
            if stop_on_violation:
                break

    return StressSummary(
        seed=int(seed),
        requested_cases=int(cases),
        checked_cases=checked,
        dimensions=dimensions_tuple,
        case_counts=dict(sorted(counts.items())),
        maximum_ratio=0.0 if maximum is None else maximum.ratio,
        maximum_ratio_case=maximum,
        violation=violation,
    )


def underestimated_m_diagnostic() -> CaseResult:
    """Return an explicit failure caused by violating the declared ``M`` assumption."""

    model = KnownMCubic(np.zeros((1, 1)), 3.0)
    return evaluate_case(
        -1,
        "OUT_OF_ASSUMPTION_underestimated_M",
        model,
        np.zeros(1),
        np.zeros(1),
        np.ones(1),
        M=0.75,
        rtol=0.0,
        atol=0.0,
    )


def save_violation(
    result: CaseResult, *, seed: int, root: str | Path = "results/theorem_stress"
) -> Path:
    """Save an exact violation in a fresh namespace without overwriting."""

    root_path = Path(root)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    candidate = root_path / f"violation_seed_{seed}_case_{result.index}_{stamp}"
    suffix = 1
    while candidate.exists():
        suffix += 1
        candidate = root_path / (
            f"violation_seed_{seed}_case_{result.index}_{stamp}_{suffix:02d}"
        )
    candidate.mkdir(parents=True, exist_ok=False)
    output = candidate / "counterexample.json"
    case_payload = asdict(result)
    if not np.isfinite(result.ratio):
        case_payload["ratio"] = "inf" if result.ratio > 0.0 else "-inf"
    payload = {
        "status": "UNDER_ASSUMPTION_VIOLATION",
        "seed": int(seed),
        "case": case_payload,
        "note": "Preserve and independently audit this case; do not weaken the test.",
    }
    output.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return output


def format_summary(summary: StressSummary) -> str:
    status = "PASS" if summary.violation is None else "VIOLATION"
    return (
        f"status={status} seed={summary.seed} "
        f"checked={summary.checked_cases}/{summary.requested_cases} "
        f"dimensions={list(summary.dimensions)} "
        f"max_ratio={summary.maximum_ratio:.12g} "
        f"case_counts={summary.case_counts}"
    )
