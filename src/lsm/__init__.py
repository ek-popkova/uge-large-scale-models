"""Shared code for the "Large-scale models" course project (agent-based transport demand).

Modules
-------
config    department, CRS, paths, random seed, model parameters
io        loaders for the raw data sets and the hand-off file ``zones.parquet``
geo       municipalities from IRIS, centroids, distance matrix
gravity   double-constrained gravity model
plotting  common map style and ``save_figure``
"""

__version__ = "0.1.0"
