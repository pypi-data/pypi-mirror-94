# Author: Christian Brodbeck <christianbrodbeck@nyu.edu>
"""Plot univariate data (:class:`~eelbrain.Var` objects)."""
import inspect
from itertools import chain
import logging
from typing import Any, Callable, Dict, Sequence, Union

import numpy as np
import scipy.linalg
import scipy.stats
import matplotlib.axes
from matplotlib.artist import setp
import matplotlib as mpl

from .._celltable import Celltable
from .._data_obj import VarArg, CategorialArg, UVArg, IndexArg, CellArg, Dataset, Var, asuv, asvar, ascategorial, assub, cellname
from .._stats import test, stats
from ._base import EelFigure, Layout, LegendMixin, CategorialAxisMixin, ColorBarMixin, XAxisMixin, YLimMixin, frame_title
from ._styles import ColorsArg, find_cell_styles


# keys for sorting kwargs
s = inspect.signature(mpl.axes.Axes.boxplot)
BOXPLOT_KEYWORDS = list(s.parameters)[2:]
del s

PAIRWISE_COLORS = ('#00FF00', '#FFCC00', '#FF6600', '#FF3300')


def _mark_plot_pairwise(  # Mark pairwise significance
        ax: matplotlib.axes.Axes,
        ct: Celltable,  # Data for the tests
        parametric: bool,  # Whether to perform parametric tests
        pos: Sequence[float],  # position of items on x axis
        bottom: float,  # Bottom of the space to use for the connectors (in data coordinates, i.e. highest point reached by the data plot)
        y_unit: float,  # Suggested scale for half the vertical distance between connectors (only used if top is None)
        corr: Union[str, None],
        trend: str,
        markers: bool,  # Plot markers indicating significance level (stars)
        levels: Union[dict, bool] = True,
        pwcolors: Sequence = None,
        top: float = None,  # Impose a fixed top end of the y-axis
) -> float:  # The top most value on the y axis
    # visual parameters
    if pwcolors is None:
        pwcolors = PAIRWISE_COLORS[1 - bool(trend):]
    font_size = mpl.rcParams['font.size'] * 1.5

    tests = test._pairwise(ct.get_data(), ct.all_within, parametric, corr, trend, levels)

    # plan grid layout
    k = len(ct.cells)
    reservation = np.zeros((sum(range(1, k)), k - 1))
    connections = []
    for distance in range(1, k):
        for i in range(0, k - distance):
            # i, j are data indexes for the categories being compared
            j = i + distance
            index = tests['pw_indexes'][(i, j)]
            stars = tests['stars'][index]
            if not stars:
                continue

            free_levels = np.flatnonzero(reservation[:, i:j].sum(1) == 0)
            level = free_levels.min()
            reservation[level, i:j] = 1
            connections.append((level, i, j, index, stars))

    # plan spatial distances
    used_levels = np.flatnonzero(reservation.sum(1))
    if len(used_levels) == 0:
        if top is None:
            return bottom + y_unit
        else:
            return top
    n_levels = used_levels.max() + 1
    n_steps = n_levels * 2 + 1 + bool(markers)
    if top is None:
        top = bottom + y_unit * n_steps
    else:
        y_unit = (top - bottom) / n_steps

    # draw connections
    for level, i, j, index, stars in connections:
        c = pwcolors[stars - 1]
        y1 = bottom + y_unit * (level * 2 + 1)
        y2 = y1 + y_unit
        x1 = pos[i] + .025
        x2 = pos[j] - .025
        ax.plot([x1, x1, x2, x2], [y1, y2, y2, y1], color=c)
        if markers:
            symbol = tests['symbols'][index]
            ax.text((x1 + x2) / 2, y2, symbol, color=c, size=font_size,
                    ha='center', va='center', clip_on=False)

    return top


def _mark_plot_1sample(  # Mark significance for one-sample test
        ax: matplotlib.axes.Axes,
        ct: Celltable,  # Data for the tests
        parametric: bool,  # Whether to perform parametric tests
        pos: Sequence[float],  # position of items on x axis
        bottom: float,  # Bottom of the space to use for the stars
        y_unit: float,  # Distance from bottom to stars
        popmean: float,
        corr: Union[str, None],
        trend: str,
        levels: Union[dict, bool] = True,
        pwcolors: Sequence = None,
        tail: int = 0,
) -> float:  # Top of space used on y axis 
    # tests
    if pwcolors is None:
        pwcolors = PAIRWISE_COLORS[1 - bool(trend):]
    # mod
    if parametric:
        ps = [test.TTestOneSample(d, popmean=popmean, tail=tail).p for d in ct.get_data()]
    else:
        raise NotImplementedError("nonparametric 1-sample test")
    ps_adjusted = test.mcp_adjust(ps, corr)
    stars = test.star(ps_adjusted, int, levels, trend)
    stars_str = test.star(ps_adjusted, str, levels, trend)
    font_size = mpl.rcParams['font.size'] * 1.5
    if any(stars):
        y_stars = bottom + 1.75 * y_unit
        for i, n_stars in enumerate(stars):
            if n_stars > 0:
                c = pwcolors[n_stars - 1]
                ax.text(pos[i], y_stars, stars_str[i], color=c, size=font_size, ha='center', va='center', clip_on=False)
        return bottom + 4. * y_unit
    else:
        return bottom


class PairwiseLegend(EelFigure):
    """Legend for colors used in pairwise comparisons

    Parameters
    ----------
    size
        Side length in inches of a virtual square containing each bar.
    trend
        Also include a bar for trends (*p* < .1).
    ...
        Also accepts :ref:`general-layout-parameters`.
    """
    def __init__(self, size: float = .3, trend: bool = False, **kwargs):
        i_start = 1 - bool(trend)
        levels = [.1, .05, .01, .001][i_start:]
        colors = PAIRWISE_COLORS[i_start:]

        # layout
        n_levels = len(levels)
        ax_h = n_levels * size
        y_unit = size / 5
        ax_aspect = 4 / n_levels
        layout = Layout(0, ax_aspect, ax_h, tight=False, **kwargs)
        EelFigure.__init__(self, None, layout)
        ax = self.figure.add_axes((0, 0, 1, 1), frameon=False)
        ax.set_axis_off()

        x1 = .1 * size
        x2 = .9 * size
        x = (x1, x1, x2, x2)
        x_text = 1.2 * size
        for i, level, color in zip(range(n_levels), levels, colors):
            y1 = y_unit * (i * 5 + 2)
            y2 = y1 + y_unit
            ax.plot(x, (y1, y2, y2, y1), color=color)
            label = "p<%s" % (str(level)[1:])
            ax.text(x_text, y1 + y_unit / 2, label, ha='left', va='center')

        ax.set_ylim(0, self._layout.h)
        ax.set_xlim(0, self._layout.w)
        self._show()


