"""Loaders for the raw data sets (clean column names) and the hand-off file ``zones.parquet``.

The loaders are STUBS (``NotImplementedError``): Person A implements them while working on the
notebooks. Column names of the raw files are noted from memory and must be verified against the
downloaded files (``data/DATA_SOURCES.md``). Conventions for the returned frames:

* ``municipality_id``  5-character INSEE code as ``str`` (Corsica: ``2A``/``2B``)
* ``iris_id``          9-character IRIS code as ``str``
* ``weight``           census weight ``IPONDI`` (always use it for statements about persons)
* geometries           EPSG:2154 (``config.CRS``)
"""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

from . import config

if TYPE_CHECKING:  # heavy imports only for type checkers; the functions import lazily
    import geopandas as gpd
    import networkx as nx
    import pandas as pd

ZONE_COLUMNS = ["municipality_id", "name", "geometry", "O", "D"]


# --------------------------------------------------------------------------------------
# Raw data loaders (stubs)
# --------------------------------------------------------------------------------------
def load_census_individuals(
    path=config.CENSUS_DETAILED_CSV, department: str = config.DEPARTMENT
) -> "pd.DataFrame":
    """INSEE detailed census 2019, "Individus localisés au canton-ou-ville" (semicolon CSV).

    Reads only the needed columns, keeps the persons of ``department`` and renames:

    ========  ============  ==============================================================
    raw       clean         notes
    ========  ============  ==============================================================
    IPONDI    weight        float, weight of the observation
    AGED      age           int, age in completed years
    CS1       spc           int 1..8, socio-professional category (8 postes)
    IRIS      iris_id       str; ``ZZZZZZZZZ`` when the person is only localised at
                            canton-ou-ville level (small municipalities)  [verify]
    CANTVILLE cantville     str, canton-ou-ville code (e.g. ``75ZZ``)
    DEPT      department    str
    ========  ============  ==============================================================

    Also derives ``municipality_id`` (first five characters of ``iris_id``), set to ``None``
    where ``iris_id`` is not identified. Read all code columns as ``str`` (leading zeros, 2A/2B).

    Returns
    -------
    DataFrame with columns ``weight, age, spc, iris_id, municipality_id, cantville``.
    """
    # TODO: implement
    raise NotImplementedError


def load_census_aggregated(
    path=config.CENSUS_AGGREGATED_CSV, department: str = config.DEPARTMENT
) -> "pd.DataFrame":
    """INSEE aggregated census "Population en 2019 - IRIS" (semicolon CSV).

    Returns one row per IRIS of ``department`` with columns

    * ``iris_id``, ``municipality_id``
    * ``population``              total population (``P19_POP``)  [verify]
    * ``pop15p``                  population aged 15+ (``C19_POP15P``)  [verify]
    * ``pop15p_spc1`` .. ``pop15p_spc8``   population 15+ per SPC (``C19_POP15P_CS1`` ..
      ``C19_POP15P_CS8``)  [verify]

    The ``n_{i,s}`` of the trip generation model (Exercise 2.1) are the ``pop15p_spc*`` columns.
    """
    # TODO: implement
    raise NotImplementedError


def load_iris_boundaries(
    path=config.IRIS_SHAPEFILE, department: str = config.DEPARTMENT
) -> "gpd.GeoDataFrame":
    """IGN CONTOURS-IRIS 2021 (shapefile, RGF93 / Lambert-93).

    Keeps the IRIS of ``department`` and renames ``CODE_IRIS -> iris_id``,
    ``INSEE_COM -> municipality_id``, ``NOM_COM -> name`` (``NOM_IRIS`` may be kept as
    ``iris_name``) [verify]. Reprojects to ``config.CRS`` if necessary.

    Returns
    -------
    GeoDataFrame with columns ``iris_id, municipality_id, name, geometry``.
    """
    # TODO: implement
    raise NotImplementedError


def load_urssaf_employment(
    path=config.URSSAF_CSV, department: str = config.DEPARTMENT
) -> "pd.DataFrame":
    """URSSAF employees per municipality x APE (CSV export, check the separator).

    Sums the employees over all APE (activity) codes and keeps the municipalities of
    ``department``. Municipalities absent from the file have no row: decide (and document in the
    report) whether they are zero or missing.

    Returns
    -------
    DataFrame with columns ``municipality_id, employees`` (float, the ``W_j`` of Exercise 2.2).
    """
    # TODO: implement
    raise NotImplementedError


def load_road_network(pbf_path=config.OSM_PBF, boundary=None) -> "nx.MultiDiGraph":
    """Routable road network from a Geofabrik ``.osm.pbf`` (pyrosm or osmium-tool + OSMnx).

    Parameters
    ----------
    pbf_path : path
        Regional OSM extract.
    boundary : shapely geometry or GeoDataFrame, optional
        Study-area boundary (EPSG:2154) used to crop the network; reproject to EPSG:4326 for OSM.

    Returns
    -------
    networkx.MultiDiGraph with edge attributes ``length`` (m) and, if available, travel time.
    """
    # TODO: implement
    raise NotImplementedError


