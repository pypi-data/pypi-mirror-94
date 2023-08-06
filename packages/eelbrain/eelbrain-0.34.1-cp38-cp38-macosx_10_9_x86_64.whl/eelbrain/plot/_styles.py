# Author: Christian Brodbeck <christianbrodbeck@nyu.edu>
"""Style specification"""
from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, replace
from functools import reduce
from itertools import chain, product
from math import ceil
import operator
from typing import Any, Dict, Sequence, Tuple, Union

import numpy as np
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap, to_rgb, to_rgba

from .._colorspaces import LocatedListedColormap, lch_to_rgb, rgb_to_lch, oneway_colors, twoway_colors, symmetric_cmaps
from .._data_obj import CategorialVariable, Factor, Interaction, CellArg
from .._exceptions import KeysMissing
from .._utils import LazyProperty


# masked keys that act as modifier rather than replacement
modifer_keys = {'alpha', 'saturation'}


@dataclass
class Style:
    """Control color/pattern by category"""
    color: Any = (0, 0, 0)
    marker: str = None
    hatch: str = ''
    linestyle: str = None
    linewidth: float = None
    zorder: float = 0  # z-order shift (relative to plot element default)
    masked: Union[Any, Dict[str, Any]] = None  # Any should be Style, but autodoc does not support foward reference under decorator yet https://github.com/agronholm/sphinx-autodoc-typehints/issues/76

    @LazyProperty
    def line_args(self):
        return {'color': self.color, 'linestyle': self.linestyle, 'linewidth': self.linewidth, 'marker': self.marker, 'markerfacecolor': self.color, 'zorder': 2 + self.zorder}

    @LazyProperty
    def patch_args(self):
        return {'facecolor': self.color, 'hatch': self.hatch, 'zorder': 1 + self.zorder}

    @LazyProperty
    def masked_style(self):  # -> 'Style'
        if self.masked is None:
            return replace(self, color=(0.7, 0.7, 0.7, 0.4))
        elif isinstance(self.masked, Style):
            return self.masked
        elif isinstance(self.masked, dict):
            kwargs = self.masked
            if modifer_keys.intersection(self.masked):
                kwargs = dict(kwargs)
                r, g, b, a = to_rgba(self.color)
                a *= kwargs.pop('alpha', 1)
                l, c, h = rgb_to_lch(r, g, b)
                c *= kwargs.pop('saturation', 1)
                kwargs['color'] = (*lch_to_rgb(l, c, h), a)
            return replace(self, **kwargs)
        else:
            raise TypeError(f"Style is invalid masked parameter: {self.masked!r}")

    @classmethod
    def _coerce(cls, arg):
        if isinstance(arg, cls):
            return arg
        elif arg is None:
            return cls()
        else:
            return cls(arg)


def to_styles_dict(colors: Dict[CellArg, Any]) -> StylesDict:
    return {cell: Style._coerce(spec) for cell, spec in colors.items()}


def find_cell_styles(
        x: CategorialVariable,
        colors: ColorsArg,
        cells: Sequence[CellArg] = None,
        fallback: bool = True,
) -> StylesDict:
    """Process the colors arg from plotting functions

    Parameters
    ----------
    x
        Model for which colors are needed. ``None`` if only a single value is
        plotted.
    colors
        Colors for the plots if multiple categories of data are plotted.
        **str**: A colormap name; cells are mapped onto the colormap in
        regular intervals.
        **list**: A list of colors in the same sequence as cells.
        **dict**: A dictionary mapping each cell to a color.
        Colors are specified as `matplotlib compatible color arguments
        <http://matplotlib.org/api/colors_api.html>`_.
    cells
        In case only a subset of cells is used.
    fallback
        If a cell is missing, fall back on partial cells (on by default).
    """
    if x is None:
        if not isinstance(colors, dict):
            if colors is None:
                colors = 'k'
            colors = {None: colors}
        return to_styles_dict(colors)
    elif cells is None:
        cells = x.cells

    if isinstance(colors, (list, tuple)):
        if len(colors) < len(cells):
            raise ValueError(f"colors={colors!r}: only {len(colors)} colors for {len(cells)} cells.")
        out = dict(zip(cells, colors))
    elif isinstance(colors, dict):
        out = colors.copy()
        missing = [cell for cell in cells if cell not in out]
        if missing:
            if fallback:
                for cell in missing[:]:
                    if isinstance(cell, str):
                        continue
                    super_cells = chain((cell[:-i] for i in range(1, len(cell))), (cell[0],))
                    for super_cell in super_cells:
                        if super_cell in out:
                            out[cell] = out[super_cell]
                            missing.remove(cell)
                            break
            if missing:
                raise KeysMissing(missing, 'colors', colors)
    elif colors is None or isinstance(colors, str):
        out = colors_for_categorial(x, cmap=colors)
    else:
        raise TypeError(f"colors={colors!r}")
    return to_styles_dict(out)