class _SimpleFigure(EelFigure):
    def __init__(self, data_desc, *args, **kwargs):
        layout = Layout(1, 1, 5, *args, **kwargs)
        EelFigure.__init__(self, data_desc, layout)
        self._ax = self._axes[0]

        # collector for handles for figure legend
        self._handles = []
        self._legend = None


class Boxplot(CategorialAxisMixin, YLimMixin, _SimpleFigure):
    r"""Boxplot for a continuous variable

    Parameters
    ----------
    y
        Dependent variable.
    x
        Category definition (draw one box for every cell in ``x``).
    match
        Match cases for a repeated measures design.
    sub
        Use a subset of the data.
    cells
        Cells to plot (optional). All entries have to be cells of ``x``). Can be
        used to change the order of the bars or plot only certain cells.
    bottom
        Lowest possible value on the y axis (default is 0 or slightly
        below the lowest value).
    top
        Set the upper x axis limit (default is to fit all the data).
    xlabel
        X-axis label. By default the label is inferred from the data.
    ylabel
        Y-axis label. By default the label is inferred from the data.
    xticks
        X-axis tick labels describing the categories.
        The default is to use the cell names from ``x``.
        Use list of labels or ``{cell: label}`` :class:`dict` for custom labels.
        None to plot no labels.
    xtick_delim
        Delimiter for x axis category descriptors (default is ``'\n'``,
        i.e. the level on each Factor of ``x`` on a separate line).
    test : bool | scalar
        ``True`` (default): perform pairwise tests; ``False``: no tests;
        scalar: 1-sample tests against this value.
    tail : 0 | 1 | -1
        Tailedness of the test (when testing against population mean).
    par : bool
        Use parametric test for pairwise comparisons (use non-parametric
        tests if False).
    trend : str
        Marker for a trend in pairwise comparisons.
    test_markers : bool
        For pairwise tests, plot markers indicating significance level
        (stars).
    corr : None | 'hochberg' | 'bonferroni' | 'holm'
        Method for multiple comparison correction (default 'hochberg').
    colors : bool | sequence | dict of matplitlib colors
        Matplotlib colors to use for boxes (True to use the module default;
        default is False, i.e. no colors).
    ds : Dataset
        If a Dataset is specified, all data-objects can be specified as
        names of Dataset variables
    label_fliers : bool
        Add labels to flier points (outliers); requires ``match`` to be
        specified.
    ...
        Also accepts :ref:`general-layout-parameters` and
        :meth:`~matplotlib.axes.Axes.boxplot` parameters.
    """
    def __init__(
            self,
            y: VarArg,
            x: CategorialArg = None,
            match: CategorialArg = None,
            sub: IndexArg = None,
            cells: Sequence[CellArg] = None,
            bottom: float = None,
            top: float = None,
            xlabel: Union[bool, str] = True,
            ylabel: Union[bool, str] = True,
            xticks: Union[bool, dict, Sequence[str]] = True,
            xtick_delim: str = '\n',
            test=True,
            tail=0,
            par=True,
            trend=False,
            test_markers=True,
            corr='Hochberg',
            colors=False,
            ds=None,
            label_fliers=False,
            **kwargs,
    ):
        # get data
        ct = Celltable(y, x, match, sub, cells, ds, asvar)
        if colors is False:
            styles = False
        else:
            styles = find_cell_styles(ct.x, colors, ct.cells)
        if label_fliers and ct.match is None:
            raise TypeError(f"label_fliers={label_fliers!r} without specifying the match parameter: match is needed to determine labels")
        if ct.x is None and test is True:
            test = 0.

        # sort out boxplot kwargs
        boxplot_args = {k: kwargs.pop(k) for k in BOXPLOT_KEYWORDS if k in kwargs}
        _SimpleFigure.__init__(self, frame_title(ct.y, ct.x), **kwargs)
        self._configure_axis_data('y', ct.y, ylabel)

        self._plot = p = _plt_boxplot(self._ax, ct, styles, bottom, top, test, tail, par, corr, trend, test_markers, label_fliers, boxplot_args)
        p.set_ylim(p.bottom, p.top)
        p.ax.set_xlim(p.left, p.right)

        CategorialAxisMixin.__init__(self, self._ax, 'x', self._layout, xlabel, ct.x, xticks, xtick_delim, p.pos, ct.cells)
        YLimMixin.__init__(self, (p,))
        self._show()