# --------------------------------------------------------------------------------------
# Hand-off file zones.parquet
# --------------------------------------------------------------------------------------
def validate_zones(zones: "gpd.GeoDataFrame", rtol: float = 1e-9) -> None:
    """Check the hand-off contract of ``zones.parquet``; raise ``ValueError`` if it is violated.

    Contract: columns ``municipality_id`` (str, unique), ``name`` (str), ``geometry`` (EPSG:2154),
    ``O`` (float >= 0), ``D`` (float >= 0) and ``O.sum() == D.sum()`` (relative tolerance
    ``rtol``).
    """
    import numpy as np

    missing = [c for c in ZONE_COLUMNS if c not in zones.columns]
    if missing:
        raise ValueError(f"zones is missing columns: {missing}")
    if zones.crs is None or zones.crs.to_string() != config.CRS:
        raise ValueError(f"zones must have CRS {config.CRS}, got {zones.crs}")
    if zones["municipality_id"].duplicated().any():
        raise ValueError("municipality_id must be unique")
    if zones[["O", "D"]].isna().any().any() or (zones[["O", "D"]] < 0).any().any():
        raise ValueError("O and D must be non-negative and not NaN")
    if not np.isclose(zones["O"].sum(), zones["D"].sum(), rtol=rtol, atol=0.0):
        raise ValueError(
            f"O.sum() != D.sum(): {zones['O'].sum()} vs {zones['D'].sum()} (they must both equal N)"
        )


def write_zones(zones: "gpd.GeoDataFrame", placeholder: bool = False) -> None:
    """Validate and write ``data/processed/zones.parquet``.

    ``placeholder=True`` additionally creates the marker file ``data/processed/zones.PLACEHOLDER``;
    a real write (``placeholder=False``) removes it. Check for the marker before trusting results.
    """
    validate_zones(zones)
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    zones[ZONE_COLUMNS].to_parquet(config.ZONES_PARQUET)
    if placeholder:
        config.ZONES_PLACEHOLDER_MARKER.write_text(
            "zones.parquet contains PLACEHOLDER data (O = population 15+, D = URSSAF employment, "
            "scaled to the same total). Not the result of Exercises 2.1/2.2.\n"
        )
    else:
        config.ZONES_PLACEHOLDER_MARKER.unlink(missing_ok=True)


def read_zones() -> "gpd.GeoDataFrame":
    """Read and validate ``data/processed/zones.parquet`` (warns if it is a placeholder)."""
    import geopandas as gpd

    if config.ZONES_PLACEHOLDER_MARKER.exists():
        warnings.warn(
            "zones.parquet is PLACEHOLDER data (see data/processed/zones.PLACEHOLDER); "
            "do not use it for final results.",
            stacklevel=2,
        )
    zones = gpd.read_parquet(config.ZONES_PARQUET)
    validate_zones(zones)
    return zones


def write_placeholder_zones() -> "gpd.GeoDataFrame":
    """Write PLACEHOLDER zones so that Person B can start before Person A has finished.

    *** PLACEHOLDER: NOT the result of Exercises 2.1 / 2.2. ***
    ``O`` = population aged 15+ per municipality (instead of the trip generation model),
    ``D`` = URSSAF employment per municipality, both scaled to the same total
    ``N = COMMUTER_SHARE * min(sum(pop15+), sum(employment))``.

    Requires the loaders above and ``lsm.geo.municipalities_from_iris``. Writes
    ``zones.parquet`` and the marker ``zones.PLACEHOLDER``; Person A's final
    ``write_zones(zones)`` removes the marker.
    """
    from . import geo

    warnings.warn("Writing PLACEHOLDER zones (O = population 15+, D = URSSAF employment).", stacklevel=2)

    municipalities = geo.municipalities_from_iris(load_iris_boundaries())
    pop = load_census_aggregated().groupby("municipality_id", as_index=False)["pop15p"].sum()
    jobs = load_urssaf_employment()

    zones = municipalities.merge(pop, on="municipality_id", how="left").merge(
        jobs, on="municipality_id", how="left"
    )
    zones[["pop15p", "employees"]] = zones[["pop15p", "employees"]].fillna(0.0)

    n_total = config.COMMUTER_SHARE * min(zones["pop15p"].sum(), zones["employees"].sum())
    zones["O"] = zones["pop15p"] / zones["pop15p"].sum() * n_total
    zones["D"] = zones["employees"] / zones["employees"].sum() * n_total

    write_zones(zones, placeholder=True)
    return zones[ZONE_COLUMNS]
