"""Zones and distances: municipalities from IRIS, centroids, distance matrix.

Municipalities are the zones of the gravity model. They are built by dissolving the IRIS polygons
(IGN CONTOURS-IRIS), because the census and the boundaries then share the same vintage.
Beware: municipality codes can differ between sources (merged communes, vintages) and, for
Paris/Lyon/Marseille, the IRIS file uses the arrondissement codes. Always check joins.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from . import config

if TYPE_CHECKING:
    import geopandas as gpd


def municipalities_from_iris(iris: "gpd.GeoDataFrame") -> "gpd.GeoDataFrame":
    """Dissolve IRIS polygons into municipality polygons.

    Parameters
    ----------
    iris : GeoDataFrame
        Output of ``lsm.io.load_iris_boundaries`` (columns ``municipality_id, name, geometry``).

    Returns
    -------
    GeoDataFrame with columns ``municipality_id, name, geometry`` (EPSG:2154), one row per
    municipality, sorted by ``municipality_id`` (this fixes the zone order of the pipeline).
    """
    municipalities = (
        iris[["municipality_id", "name", "geometry"]]
        .dissolve(by="municipality_id", aggfunc="first")
        .reset_index()
        .sort_values("municipality_id", ignore_index=True)
    )
    return municipalities.set_crs(config.CRS, allow_override=True)


def centroids(zones: "gpd.GeoDataFrame") -> np.ndarray:
    """Centroid coordinates of the zones as an ``(n, 2)`` array ``[x, y]`` in metres.

    The CRS must be projected (``config.CRS``); centroids of geographic coordinates are wrong.
    """
    c = zones.geometry.centroid
    return np.column_stack([c.x.to_numpy(), c.y.to_numpy()])


def distance_matrix(xy: np.ndarray) -> np.ndarray:
    """Euclidean distance matrix in metres between points.

    Parameters
    ----------
    xy : (n, 2) array
        Coordinates in a projected CRS.

    Returns
    -------
    (n, n) array
        ``d[i, j] = ||xy[i] - xy[j]||``; symmetric with a zero diagonal.
    """
    xy = np.asarray(xy, dtype=float)
    diff = xy[:, None, :] - xy[None, :, :]
    return np.sqrt((diff**2).sum(axis=-1))