class Barplot(CategorialAxisMixin, YLimMixin, _SimpleFigure):
    r"""Barplot for a continuous variable

    Parameters
    ----------
    y : Var
        Dependent variable.
    x : categorial
        Model (Factor or Interaction).
    match : None | categorial
        Match cases for a repeated measures design.
    sub : index-array
        Use a subset of the data.
    cells : None | sequence of cells of x
        Cells to plot (optional). All entries have to be cells of ``x``). Can be
        used to change the order of the bars or plot only certain cells.
    test : bool | scalar
        ``True`` (default): perform pairwise tests; ``False``: no tests;
        scalar: 1-sample tests against this value.
    tail : 0 | 1 | -1
        Tailedness of the test (when testing against population mean).
    par : bool
        Use parametric test for pairwise comparisons (use non-parametric
        tests if False).
    corr : None | 'hochberg' | 'bonferroni' | 'holm'
        Method for multiple comparison correction (default 'hochberg').
    trend : str
        Marker for a trend in pairwise comparisons.
    test_markers : bool
        For pairwise tests, plot markers indicating significance level
        (stars).
    ylabel : str | None
        Y axis label (default is inferred from the data).
    error
        Measure of variability to plot. Examples:
        ``sem``: Standard error of the mean;
        ``2sem``: 2 standard error of the mean;
        ``ci``: 95% confidence interval;
        ``99%ci``: 99% confidence interval.
    pool_error : bool
        Pool the errors for the estimate of variability (default is True
        for related measures designs, False for others). See Loftus & Masson
        (1994).
    ec : matplotlib color
        Error bar color.
    xlabel : str | bool
        X axis label (default is ``x.name``).
    xticks : None | sequence of str | dict
        X-axis tick labels describing the categories.
        The default is to use the cell names from ``x``.
        Use list of labels or ``{cell: label}`` :class:`dict` for custom labels.
        None to plot no labels.
    xtick_delim : str
        Delimiter for x axis category descriptors (default is ``'\n'``,
        i.e. the level on each Factor of ``x`` on a separate line).
    colors : bool | dict | sequence of matplitlib colors
        Matplotlib colors to use for boxes (True to use the module default;
        default is False, i.e. no colors).
    bottom : scalar
        Lower end of the y axis (default is determined from the data).
    top : scalar
        Upper end of the y axis (default is determined from the data).
    origin : scalar
        Origin of the bars on the y-axis (the default is ``0``, or the visible
        point closest to it).
    pos : sequence of scalar
        Position of the bars on the x-axis (default is ``range(n_cells)``).
    width : scalar or sequence of scalar
        Width of the bars (deault 0.5).
    c : matplotlib color
        Bar color (ignored if colors is specified).
    edgec : matplotlib color
        Barplot edge color.
    ds : Dataset
        If a Dataset is specified, all data-objects can be specified as
        names of Dataset variables
    ...
        Also accepts :ref:`general-layout-parameters`.
    """
    def __init__(self, y, x=None, match=None, sub=None, cells=None, test=True, tail=0, par=True,
                 corr='Hochberg', trend=False, test_markers=True, ylabel=True,
                 error: str = 'sem', pool_error=None, ec='k', xlabel=True, xticks=True,
                 xtick_delim='\n', colors=False, bottom=None, top=None,
                 origin=None, pos=None, width=0.5, c='#0099FF', edgec=None, ds=None, **kwargs):
        ct = Celltable(y, x, match, sub, cells, ds, asvar)
        if colors is False:
            styles = False
        else:
            styles = find_cell_styles(ct.x, colors, ct.cells)
        if pool_error is None:
            pool_error = ct.all_within

        _SimpleFigure.__init__(self, frame_title(ct.y, ct.x), **kwargs)
        self._configure_axis_data('y', ct.y, ylabel)

        p = _plt_barplot(self._ax, ct, error, pool_error, styles, bottom, top, origin, pos, width, c, edgec, ec, test, tail, par, trend, corr, test_markers)
        p.set_ylim(p.bottom, p.top)
        p.ax.set_xlim(p.left, p.right)

        CategorialAxisMixin.__init__(self, self._ax, 'x', self._layout, xlabel, ct.x, xticks, xtick_delim, p.pos, ct.cells, p.origin)
        YLimMixin.__init__(self, (p,))
        self._show()


class BarplotHorizontal(XAxisMixin, CategorialAxisMixin, _SimpleFigure):
    r"""Horizontal barplot for a continuous variable

    For consistency with :class:`plot.Barplot`, ``y`` refers to the horizontal
    axis and ``x`` refers to the vertical (categorial) axis.

    Parameters
    ----------
    y : Var
        Dependent variable.
    x : categorial
        Model (Factor or Interaction).
    match : None | categorial
        Match cases for a repeated measures design.
    sub : index-array
        Use a subset of the data.
    cells : None | sequence of cells of x
        Cells to plot (optional). All entries have to be cells of ``x``). Can be
        used to change the order of the bars or plot only certain cells.
    test : bool | scalar
        ``True`` (default): perform pairwise tests; ``False``: no tests;
        scalar: 1-sample tests against this value.
    tail : 0 | 1 | -1
        Tailedness of the test (when testing against population mean).
    par : bool
        Use parametric test for pairwise comparisons (use non-parametric
        tests if False).
    corr : None | 'hochberg' | 'bonferroni' | 'holm'
        Method for multiple comparison correction (default 'hochberg').
    trend : str
        Marker for a trend in pairwise comparisons.
    test_markers : bool
        For pairwise tests, plot markers indicating significance level
        (stars).
    ylabel : str | None
        Y axis label (default is inferred from the data).
    error
        Measure of variability to plot. Examples:
        ``sem``: Standard error of the mean;
        ``2sem``: 2 standard error of the mean;
        ``ci``: 95% confidence interval;
        ``99%ci``: 99% confidence interval.
    pool_error : bool
        Pool the errors for the estimate of variability (default is True
        for related measures designs, False for others). See Loftus & Masson
        (1994).
    ec : matplotlib color
        Error bar color.
    xlabel : str | bool
        X axis label (default is ``x.name``).
    xticks : None | sequence of str | dict
        X-axis tick labels describing the categories.
        The default is to use the cell names from ``x``.
        Use list of labels or ``{cell: label}`` :class:`dict` for custom labels.
        None to plot no labels.
    xtick_delim : str
        Delimiter for x axis category descriptors (default ``' '``).
    hatch : bool | str
        Matplotlib Hatch pattern to fill boxes (True to use the module
        default; default is False).
    colors : bool | dict | sequence of matplitlib colors
        Matplotlib colors to use for boxes (True to use the module default;
        default is False, i.e. no colors).
    left : scalar
        Left end of the data axis (default is determined from the data).
    right : scalar
        Right end of the data axis (default is determined from the data).
    origin : scalar
        Origin of the bars on the data axis (the default is ``0``).
    pos : sequence of scalar
        Position of the bars on the x-axis (default is ``range(n_cells)``).
    width : scalar or sequence of scalar
        Width of the bars (deault 0.5).
    c : matplotlib color
        Bar color (ignored if colors is specified).
    edgec : matplotlib color
        Barplot edge color.
    ds : Dataset
        If a Dataset is specified, all data-objects can be specified as
        names of Dataset variables
    ...
        Also accepts :ref:`general-layout-parameters`.
    """
    def __init__(self, y, x=None, match=None, sub=None, cells=None, test=False, tail=0, par=True,
                 corr='Hochberg', trend=False, test_markers=True, ylabel=True,
                 error: str = 'sem', pool_error=None, ec='k', xlabel=True, xticks=True,
                 xtick_delim=' ', colors=False, bottom=0, top=None,
                 origin=None, pos=None, width=0.5, c='#0099FF', edgec=None, ds=None, **kwargs):
        if test is not False:
            raise NotImplemented("Horizontal barplot with pairwise significance")

        ct = Celltable(y, x, match, sub, cells, ds, asvar)
        if colors is False:
            styles = False
        else:
            styles = find_cell_styles(ct.x, colors, ct.cells)
        if pool_error is None:
            pool_error = ct.all_within

        _SimpleFigure.__init__(self, frame_title(ct.y, ct.x), **kwargs)

        p = _plt_barplot(self._ax, ct, error, pool_error, styles, bottom, top, origin, pos, width, c, edgec, ec, test, tail, par, trend, corr, test_markers, horizontal=True)
        p.ax.set_ylim(p.left, p.right)
        self._configure_axis_data('x', ct.y, ylabel)

        XAxisMixin.__init__(self, p.bottom, p.top, axes=[p.ax])
        CategorialAxisMixin.__init__(self, self._ax, 'y', self._layout, xlabel, ct.x, xticks, xtick_delim, p.pos, ct.cells, p.origin)
        self._show()


