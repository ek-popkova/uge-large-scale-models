"""Common plot style and figure export.

Every figure that goes into the report is saved with :func:`save_figure`, which writes a vector
PDF to ``report/figures/<name>.pdf`` (referenced in LaTeX as ``\\includegraphics{<name>}``).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING

from . import config

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

# Shared style for all figures (applied by ``setup_style``).
RCPARAMS = {
    "figure.dpi": 100,
    "savefig.dpi": 300,
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "legend.fontsize": 8,
    "pdf.fonttype": 42,  # embed TrueType fonts, keeps text selectable
}
MAP_FIGSIZE = (6.0, 6.0)
MAP_CMAP = "viridis"
MAP_EDGECOLOR = "white"
MAP_LINEWIDTH = 0.3


def setup_style() -> None:
    """Apply the common matplotlib style (call once at the top of a notebook)."""
    import matplotlib as mpl

    mpl.rcParams.update(RCPARAMS)


def style_map_axes(ax: "Axes") -> "Axes":
    """Common map look: equal aspect, no axes frame."""
    ax.set_aspect("equal")
    ax.set_axis_off()
    return ax


def map_axes(figsize: tuple[float, float] = MAP_FIGSIZE) -> tuple["Figure", "Axes"]:
    """Create a figure with a single axes styled for maps."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=figsize)
    return fig, style_map_axes(ax)


def save_figure(fig: "Figure", name: str) -> Path:
    """Save ``fig`` as ``report/figures/<name>.pdf`` and return the path.

    Parameters
    ----------
    fig : matplotlib Figure
    name : str
        File stem without extension or directory, e.g. ``"age_distribution"``. Use the same name as
        in the ``\\figplaceholder{...}`` of the report chapter.
    """
    if not re.fullmatch(r"[A-Za-z0-9_\-]+", name):
        raise ValueError(f"figure name must be a plain file stem (letters, digits, _ or -): {name!r}")
    config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = config.FIGURES_DIR / f"{name}.pdf"
    fig.savefig(path, format="pdf", bbox_inches="tight")
    return path
