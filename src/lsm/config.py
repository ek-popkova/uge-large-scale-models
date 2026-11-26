"""Central configuration: study area, CRS, paths, random seed and model parameters.

Everything that the notebooks and the report have to agree on lives here, so that a number is
defined exactly once. Values marked TODO need a human decision.
"""

from __future__ import annotations

from pathlib import Path

# --------------------------------------------------------------------------------------
# Study area
# --------------------------------------------------------------------------------------
# TODO: INSEE department code of the study area (string, e.g. "XX"; Corsica is "2A"/"2B").
# Must not be in Ile-de-France (75, 77, 78, 91, 92, 93, 94, 95).
DEPARTMENT: str = "TODO"

CRS: str = "EPSG:2154"  # RGF93 / Lambert-93, metres; used for all geometries and distances

# --------------------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
FIGURES_DIR = ROOT / "report" / "figures"

# Raw files. TODO: adjust the file names to what was actually downloaded
# (see data/DATA_SOURCES.md).
CENSUS_DETAILED_CSV = DATA_RAW / "TODO_FD_INDCVIZx_2019.csv"      # INSEE, detailed census
CENSUS_AGGREGATED_CSV = DATA_RAW / "TODO_base-ic-evol-struct-pop-2019.csv"  # INSEE, IRIS
IRIS_SHAPEFILE = DATA_RAW / "TODO_CONTOURS-IRIS.shp"              # IGN CONTOURS-IRIS 2021
URSSAF_CSV = DATA_RAW / "TODO_urssaf_commune_x_ape.csv"           # URSSAF export
OSM_PBF = DATA_RAW / "TODO_region-latest.osm.pbf"                 # Geofabrik

# Processed files (written by the notebooks, git-ignored)
ZONES_PARQUET = DATA_PROCESSED / "zones.parquet"   # hand-off A -> B, see lsm.io.write_zones
ZONES_PLACEHOLDER_MARKER = DATA_PROCESSED / "zones.PLACEHOLDER"
CENSUS_PARQUET = DATA_PROCESSED / "census_individuals.parquet"  # A1 -> A2
IRIS_GPKG = DATA_PROCESSED / "iris.gpkg"                        # A1 -> A2, A3, A4
MUNICIPALITIES_GPKG = DATA_PROCESSED / "municipalities.gpkg"    # A1 -> A2, A3, A4
EMPLOYMENT_PARQUET = DATA_PROCESSED / "employment.parquet"      # A3 -> A4
FLOWS_PARQUET = DATA_PROCESSED / "flows.parquet"                # B1 -> B2
TRIPS_PARQUET = DATA_PROCESSED / "trips.parquet"                # B2 -> B3
NETWORK_GRAPHML = DATA_PROCESSED / "network.graphml"            # B3
EDGE_FLOWS_GPKG = DATA_PROCESSED / "edge_flows.gpkg"            # B3

# --------------------------------------------------------------------------------------
# Randomness
# --------------------------------------------------------------------------------------
SEED: int = 42  # used for all random sampling (Exercise 3.1); report it in the appendix

# --------------------------------------------------------------------------------------
# Model parameters (from the assignment, Autumn 2026)
# --------------------------------------------------------------------------------------
# Exercise 2.1, Table 1: O_i = max(beta_0 + sum_s beta_s * n_{i,s}, 0). The offset is added ONCE.
TRIP_GEN_OFFSET: float = 27.244
SPC_LABELS: dict[int, str] = {
    1: "Agriculteurs exploitants",
    2: "Artisans, commerçants et chefs d'entreprise",
    3: "Cadres et professions intellectuelles supérieures",
    4: "Professions intermédiaires",
    5: "Employés",
    6: "Ouvriers",
    7: "Retraités",
    8: "Autres personnes sans activité professionnelle",
}
TRIP_GEN_BETA: dict[int, float] = {
    1: 0.319,
    2: 0.994,
    3: 0.863,
    4: 0.990,
    5: 0.780,
    6: 0.708,
    7: 0.120,
    8: -0.073,
}

# Exercise 2.2: N = min(0.7 * sum_j W_j, 0.7 * sum_i O_i)
COMMUTER_SHARE: float = 0.7

# Exercise 2.3, Table 2: rho_ij = exp(beta * d_ij + alpha), d_ij in metres.
# alpha is a constant factor exp(alpha) that cancels in the balancing (absorbed by p_i, a_j);
# TODO: confirm the symbols of the two Table 2 parameters in the assignment PDF.
FRICTION_BETA: float = -1.1e-4
FRICTION_ALPHA: float = -0.4
GRAVITY_MAX_ITER: int = 500
GRAVITY_TOL: float = 1e-10  # max relative change of p_i, a_j between two iterations

# Exercise 3.1
N_TRIPS: int = 10_000  # "at least 10,000" individual trips
# T ~ Normal(mu, sigma^2) in seconds after midnight, negative values reset to 0.
# TODO: confirm mu in the assignment PDF. The text export reads "83600", which looks like a
# lost multiplication sign: 8 * 3600 = 28800 s = 08:00.
DEPARTURE_MU_S: float = 8 * 3600
DEPARTURE_SIGMA_S: float = 3600.0