class _plt_uv_base:
    """Base for barplot and boxplot -- x is categorial, y is scalar"""

    def __init__(self, ax, ct, origin, pos, width, bottom, plot_max, top, test, tail, corr, par, trend, test_markers, horizontal=False):
        # pairwise tests
        y_unit = (plot_max - bottom) / 15
        if ct.x is None and test is True:
            test = 0.
        if test is True:
            if tail:
                raise ValueError(f"tail={tail} for pairwise test")
            y_top = _mark_plot_pairwise(ax, ct, par, pos, plot_max, y_unit, corr, trend, test_markers, top=top)
        elif (test is False) or (test is None):
            y_top = plot_max + y_unit
        else:
            ax.axhline(test, color='black')
            y_top = _mark_plot_1sample(ax, ct, par, pos, plot_max, y_unit, test, corr, trend, tail=tail)

        if top is not None:
            y_top = top
        elif origin is not None:
            y_top = max(y_top, origin)

        if np.isscalar(width):
            left_margin = right_margin = width
        else:
            left_margin = width[np.argmin(pos)]
            right_margin = width[np.argmax(pos)]
        self.left = min(pos) - left_margin
        self.right = max(pos) + right_margin
        self.origin = origin
        self.bottom = bottom
        self.top = y_top
        self.pos = pos
        self.horizontal = horizontal
        self.vmin, self.vmax = ax.get_ylim()
        self.ax = ax

    def set_ylim(self, bottom, top):
        if self.horizontal:
            self.ax.set_xlim(bottom, top)
            self.vmin, self.vmax = self.ax.get_xlim()
        else:
            self.ax.set_ylim(bottom, top)
            self.vmin, self.vmax = self.ax.get_ylim()


class _plt_boxplot(_plt_uv_base):
    """Boxplot"""

    def __init__(self, ax, ct, styles, bottom, top, test, tail, par, corr, trend, test_markers, label_fliers, boxplot_args):
        # determine ax lim
        if bottom is None:
            if np.min(ct.y.x) >= 0:
                bottom = 0
            else:
                d_min = np.min(ct.y.x)
                d_max = np.max(ct.y.x)
                d_range = d_max - d_min
                bottom = d_min - .05 * d_range

        # boxplot
        width = 0.5
        k = len(ct.cells)
        all_data = ct.get_data()
        box_data = [y.x for y in all_data]
        if 'positions' not in boxplot_args:
            boxplot_args['positions'] = np.arange(k)
        pos = boxplot_args['positions']
        self.boxplot = bp = ax.boxplot(box_data, **boxplot_args)

        # Now fill the boxes with desired colors
        if styles:
            for cell, box in zip(ct.cells, bp['boxes']):
                box_x = box.get_xdata()[:5]  # []
                box_y = box.get_ydata()[:5]  # []
                box_coords = list(zip(box_x, box_y))
                style = styles[cell]
                poly = mpl.patches.Polygon(box_coords, facecolor=style.color, hatch=style.hatch, zorder=-999)
                ax.add_patch(poly)
            for item in bp['medians']:
                item.set_color('black')

        # data labels
        if label_fliers:
            for cell, fliers in zip(ct.cells, bp['fliers']):
                xs, ys = fliers.get_data()
                if len(xs) == 0:
                    continue
                x = xs[0] + 0.25
                data = ct.data[cell]
                match = ct.match[ct.data_indexes[cell]]
                for y in set(ys):
                    indices = data.index(y)
                    label = ', '.join(cellname(match[i]) for i in indices)
                    ax.annotate(label, (x, y), va='center')

        # set ax limits
        plot_max = max(x.max() for x in all_data)
        _plt_uv_base.__init__(self, ax, ct, None, pos, width, bottom, plot_max, top, test, tail, corr, par, trend, test_markers)