def colors_for_categorial(x, hue_start=0.2, cmap=None):
    """Automatically select colors for a categorial model

    Parameters
    ----------
    x : categorial
        Model defining the cells for which to define colors.
    hue_start : 0 <= scalar < 1
        First hue value (only for two-way or higher level models).
    cmap : str (optional)
        Name of a matplotlib colormap to use instead of default hue-based
        colors (only used for one-way models).

    Returns
    -------
    colors : dict {cell -> color}
        Dictionary providing colors for the cells in x.
    """
    if isinstance(x, Factor):
        return colors_for_oneway(x.cells, hue_start, cmap=cmap)
    elif isinstance(x, Interaction):
        return colors_for_nway([f.cells for f in x.base], hue_start)
    else:
        raise TypeError(f"x={x!r}: needs to be Factor or Interaction")


def colors_for_oneway(
        cells,
        hue_start: Union[float, Sequence[float]] = 0.2,
        light_range: Union[float, Tuple[float, float]] = 0.5,
        cmap: str = None,
        light_cycle: int = None,
        always_cycle_hue: bool = False,
        locations: Sequence[float] = None,
        unambiguous: Union[bool, Sequence[int]] = None,
):
    """Define colors for a single factor design

    Parameters
    ----------
    cells : sequence of str
        Cells for which to assign colors.
    hue_start
        First hue value (``0 <= hue < 1``) or list of hue values.
    light_range : scalar | tuple of 2 scalar
        Scalar that specifies the amount of lightness variation (default 0.5).
        If positive, the first color is lightest; if negative, the first color
        is darkest. A tuple can be used to specify exact end-points (e.g.,
        ``(1.0, 0.4)``). ``0.2`` is equivalent to ``(0.4, 0.6)``.
        The ``light_cycle`` parameter can be used to cycle between light and
        dark more than once.
    cmap
        Use a matplotlib colormap instead of the default color generation
        algorithm. Name of a matplotlib colormap to use (e.g., 'jet'). If
        specified, ``hue_start`` and ``light_range`` are ignored.
    light_cycle
        Cycle from light to dark in ``light_cycle`` cells to make nearby colors
        more distinct (default cycles once).
    always_cycle_hue
        Cycle hue even when cycling lightness. With ``False`` (default), hue
        is constant within a lightness cycle.
    locations
        Locations of the cells on the color-map (all in range [0, 1]; default is
        evenly spaced; example: ``numpy.linspace(0, 1, len(cells)) ** 0.5``).
    unambiguous
        Use `unambiguos colors <https://jfly.uni-koeln.de/html/color_blind/
        #pallet>`_. If ``True``, choose the ``n`` first colors; use a list of
        ``int`` to pick specific colors. Other parameters are ignored.

    Returns
    -------
    dict : {str: tuple}
        Mapping from cells to colors.
    """
    if isinstance(cells, Iterator):
        cells = tuple(cells)
    n = len(cells)
    if cmap is None:
        colors = oneway_colors(n, hue_start, light_range, light_cycle, always_cycle_hue, locations, unambiguous)
    else:
        cm = mpl.cm.get_cmap(cmap)
        if locations is None:
            imax = n - 1
            locations = (i / imax for i in range(n))
        colors = (cm(x) for x in locations)
    return dict(zip(cells, colors))


def colors_for_twoway(
        x1_cells: Sequence[str],
        x2_cells: Sequence[str],
        hue_start: float = 0.2,
        hue_shift: float = 0.,
        hues: Sequence[float] = None,
        lightness: Union[float, Sequence[float]] = None,
):
    """Define cell colors for a two-way design

    Parameters
    ----------
    x1_cells
        Cells of the major factor.
    x2_cells
        Cells of the minor factor.
    hue_start : 0 <= scalar < 1
        First hue value.
    hue_shift : 0 <= scalar < 1
        Use that part of the hue continuum between categories to shift hue
        within categories.
    hues
        List of hue values corresponding to the levels of the first factor
        (overrides regular hue distribution).
    lightness
        If specified as scalar, colors will occupy the range
        ``[lightness, 100-lightness]``. Can also be given as list with one
        value corresponding to each element in the second factor.

    Returns
    -------
    dict : {tuple: tuple}
        Mapping from cells to colors.
    """
    x1_cells = list(x1_cells)
    x2_cells = list(x2_cells)
    n1 = len(x1_cells)
    n2 = len(x2_cells)
    if n1 < 2 or n2 < 2:
        raise ValueError("Need at least 2 cells on each factor")

    clist = twoway_colors(n1, n2, hue_start, hue_shift, hues, lightness)
    return dict(zip(product(x1_cells, x2_cells), clist))


