import numpy as np

from scripts.math_utils import paired_radius


def test_large_common_action_with_tiny_separation_has_smaller_radius() -> None:
    common = np.array([100.0, 0.0, 0.0])
    close_s0 = common
    close_s1 = common + np.array([0.0, 1e-4, 0.0])
    wide_s0 = common
    wide_s1 = -common

    close_radius = paired_radius(close_s0, close_s1, M=1.0)
    wide_radius = paired_radius(wide_s0, wide_s1, M=1.0)

    assert close_radius < 1e-5 * wide_radius


def test_radius_depends_on_action_separation_not_only_norms() -> None:
    radius_same = paired_radius([3.0, 4.0], [3.0, 4.0], M=2.0)
    radius_opposite = paired_radius([3.0, 4.0], [-3.0, -4.0], M=2.0)
    assert radius_same == 0.0
    assert radius_opposite > 0.0


def test_zero_action_reduces_to_absolute_cubic_radius() -> None:
    action = np.array([2.0, -1.0, 2.0])
    expected = (1.7 / 6.0) * np.linalg.norm(action) ** 3
    assert paired_radius(np.zeros_like(action), action, 1.7) == expected