class _plt_barplot(_plt_uv_base):
    "Barplot from Celltable ``ct``"
    def __init__(
            self,
            ax: mpl.axes.Axes,
            ct: Celltable,  # Data to plot.
            error: str,  # Variability description (e.g., "95%ci")
            pool_error: bool,  # for the variability estimate
            styles: dict = False,
            bottom: float = None,
            top: float = None,
            origin: float = None,
            pos: Sequence[float] = None,  # position of the bars
            width: Union[float, Sequence[float]] = .5,  # width of the bars
            c='#0099FF',
            edgec=None,
            ec='k',
            test: bool = True,
            tail: int = 0,
            par=True,
            trend: Union[bool, str] = False,
            corr='Hochberg',
            test_markers=True,
            horizontal: bool = False,
    ):
        # data means
        k = len(ct.cells)
        if pos is None:
            pos = np.arange(k)
        else:
            pos = np.asarray(pos)
        if horizontal:
            pos = -pos
        height = np.array(ct.get_statistic(np.mean))

        # origin
        if origin is None:
            if bottom and bottom > 0:
                origin = bottom
            elif top and top < 0:
                origin = top
            else:
                origin = 0

        # error bars
        if ct.x is None:
            error_match = None
        else:
            error_match = ct.match
        error_bars = stats.variability(ct.y.x, ct.x, error_match, error, pool_error, ct.cells)

        # fig spacing
        plot_max = np.max(height + error_bars)
        plot_min = np.min(height - error_bars)
        plot_span = plot_max - plot_min
        if bottom is None:
            bottom = min(plot_min - plot_span * .05, origin)

        # main BARPLOT
        if horizontal:
            bars = ax.barh(pos, height - origin, width, origin, color=c, edgecolor=edgec, ecolor=ec, xerr=error_bars)
        else:
            bars = ax.bar(pos, height - origin, width, origin, color=c, edgecolor=edgec, ecolor=ec, yerr=error_bars)

        # prevent bars from clipping
        for artist in chain(bars.patches, *bars.errorbar.lines[1:]):
            artist.set_clip_on(False)

        if styles:
            for cell, bar, in zip(ct.cells, bars):
                style = styles[cell]
                bar.set_facecolor(style.color)
                if style.hatch:
                    bar.set_hatch(style.hatch)

        _plt_uv_base.__init__(self, ax, ct, origin, pos, width, bottom, plot_max, top, test, tail, corr, par, trend, test_markers, horizontal)


class Timeplot(LegendMixin, YLimMixin, EelFigure):
    """Plot a variable over time

    Parameters
    ----------
    y
        Dependent variable.
    time
        Variable assigning the time to each case.
    categories
        Plot ``y`` separately for different categories.
    match
        Match cases for a repeated measures design.
    sub
        Use a subset of the data.
    ds
        If a Dataset is specified, all data-objects can be specified as
        names of Dataset variables
    main : numpy function
        draw lines to connect values across time (default: np.mean).
        Can be 'bar' for barplots or False.
    error
        How to indicate estimate error. For complete within-subject designs,
        the within-subject measures are displayed (see Loftus & Masson, 1994).
        Options:
        'box': boxplots;
        '[x]sem': x standard error of the means (e.g. 'sem', '2sem');
        '[x]std': x standard deviations.
    x_jitter : bool
        When plotting error bars, jitter their location on the x-axis to
        increase readability.
    bottom : scalar
        Lower end of the y axis (default is 0).
    top : scalar
        Upper end of the y axis (default is determined from the data).
    xlabel
        X-axis label. By default the label is inferred from the data.
    ylabel
        Y-axis label. By default the label is inferred from the data.
    timelabels : sequence | dict | 'all'
        Labels for the x (time) axis. Exact labels can be specified in the form 
        of a list of labels corresponsing to all unique values of ``time``, or a 
        ``{time_value: label}`` dictionary. For 'all', all values of ``time`` 
        are marked. The default is normal matplotlib ticks.
    legend : str | int | 'fig' | None
        Matplotlib figure legend location argument or 'fig' to plot the
        legend in a separate figure.
    labels : dict
        Alternative labels for legend as ``{cell: label}`` dictionary (preserves
        order).
    colors : str | list | dict
        Colors for the categories.
        **str**: A colormap name; cells are mapped onto the colormap in
        regular intervals.
        **list**: A list of colors in the same sequence as the cells.
        **dict**: A dictionary mapping each cell to a color.
        Colors are specified as `matplotlib compatible color arguments
        <http://matplotlib.org/api/colors_api.html>`_.
    ...
        Also accepts :ref:`general-layout-parameters`.
    """
    def __init__(
            self,
            y: VarArg,
            time: UVArg,
            categories: CategorialArg = None,
            match: CategorialArg = None,
            sub: IndexArg = None,
            ds: Dataset = None,
            # data plotting
            main: Callable = np.mean,
            error: str = 'sem',
            x_jitter: bool = False,
            bottom: float = None,
            top: float = None,
            # labelling
            xlabel: Union[bool, str] = True,
            ylabel: Union[bool, str] = True,
            timelabels: Union[Sequence, Dict, str] = None,
            legend: Union[str, int, bool] = 'upper right',
            labels: Dict = None,
            colors: ColorsArg = None,
            **kwargs,
    ):
        sub, n = assub(sub, ds, return_n=True)
        y, n = asvar(y, sub, ds, n, return_n=True)
        x = asuv(time, sub, ds, n)
        if categories is None:
            legend = False
        else:
            categories = ascategorial(categories, sub, ds, n)
        if match is not None:
            match = ascategorial(match, sub, ds, n)

        # transform to 3 kwargs:
        # - local_plot ('bar' or 'box')
        # - line_plot (function for values to connect)
        # - error
        if main == 'bar':
            assert error != 'box'
            local_plot = 'bar'
            line_plot = None
        else:
            line_plot = main
            if error == 'box':
                local_plot = 'box'
                error = None
            else:
                local_plot = None

        if not line_plot:
            legend = False

        styles = find_cell_styles(categories, colors)

        # get axes
        layout = Layout(1, 1, 5, **kwargs)
        EelFigure.__init__(self, frame_title(y, categories), layout)
        self._configure_axis_data('y', y, ylabel)
        self._configure_axis_data('x', x, xlabel)

        plot = _ax_timeplot(self._axes[0], y, categories, x, match, styles, line_plot, error, local_plot, timelabels, x_jitter, bottom, top)

        YLimMixin.__init__(self, (plot,))
        LegendMixin.__init__(self, legend, plot.legend_handles, labels)
        self._show()

    def _fill_toolbar(self, tb):
        LegendMixin._fill_toolbar(self, tb)


