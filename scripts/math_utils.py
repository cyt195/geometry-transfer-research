"""Mathematical primitives for intrinsic value and paired transfer.

The functions in this module implement declared formulas. They do not infer
historical Gate-3 metrics or read frozen evidence.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray


FloatArray = NDArray[np.float64]


def _vector(name: str, value: ArrayLike) -> FloatArray:
    array = np.asarray(value, dtype=float)
    if array.ndim != 1:
        raise ValueError(f"{name} must be a one-dimensional vector")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    return array


def _square_matrix(name: str, value: ArrayLike, dimension: int) -> FloatArray:
    array = np.asarray(value, dtype=float)
    if array.shape != (dimension, dimension):
        raise ValueError(
            f"{name} must have shape {(dimension, dimension)}, got {array.shape}"
        )
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    return array


def intrinsic_terms(
    h: ArrayLike, K: ArrayLike, Omega: ArrayLike, P: ArrayLike
) -> tuple[float, float]:
    """Return ``(A_P, B_P)`` for the stochastic-quadratic valuation.

    ``P`` is checked to be symmetric positive definite because that is part of
    the declared model. ``K`` and ``Omega`` are shape-checked but not projected
    or repaired: invalid scientific inputs should remain visible.
    """

    h_array = _vector("h", h)
    dimension = h_array.size
    k_array = _square_matrix("K", K, dimension)
    omega_array = _square_matrix("Omega", Omega, dimension)
    p_array = _square_matrix("P", P, dimension)

    if not np.allclose(p_array, p_array.T, rtol=1e-10, atol=1e-12):
        raise ValueError("P must be symmetric")
    try:
        np.linalg.cholesky(p_array)
    except np.linalg.LinAlgError as error:
        raise ValueError("P must be positive definite") from error

    a_p = float(h_array @ p_array @ h_array)
    b_p = float(
        h_array @ p_array @ k_array @ p_array @ h_array
        + np.trace(k_array @ p_array @ omega_array @ p_array)
    )
    return a_p, b_p


def intrinsic_value(h: ArrayLike, K: ArrayLike, Omega: ArrayLike, P: ArrayLike) -> float:
    """Return ``A_P**2 / (2 B_P)`` and explicitly reject ``B_P <= 0``."""

    a_p, b_p = intrinsic_terms(h, K, Omega, P)
    if not np.isfinite(b_p) or b_p <= 0.0:
        raise ValueError(f"intrinsic value requires B_P > 0; received B_P={b_p}")
    return a_p * a_p / (2.0 * b_p)


def paired_radius(s0: ArrayLike, s1: ArrayLike, M: float) -> float:
    """Return the candidate-differential paired transfer radius exactly.

    The formula is

    ``M/6 * (||s0||^2 + <s0,s1> + ||s1||^2) * ||s1-s0||``.
    """

    s0_array = _vector("s0", s0)
    s1_array = _vector("s1", s1)
    if s0_array.shape != s1_array.shape:
        raise ValueError("s0 and s1 must have the same shape")
    m_value = float(M)
    if not np.isfinite(m_value) or m_value < 0.0:
        raise ValueError("M must be a finite nonnegative Hessian-Lipschitz constant")

    geometry = float(
        s0_array @ s0_array + s0_array @ s1_array + s1_array @ s1_array
    )
    separation = float(np.linalg.norm(s1_array - s0_array))
    return (m_value / 6.0) * geometry * separation


@dataclass(frozen=True)
class KnownMCubic:
    """The known-``M`` family ``f(x)=x^T A x/2 + lambda sum(x_i^3)/6``."""

    A: FloatArray
    lambda_: float

    def __post_init__(self) -> None:
        matrix = np.asarray(self.A, dtype=float)
        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("A must be a square matrix")
        if not np.all(np.isfinite(matrix)):
            raise ValueError("A must contain only finite values")
        if not np.allclose(matrix, matrix.T, rtol=1e-10, atol=1e-12):
            raise ValueError("A must be symmetric")
        coefficient = float(self.lambda_)
        if not np.isfinite(coefficient):
            raise ValueError("lambda_ must be finite")
        object.__setattr__(self, "A", matrix)
        object.__setattr__(self, "lambda_", coefficient)

    @property
    def dimension(self) -> int:
        return int(self.A.shape[0])

    @property
    def hessian_lipschitz_constant(self) -> float:
        """A valid global operator-norm Hessian-Lipschitz constant."""

        return abs(self.lambda_)

    def _point(self, name: str, value: ArrayLike) -> FloatArray:
        point = _vector(name, value)
        if point.size != self.dimension:
            raise ValueError(
                f"{name} must have dimension {self.dimension}, got {point.size}"
            )
        return point

    def value(self, x: ArrayLike) -> float:
        point = self._point("x", x)
        return float(
            0.5 * point @ self.A @ point
            + (self.lambda_ / 6.0) * np.sum(point**3)
        )

    def gradient(self, x: ArrayLike) -> FloatArray:
        point = self._point("x", x)
        return self.A @ point + 0.5 * self.lambda_ * point**2

    def hessian(self, x: ArrayLike) -> FloatArray:
        point = self._point("x", x)
        return self.A + self.lambda_ * np.diag(point)

    def quadratic_model(self, base: ArrayLike, step: ArrayLike) -> float:
        base_point = self._point("base", base)
        step_vector = self._point("step", step)
        return float(
            self.value(base_point)
            + self.gradient(base_point) @ step_vector
            + 0.5 * step_vector @ self.hessian(base_point) @ step_vector
        )

    def quadratic_taylor_remainder(self, base: ArrayLike, step: ArrayLike) -> float:
        """Return the exact cubic Taylor remainder.

        The base is still validated, but the algebraically exact expression is
        used to avoid cancellation from subtracting two large objective values.
        """

        self._point("base", base)
        step_vector = self._point("step", step)
        return float((self.lambda_ / 6.0) * np.sum(step_vector**3))

    def direct_quadratic_taylor_remainder(
        self, base: ArrayLike, step: ArrayLike
    ) -> float:
        """Evaluate ``f(base+step)-Q(step)`` directly for implementation checks."""

        base_point = self._point("base", base)
        step_vector = self._point("step", step)
        return self.value(base_point + step_vector) - self.quadratic_model(
            base_point, step_vector
        )


def transfer_differences(
    model: KnownMCubic, base: ArrayLike, s0: ArrayLike, s1: ArrayLike
) -> tuple[float, float, float]:
    """Return ``(Delta_Q, Delta_real, Delta_real-Delta_Q)``.

    Every difference is oriented as candidate 1 minus candidate 0.
    """

    base_point = model._point("base", base)
    s0_vector = model._point("s0", s0)
    s1_vector = model._point("s1", s1)
    delta_q = model.quadratic_model(base_point, s1_vector) - model.quadratic_model(
        base_point, s0_vector
    )
    delta_real = model.value(base_point + s1_vector) - model.value(
        base_point + s0_vector
    )
    remainder_difference = model.quadratic_taylor_remainder(
        base_point, s1_vector
    ) - model.quadratic_taylor_remainder(base_point, s0_vector)
    return float(delta_q), float(delta_real), float(remainder_difference)
