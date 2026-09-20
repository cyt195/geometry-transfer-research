import json
from pathlib import Path

import numpy as np
import pytest

from scripts.math_utils import KnownMCubic, paired_radius, transfer_differences
from scripts.theorem_stress import (
    CASE_KINDS,
    evaluate_case,
    run_stress,
    save_violation,
    underestimated_m_diagnostic,
)


def test_identical_actions_have_zero_radius() -> None:
    action = np.array([1.0, -2.0, 3.0])
    assert paired_radius(action, action, 4.0) == 0.0


def test_paired_radius_is_nonnegative() -> None:
    rng = np.random.default_rng(41)
    for dimension in (1, 2, 5, 11):
        for _ in range(250):
            s0 = rng.normal(size=dimension)
            s1 = rng.normal(size=dimension)
            assert paired_radius(s0, s1, M=2.3) >= 0.0


def test_thousands_of_known_m_cases_satisfy_bound() -> None:
    summary = run_stress(cases=8_192, seed=2027, stop_on_violation=True)
    assert summary.violation is None
    assert summary.checked_cases == 8_192
    assert set(summary.case_counts) == set(CASE_KINDS)
    assert summary.maximum_ratio <= 1.0 + 5e-12


def test_one_dimensional_collinear_case_is_tight() -> None:
    model = KnownMCubic(np.array([[0.4]]), lambda_=2.0)
    base = np.array([-0.3])
    s0 = np.array([0.7])
    s1 = np.array([1.9])
    difference = abs(
        model.quadratic_taylor_remainder(base, s1)
        - model.quadratic_taylor_remainder(base, s0)
    )
    radius = paired_radius(s0, s1, model.hessian_lipschitz_constant)
    assert difference == pytest.approx(radius, rel=2e-15, abs=1e-15)


def test_transfer_differences_use_candidate_one_minus_zero() -> None:
    model = KnownMCubic(np.array([[1.0]]), lambda_=0.6)
    base = np.array([0.2])
    s0 = np.array([-0.1])
    s1 = np.array([0.4])
    delta_q, delta_real, remainder_difference = transfer_differences(
        model, base, s0, s1
    )
    assert delta_q == pytest.approx(
        model.quadratic_model(base, s1) - model.quadratic_model(base, s0)
    )
    assert delta_real == pytest.approx(
        model.value(base + s1) - model.value(base + s0)
    )
    assert delta_real - delta_q == pytest.approx(remainder_difference, abs=1e-14)


def test_underestimated_m_is_explicitly_out_of_assumption() -> None:
    diagnostic = underestimated_m_diagnostic()
    assert diagnostic.kind.startswith("OUT_OF_ASSUMPTION")
    assert not diagnostic.passed
    assert diagnostic.absolute_error > diagnostic.paired_radius


def test_zero_radius_violation_can_be_preserved(tmp_path: Path) -> None:
    model = KnownMCubic(np.zeros((1, 1)), lambda_=1.0)
    result = evaluate_case(
        9,
        "test_zero_M",
        model,
        np.zeros(1),
        np.zeros(1),
        np.ones(1),
        M=0.0,
        rtol=0.0,
        atol=0.0,
    )
    assert not result.passed
    output = save_violation(result, seed=5, root=tmp_path)
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["case"]["ratio"] == "inf"