class _ax_timeplot:

    def __init__(self, ax, y, categories, time, match, styles, line_plot, error, local_plot, timelabels, x_jitter, bottom, top):
        # categories
        n_cat = 1 if categories is None else len(categories.cells)
        # find time points
        time_points = np.unique(time.x)
        # n_time_points = len(time_points)
        # determine whether spread can be plotted
        celltables = [Celltable(y, categories, match=match, sub=(time == t)) for
                      t in time_points]
        line_values = np.array([ct.get_statistic(line_plot) for ct in celltables]).T
        # all_within = all(ct.all_within for ct in celltables)
        if error and all(ct.n_cases > ct.n_cells for ct in celltables):
            spread_values = np.array([ct.variability(error) for ct in celltables]).T
        else:
            error = spread_values = False

        time_step = min(np.diff(time_points))
        if local_plot in ['box', 'bar']:
            within_spacing = time_step / (2 * n_cat)
            padding = (2 + n_cat / 2) * within_spacing
        else:
            within_spacing = time_step / (8 * n_cat)
            padding = time_step / 4  # (2 + n_cat/2) * within_spacing

        rel_pos = np.arange(0, n_cat * within_spacing, within_spacing)
        rel_pos -= np.mean(rel_pos)

        t_min = min(time_points) - padding
        t_max = max(time_points) + padding

        # local plots
        for t, ct in zip(time_points, celltables):
            pos = rel_pos + t
            if local_plot == 'box':
                # boxplot
                bp = ax.boxplot(ct.get_data(out=list), positions=pos, widths=within_spacing)
                # make outlines black
                for lines in bp.values():
                    setp(lines, color='black')
                # Now fill the boxes with desired colors
                for cell, box in enumerate(ct.cells, bp['boxes']):
                    box_x = box.get_xdata()[:5]
                    box_y = box.get_ydata()[:5]
                    style = styles[cell]
                    patch = mpl.patches.Polygon(zip(box_x, box_y), zorder=-999, **style.patch_args)
                    ax.add_patch(patch)
            elif local_plot == 'bar':
                _plt_barplot(ax, ct, error, False, styles, 0, pos=pos, width=within_spacing, test=False)

        legend_handles = {}
        if line_plot:
            # plot means
            x = time_points
            cells = [None] if categories is None else categories.cells
            for i, cell in enumerate(cells):
                y = line_values[i]
                name = cellname(cell)
                style = styles[cell]
                kwargs = {**style.line_args, 'zorder': 6}
                handles = ax.plot(x, y, label=name, **kwargs)
                legend_handles[cell] = handles[0]

                if error:
                    if x_jitter:
                        x_errbars = x + rel_pos[i]
                    else:
                        x_errbars = x
                    ax.errorbar(x_errbars, y, yerr=spread_values[i], fmt='none', zorder=5, ecolor=style.color, label=name)

        # x-ticks
        if timelabels is not None:
            if isinstance(timelabels, dict):
                locations = [t for t in time_points if t in timelabels]
                labels = [timelabels[t] for t in locations]
            elif isinstance(timelabels, str):
                if timelabels == 'all':
                    locations = time_points
                    labels = None
                else:
                    raise ValueError("timelabels=%r" % (timelabels,))
            elif (not isinstance(timelabels, Sequence) or
                  not len(timelabels) == len(time_points)):
                raise TypeError(f"timelabels={timelabels}; needs to be a sequence whose length equals the number of time points ({len(time_points)})")
            else:
                locations = time_points
                labels = [str(l) for l in timelabels]
            ax.set_xticks(locations)
            if labels is not None:
                ax.set_xticklabels(labels)

        # data-limits
        data_max = line_values.max()
        data_min = line_values.min()
        if error:
            max_spread = max(spread_values.max(), -spread_values.min())
            data_max += max_spread
            data_min -= max_spread
        pad = (data_max - data_min) / 20.
        if bottom is None:
            bottom = data_min - pad
        if top is None:
            top = data_max + pad

        # finalize
        ax.set_xlim(t_min, t_max)
        self.ax = ax
        self.legend_handles = legend_handles
        self.set_ylim(bottom, top)

    def set_ylim(self, vmin, vmax):
        self.ax.set_ylim(vmin, vmax)
        self.vmin, self.vmax = self.ax.get_ylim()


def _reg_line(y, reg):
    coeff = np.hstack([np.ones((len(reg), 1)), reg[:, None]])
    (a, b), residues, rank, s = scipy.linalg.lstsq(coeff, y)
    regline_x = np.array([min(reg), max(reg)])
    regline_y = a + b * regline_x
    return regline_x, regline_y


class Scatter(EelFigure, LegendMixin, ColorBarMixin):
    """Scatter-plot

    Parameters
    ----------
    y
        Variable for the y-axis.
    x
        Variable for the x-axis.
    color
        Plot the correlation separately for different categories.
    size
        Size of the markers.
    sub
        Use a subset of the data.
    ds
        If a Dataset is specified, all data-objects can be specified as
        names of Dataset variables
    colors
        If ``color`` is continuous, a colormap to assign color to values. If
        ``color`` is discrete, a dictionary of colors for values in ``color``.
    vmin
        Lower bound of the colormap.
    vmax
        Upper bound of the colormap.
    markers
        Marker shape (see :mod:`matplotlib.markers`).
    legend
        Matplotlib figure legend location argument, or ``'fig'`` to plot the
        legend in a separate figure.
    labels
        Alternative labels for legend as ``{cell: label}`` dictionary (preserves
        order).
    xlabel
        Labels for x-axis; the default is determined from the data.
    ylabel
        Labels for y-axis; the default is determined from the data.
    ...
        Also accepts :ref:`general-layout-parameters`.
    """
    def __init__(
            self,
            y: VarArg,
            x: VarArg,
            color: Union[CategorialArg, Var] = None,
            size: Union[VarArg, float] = None,
            sub: IndexArg = None,
            ds: Dataset = None,
            colors: Union[dict, str] = None,
            vmin: str = None,
            vmax: str = None,
            markers: str = None,
            legend: Union[str, int, bool] = 'upper right',
            labels: dict = None,
            alpha: float = 1.,
            xlabel: Union[bool, str] = True,
            ylabel: Union[bool, str] = True,
            **kwargs):
        sub, n = assub(sub, ds, return_n=True)
        y, n = asvar(y, sub, ds, n, return_n=True)
        x = asvar(x, sub, ds, n)

        # colors
        cmap = color_obj = color_data = cat = styles = None
        if color is not None:
            color = asuv(color, sub, ds, n, interaction=True)
            if isinstance(color, Var) and not isinstance(colors, dict):
                color_obj = color
                color_data = color.x
                cmap = colors
            else:
                cat = color
                styles = find_cell_styles(color, colors)

        # size
        if size is not None:
            size = asvar(size, sub, ds, n).x

        # figure
        layout = Layout(1, 1, 5, autoscale=True, **kwargs)
        EelFigure.__init__(self, frame_title(y, x), layout)
        self._configure_axis_data('y', y, ylabel)
        self._configure_axis_data('x', x, xlabel)

        ax = self._axes[0]
        legend_handles = {}
        if cat is None:
            legend = False
            mappable = ax.scatter(x.x, y.x, size, color_data, markers, cmap, vmin=vmin, vmax=vmax, alpha=alpha)
        else:
            mappable = None
            for cell in cat.cells:
                label = cellname(cell)
                idx = (cat == cell)
                size_i = size[idx] if isinstance(size, np.ndarray) else size
                legend_handles[label] = ax.scatter(x.x[idx], y.x[idx], size_i, styles[cell].color, markers, alpha=alpha, label=label)

        LegendMixin.__init__(self, legend, legend_handles, labels)
        ColorBarMixin.__init__(self, data=color_obj, mappable=mappable)
        self._n_cases = n
        self._show()

    def _fill_toolbar(self, tb):
        LegendMixin._fill_toolbar(self, tb)
        ColorBarMixin._fill_toolbar(self, tb)


