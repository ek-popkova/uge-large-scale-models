"""Double-constrained gravity model (Exercise 2.3).

Hand-off contract
-----------------
``data/processed/zones.parquet`` is the ONLY interface between Person A (Exercises 1.1-2.2) and
Person B (Exercises 2.3-3.2). It has one row per municipality and the columns

    municipality_id  str       INSEE municipality code
    name             str       municipality name
    geometry         geometry  EPSG:2154
    O                float     scaled originating trips O'_i  (Exercise 2.2)
    D                float     arriving trips D_j             (Exercise 2.2)

with the constraint ``O.sum() == D.sum() == N`` (up to floating-point error). The row order of
that file fixes the order of the zones in every vector and matrix of this module.

Model
-----
Friction (d in metres)::

    rho_ij = exp(beta * d_ij + alpha)            beta = -1.1e-4, alpha = -0.4

Weighting factors, initialised to 1 and iterated until they stabilise::

    p_i = O_i / sum_j a_j * rho_ij
    a_j = D_j / sum_i p_i * rho_ij

Flows::

    F_ij = O_i / (sum_j' a_j' rho_ij')  *  D_j / (sum_i' p_i' rho_i'j)  *  rho_ij
         = p_i * a_j * rho_ij            (at convergence)

Notes
-----
* A constant factor in rho (e.g. exp(alpha)) is absorbed by p and a and does not change F.
* The iteration only converges to the exact marginals if ``sum(O) == sum(D)``; check this first.
* Check the implementation with ``tests/test_gravity_toy.py`` (toy example of the assignment).

All functions below are stubs: implement them (Person B).
"""

from __future__ import annotations

import numpy as np

from . import config


def friction_matrix(
    distance: np.ndarray,
    beta: float = config.FRICTION_BETA,
    alpha: float = config.FRICTION_ALPHA,
) -> np.ndarray:
    """Friction term ``rho_ij = exp(beta * d_ij + alpha)``.

    Parameters
    ----------
    distance : (n, n) array
        Centroid distances d_ij in metres.
    beta, alpha : float
        Parameters of Table 2 of the assignment.

    Returns
    -------
    (n, n) array
        Friction matrix rho.
    """
    # TODO: implement
    raise NotImplementedError


def balancing_factors(
    origins: np.ndarray,
    destinations: np.ndarray,
    friction: np.ndarray,
    max_iter: int = config.GRAVITY_MAX_ITER,
    tol: float = config.GRAVITY_TOL,
) -> tuple[np.ndarray, np.ndarray, int]:
    """Iterate the production and attraction factors ``p_i`` and ``a_j``.

    Starts from ``p = a = 1`` and alternates ``p_i = O_i / sum_j a_j rho_ij`` and
    ``a_j = D_j / sum_i p_i rho_ij`` until the largest relative change of ``p`` and ``a`` is
    below ``tol`` or ``max_iter`` is reached.

    Parameters
    ----------
    origins : (n,) array
        O_i (scaled demand O'_i).
    destinations : (n,) array
        D_j.
    friction : (n, n) array
        Friction matrix rho.
    max_iter, tol
        Stopping criteria.

    Returns
    -------
    p, a : (n,) arrays
        Production and attraction factors.
    n_iter : int
        Number of iterations performed (report it; warn if ``max_iter`` was hit).
    """
    # TODO: implement
    raise NotImplementedError


def flow_matrix(
    origins: np.ndarray,
    destinations: np.ndarray,
    friction: np.ndarray,
    p: np.ndarray,
    a: np.ndarray,
) -> np.ndarray:
    """Flow matrix ``F_ij`` from the balancing factors (formula in the module docstring).

    Returns
    -------
    (n, n) array
        Flows F_ij from zone i (row) to zone j (column). Row sums approximate ``origins``,
        column sums approximate ``destinations``.
    """
    # TODO: implement
    raise NotImplementedError


def double_constrained_gravity(
    origins: np.ndarray,
    destinations: np.ndarray,
    distance: np.ndarray,
    beta: float = config.FRICTION_BETA,
    alpha: float = config.FRICTION_ALPHA,
    max_iter: int = config.GRAVITY_MAX_ITER,
    tol: float = config.GRAVITY_TOL,
) -> np.ndarray:
    """Full model: friction -> balancing factors -> flow matrix.

    Parameters
    ----------
    origins, destinations : (n,) arrays
        O'_i and D_j, in the order of ``zones.parquet``.
    distance : (n, n) array
        Centroid distances in metres (see ``lsm.geo.distance_matrix``).
    beta, alpha, max_iter, tol
        See ``friction_matrix`` and ``balancing_factors``.

    Returns
    -------
    (n, n) array
        Flow matrix F_ij (floats; round or floor only for display).
    """
    # TODO: implement by combining the three functions above
    raise NotImplementedError
