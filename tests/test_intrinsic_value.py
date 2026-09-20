import numpy as np
import pytest

from scripts.math_utils import KnownMCubic, intrinsic_terms, intrinsic_value


def _spd(rng: np.random.Generator, dimension: int) -> np.ndarray:
    raw = rng.normal(size=(dimension, dimension))
    return raw.T @ raw + 0.5 * np.eye(dimension)


@pytest.mark.parametrize("scale", [1e-4, 0.1, 1.0, 7.5, 1e4])
def test_intrinsic_value_is_scale_invariant(scale: float) -> None:
    rng = np.random.default_rng(31415)
    dimension = 6
    h = rng.normal(size=dimension)
    K = _spd(rng, dimension)
    Omega = _spd(rng, dimension)
    P = _spd(rng, dimension)

    baseline = intrinsic_value(h, K, Omega, P)
    scaled = intrinsic_value(h, K, Omega, scale * P)

    assert scaled == pytest.approx(baseline, rel=2e-12, abs=1e-14)


def test_intrinsic_value_rejects_nonpositive_b() -> None:
    h = np.array([1.0, -1.0])
    P = np.eye(2)
    K = -np.eye(2)
    Omega = np.zeros((2, 2))
    _, b_p = intrinsic_terms(h, K, Omega, P)
    assert b_p < 0.0
    with pytest.raises(ValueError, match="B_P > 0"):
        intrinsic_value(h, K, Omega, P)


def test_intrinsic_value_requires_spd_preconditioner() -> None:
    with pytest.raises(ValueError, match="positive definite"):
        intrinsic_value(
            np.ones(2), np.eye(2), np.eye(2), np.diag([1.0, -1.0])
        )


def test_known_m_cubic_exact_derivatives_and_remainder() -> None:
    model = KnownMCubic(np.array([[2.0, 0.3], [0.3, 1.0]]), -1.25)
    x = np.array([0.4, -0.7])
    step = np.array([0.2, -0.1])
    epsilon = 1e-6

    finite_gradient = np.array(
        [
            (
                model.value(x + epsilon * np.eye(2)[index])
                - model.value(x - epsilon * np.eye(2)[index])
            )
            / (2.0 * epsilon)
            for index in range(2)
        ]
    )
    assert model.gradient(x) == pytest.approx(finite_gradient, rel=1e-9, abs=1e-9)
    assert model.hessian(x) == pytest.approx(
        model.A + model.lambda_ * np.diag(x), rel=0.0, abs=0.0
    )
    assert model.quadratic_taylor_remainder(x, step) == pytest.approx(
        model.direct_quadratic_taylor_remainder(x, step), abs=1e-14
    )
    assert model.hessian_lipschitz_constant == abs(model.lambda_)