class Regression(EelFigure, LegendMixin):
    """Plot the regression of ``y`` on ``x``

    parameters
    ----------
    y
        Variable for the y-axis.
    x
        Variable for the x-axis.
    cat
        Plot the regression separately for different categories.
    match
        Match cases for a repeated measures design.
    sub
        Use a subset of the data.
    ds
        If a Dataset is specified, all data-objects can be specified as
        names of Dataset variables
    xlabel
        X-axis label. By default the label is inferred from the data.
    ylabel
        Y-axis label. By default the label is inferred from the data.
    alpha
        alpha for individual data points (to control visualization of
        overlap)
    legend
        Matplotlib figure legend location argument or 'fig' to plot the
        legend in a separate figure.
    labels
        Alternative labels for legend as ``{cell: label}`` dictionary (preserves
        order).
    c : color | sequence of colors
        Colors.
    tight : bool
        Use matplotlib's tight_layout to expand all axes to fill the figure
        (default True)
    ...
        Also accepts :ref:`general-layout-parameters`.
    """
    def __init__(
            self,
            y: VarArg,
            x: VarArg,
            cat: CategorialArg = None,
            match: CategorialArg = None,
            sub: IndexArg = None,
            ds: Dataset = None,
            xlabel: Union[bool, str] = True,
            ylabel: Union[bool, str] = True,
            alpha: float = .2,
            legend: Union[str, int, bool] = 'upper right',
            labels: dict = None,
            c: Any = ('#009CFF', '#FF7D26', '#54AF3A', '#FE58C6', '#20F2C3'),
            **kwargs):
        sub, n = assub(sub, ds, return_n=True)
        y, n = asvar(y, sub, ds, n, return_n=True)
        x = asvar(x, sub, ds, n)
        if cat is not None:
            cat = ascategorial(cat, sub, ds, n)
        if match is not None:
            raise NotImplementedError("match kwarg")

        if ylabel is True:
            ylabel = y.name

        # figure
        layout = Layout(1, 1, 5, autoscale=True, **kwargs)
        EelFigure.__init__(self, frame_title(y, x, cat), layout)
        self._configure_axis_data('x', x, xlabel)
        self._configure_axis_data('y', y, ylabel)

        ax = self._axes[0]
        legend_handles = {}
        if cat is None:
            legend = False
            if type(c) in [list, tuple]:
                color = c[0]
            else:
                color = c
            ax.scatter(x.x, y.x, edgecolor=color, facecolor=color, s=100,
                       alpha=alpha, marker='o', label='_nolegend_')
            reg_x, reg_y = _reg_line(y.x, x.x)
            ax.plot(reg_x, reg_y, c=color)
        else:
            for i, cell in enumerate(cat.cells):
                idx = (cat == cell)
                # scatter
                y_i = y.x[idx]
                x_i = x.x[idx]
                color = c[i % len(c)]
                h = ax.scatter(x_i, y_i, edgecolor=color, facecolor=color, s=100,
                               alpha=alpha, marker='o', label='_nolegend_')
                legend_handles[cell] = h
                # regression line
                reg_x, reg_y = _reg_line(y_i, x_i)
                ax.plot(reg_x, reg_y, c=color, label=cellname(cell))

        LegendMixin.__init__(self, legend, legend_handles, labels)
        self._show()

    def _fill_toolbar(self, tb):
        LegendMixin._fill_toolbar(self, tb)


# MARK: Requirements for Statistical Tests

def _difference(data, names):
    "Data condition x subject"
    data_differences = []; diffnames = []; diffnames_2lines = []
    for i, (name1, data1) in enumerate(zip(names, data)):
        for name2, data2 in zip(names[i + 1:], data[i + 1:]):
            data_differences.append(data1 - data2)
            diffnames.append('-'.join([name1, name2]))
            diffnames_2lines.append('-\n'.join([name1, name2]))
    return data_differences, diffnames, diffnames_2lines


def _ax_histogram(ax, data, density, test_normality, **kwargs):
    """Create normality test figure"""
    n, bins, patches = ax.hist(data, density=density, **kwargs)

    if test_normality:
        # normal line
        mu = np.mean(data)
        sigma = np.std(data)
        y = scipy.stats.norm.pdf(bins, mu, sigma)
        if not density:
            y *= len(data) * np.diff(bins)[0]
        ax.plot(bins, y, 'r--', linewidth=1)

        # TESTS
        # test Anderson
        a2, thresh, sig = scipy.stats.morestats.anderson(data)
        index = sum(a2 >= thresh)
        if index > 0:
            ax.text(.95, .95, '$^{*}%s$' % str(sig[index - 1] / 100), color='r', size=11,
                    horizontalalignment='right',
                    verticalalignment='top',
                    transform=ax.transAxes,)
        logging.debug(" Anderson: %s, %s, %s" % (a2, thresh, sig))
        # test Lilliefors
        n_test = test.lilliefors(data)
        ax.set_xlabel(r"$D=%.3f$, $p_{est}=%.2f$" % n_test)  # \chi ^{2}

    # finalize axes
    ax.autoscale()


