"""Toy example of the assignment (Exercise 2.3, Tables 3-5) for the gravity model.

These tests FAIL (NotImplementedError) until ``lsm.gravity`` is implemented. That is expected.

About D_1: the assignment prints D_1 = 9462 in Table 3, which is a typo (9462 is d_14). The value
that matches the column sum of Table 5 is D_1 = 420, which is used in ``test_toy_flows``.
Note that 420 + 2294 + 48377 + 6621 = 57712, whereas sum(O) = 57715 (Table 5 shows rounded-down
flows). With D_1 = 423 the totals are balanced and the floored flows match Table 5 exactly
(``test_toy_flows_balanced_totals``).
"""

import numpy as np
import pytest

from lsm.gravity import double_constrained_gravity

O = np.array([3396, 5442, 43196, 5681], dtype=float)
D_ASSIGNMENT = np.array([420, 2294, 48377, 6621], dtype=float)  # D_1 = 420, see module docstring
D_BALANCED = np.array([423, 2294, 48377, 6621], dtype=float)  # sums to sum(O) = 57715

DISTANCE = np.array(
    [
        [0, 4066, 6595, 9462],
        [4066, 0, 4340, 10299],
        [6595, 4340, 0, 7287],
        [9462, 10299, 7287, 0],
    ],
    dtype=float,
)

# Table 5 of the assignment (values rounded down)
EXPECTED_FLOORED = np.array(
    [
        [74, 220, 2661, 439],
        [61, 445, 4415, 518],
        [247, 1463, 37659, 3825],
        [38, 163, 3640, 1837],
    ]
)


def test_toy_flows():
    """Floored flows reproduce Table 5 within +-2 (D_1 = 420 as in the assignment)."""
    flows = double_constrained_gravity(O, D_ASSIGNMENT, DISTANCE)
    assert flows.shape == (4, 4)
    assert np.all(np.abs(np.floor(flows) - EXPECTED_FLOORED) <= 2)


def test_toy_flows_balanced_totals():
    """With sum(D) == sum(O) (D_1 = 423) the floored flows match Table 5 exactly."""
    flows = double_constrained_gravity(O, D_BALANCED, DISTANCE)
    np.testing.assert_array_equal(np.floor(flows), EXPECTED_FLOORED)


def test_toy_marginals_balanced_totals():
    """Row sums equal O and column sums equal D when the totals are balanced."""
    flows = double_constrained_gravity(O, D_BALANCED, DISTANCE)
    np.testing.assert_allclose(flows.sum(axis=1), O, rtol=1e-6)
    np.testing.assert_allclose(flows.sum(axis=0), D_BALANCED, rtol=1e-6)


@pytest.mark.parametrize("alpha", [0.0, -0.4, 1.3])
def test_friction_intercept_is_irrelevant(alpha):
    """A constant factor exp(alpha) in the friction is absorbed by p_i and a_j."""
    reference = double_constrained_gravity(O, D_BALANCED, DISTANCE, alpha=0.0)
    flows = double_constrained_gravity(O, D_BALANCED, DISTANCE, alpha=alpha)
    np.testing.assert_allclose(flows, reference, rtol=1e-6)