def colors_for_nway(
        cell_lists: Sequence[CellArg],
        hue_start: float = 0.2,
):
    """Define cell colors for a two-way design

    Parameters
    ----------
    cell_lists : sequence of of tuple of str
        List of the cells for each factor. E.g. for ``A % B``:
        ``[('a1', 'a2'), ('b1', 'b2', 'b3')]``.
    hue_start : 0 <= scalar < 1
        First hue value.

    Returns
    -------
    dict : {tuple: tuple}
        Mapping from cells to colors.
    """
    if len(cell_lists) == 1:
        return colors_for_oneway(cell_lists[0])
    elif len(cell_lists) == 2:
        return colors_for_twoway(cell_lists[0], cell_lists[1], hue_start)
    elif len(cell_lists) > 2:
        ns = tuple(map(len, cell_lists))
        n_outer = reduce(operator.mul, ns[:-1])
        n_inner = ns[-1]

        # outer circle
        hues = np.linspace(hue_start, 1 + hue_start, ns[0], False)
        # subdivide for each  level
        distance = 1. / ns[0]
        for n_current in ns[1:-1]:
            new = []
            d = distance / 3
            for hue in hues:
                new.extend(np.linspace(hue - d, hue + d, n_current))
            hues = new
            distance = 2 * d / (n_current - 1)
        hues = np.asarray(hues)
        hues %= 1
        colors = twoway_colors(n_outer, n_inner, hues=hues)
        return dict(zip(product(*cell_lists), colors))
    else:
        return {}


def single_hue_colormap(hue: ColorArg):
    """Colormap based on single hue

    Parameters
    ----------
    hue : matplotlib color
        Base RGB color.

    Returns
    -------
    colormap : matplotlib Colormap
        Colormap from transparent to ``hue``.
    """
    name = str(hue)
    color = to_rgb(hue)
    start = color + (0.,)
    stop = color + (1.,)
    return LinearSegmentedColormap.from_list(name, (start, stop))


def soft_threshold_colormap(
        cmap: str,
        threshold: float,
        vmax: float,
        subthreshold: ColorArg = None,
        symmetric: bool = None,
) -> mpl.colors.ListedColormap:
    """Soft-threshold a colormap to make small values transparent

    Parameters
    ----------
    cmap
        Base colormap.
    threshold
        Value at which to threshold the colormap (i.e., the value at which to
        start the colormap).
    vmax
        Intended largest value of the colormap (used to infer the location of
        the ``threshold``).
    subthreshold : matplotlib color
        Color of sub-threshold values (the default is the end or middle of
        the colormap, depending on whether it is symmetric).
    symmetric
        Whether the ``cmap`` is symmetric (ranging from ``-vmax`` to ``vmax``)
        or not (ranging from ``0`` to ``vmax``). The default is ``True`` for
        known symmetric colormaps and ``False`` otherwise.

    Returns
    -------
    thresholded_cmap
        Soft-thresholded colormap.
    """
    assert vmax > threshold >= 0
    cmap = mpl.cm.get_cmap(cmap)
    if symmetric is None:
        symmetric = cmap.name in symmetric_cmaps

    colors = cmap(np.linspace(0., 1., cmap.N))
    if subthreshold is None:
        subthreshold_color = cmap(0.5) if symmetric else cmap(0)
    else:
        subthreshold_color = to_rgba(subthreshold)

    n = int(round(vmax / ((vmax - threshold) / cmap.N)))
    out_colors = np.empty((n, 4))
    if symmetric:
        i_threshold = int(ceil(cmap.N / 2))
        out_colors[:i_threshold] = colors[:i_threshold]
        out_colors[i_threshold:-i_threshold] = subthreshold_color
        out_colors[-i_threshold:] = colors[-i_threshold:]
    else:
        out_colors[:-cmap.N] = subthreshold_color
        out_colors[-cmap.N:] = colors
    out = LocatedListedColormap(out_colors, cmap.name)
    out.vmax = vmax
    out.vmin = -vmax if symmetric else 0
    out.symmetric = symmetric
    return out


ColorArg = Union[str, Sequence[float]]
ColorsArg = Union[ColorArg, Dict[CellArg, ColorArg], Sequence[ColorArg]]
StylesDict = Dict[CellArg, Style]