class Histogram(EelFigure):
    """
    Histogram plots with tests of normality

    Parameters
    ----------
    Y : Var
        Dependent variable.
    x : categorial
        Categories for separate histograms.
    match : None | categorial
        Match cases for a repeated measures design.
    sub : index-array
        Use a subset of the data.
    ds : Dataset
        If a Dataset is specified, all data-objects can be specified as
        names of Dataset variables
    pooled : bool
        Add one plot with all values/differences pooled.
    density : bool
        Norm counts to approximate a probability density (default False).
    test : bool
        Test for normality.
    tight : bool
        Use matplotlib's tight_layout to expand all axes to fill the figure
        (default True)
    bins : str | int | array
        Histogram bins, specified either as arry of bin edges or as ``bins``
        parameter for :func:`numpy.histogram_bin_edges`).
    ...
        Also accepts :ref:`general-layout-parameters`.
    """
    def __init__(self, y, x=None, match=None, sub=None, ds=None, pooled=True,
                 density=False, test=False, tight=True, title=None, xlabel=True,
                 bins=None, **kwargs):
        ct = Celltable(y, x, match=match, sub=sub, ds=ds, coercion=asvar)

        # layout
        if x is None:
            nax = 1
            if title is True:
                title = "Test for Normality" if test else "Histogram"
        elif ct.all_within:
            n_comp = len(ct.cells) - 1
            nax = n_comp ** 2
            kwargs['nrow'] = n_comp
            kwargs['ncol'] = n_comp
            self._make_axes = False
            self._default_ylabel_ax = -1
            if title is True:
                if test:
                    title = "Tests for Normality of the Differences"
                else:
                    title = "Histogram of Pairwise Difference"
        else:
            nax = len(ct.cells)
            if title is True:
                title = "Tests for Normality" if test else "Histogram"

        layout = Layout(nax, 1, 3, tight, title, **kwargs)
        EelFigure.__init__(self, frame_title(ct.y, ct.x), layout)

        if bins is None:
            bins = 'auto'
            if ct.y.x.dtype.kind == 'i':
                if ct.y.max() - ct.y.min() < len(ct.y.x):
                    bins = 'int'
        if isinstance(bins, (str, int)):
            if bins == 'int':
                bins = np.arange(ct.y.min() - 0.5, ct.y.max() + 1, 1)
            else:
                bins = np.histogram_bin_edges(ct.y.x, bins)

        if x is None:
            _ax_histogram(self._axes[0], ct.y.x, density, test, bins=bins)
        elif ct.all_within:  # distribution of differences
            data = [v.x for v in ct.get_data()]
            names = ct.cellnames()

            pooled_data = []
            # i: row
            # j: -column
            for i in range(n_comp + 1):
                for j in range(i + 1, n_comp + 1):
                    difference = data[i] - data[j]
                    pooled_data.append(difference)
                    ax_i = n_comp * i + (n_comp + 1 - j)
                    ax = self.figure.add_subplot(n_comp, n_comp, ax_i)
                    self._axes.append(ax)
                    _ax_histogram(ax, difference, density, test, bins=bins)
                    if i == 0:
                        ax.set_title(names[j], size=12)
                    if j == n_comp:
                        ax.set_ylabel(names[i], size=12)
            pooled_data = np.hstack(pooled_data)
            # pooled diffs
            if pooled and len(names) > 2:
                ax = self.figure.add_subplot(n_comp, n_comp, n_comp ** 2)
                self._axes.append(ax)
                _ax_histogram(ax, pooled_data, density, test, facecolor='g', bins=bins)
                ax.set_title("Pooled Differences")
        else:  # independent measures
            for cell, ax in zip(ct.cells, self._axes):
                ax.set_title(cellname(cell))
                _ax_histogram(ax, ct.data[cell].x, density, test, bins=bins)

        if test:
            self.figure.text(.99, .01, "$^{*}$ Anderson and Darling test "
                             "thresholded at $[.15, .10, .05, .025, .01]$.",
                             color='r', verticalalignment='bottom',
                             horizontalalignment='right')
            xlabel = False  # xlabel is used for test result

        if density:
            self._configure_axis_data('y', 'p', 'probability density')
        else:
            self._configure_axis_data('y', 'n', 'count')
        self._configure_axis_data('x', ct.y, xlabel)
        self._show()


def boxcox_explore(y, params=[-1, -.5, 0, .5, 1], crange=False, ax=None, box=True):
    """
    Plot the distribution resulting from a Box-Cox transformation

    Parameters
    ----------
    y : array-like
        array containing data whose distribution is to be examined
    crange :
        correct range of transformed data
    ax :
        ax to plot to (``None`` creates a new figure)
    box :
        use Box-Cox family

    """
    if hasattr(y, 'x'):
        y = y.x
    else:
        y = np.ravel(y)

    if np.any(y == 0):
        raise ValueError("data contains 0")

    y = []
    for p in params:
        if p == 0:
            if box:
                xi = np.log(y)
            else:
                xi = np.log10(y)
                # xi = np.log1p(x)
        else:
            if box:
                xi = (y ** p - 1) / p
            else:
                xi = y ** p
        if crange:
            xi -= min(xi)
            xi /= max(xi)
        y.append(xi)

    if not ax:
        import matplotlib.pyplot as plt
        plt.figure()
        ax = plt.subplot(111)

    ax.boxplot(y)
    ax.set_xticks(np.arange(1, 1 + len(params)))
    ax.set_xticklabels(params)
    ax.set_xlabel("p")
    if crange:
        ax.set_ylabel("Value (Range Corrected)")
