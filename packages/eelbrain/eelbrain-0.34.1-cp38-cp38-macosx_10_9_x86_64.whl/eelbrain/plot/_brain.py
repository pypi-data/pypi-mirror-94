# Author: Christian Brodbeck <christianbrodbeck@nyu.edu>
from dataclasses import dataclass
from enum import Enum
from functools import partial
from itertools import product
from numbers import Number
from typing import Any, Sequence, Union

import matplotlib
import mne
from nibabel.freesurfer import read_annot
import numpy as np

from .._data_obj import NDVar, SourceSpace
from .._stats.testnd import NDTest, NDDifferenceTest, MultiEffectNDTest
from .._utils import deprecated
from ..fmtxt import im_table
from .._text import ms, ms_window
from ._base import EelFigure, ImLayout, ColorBarMixin, brain_data, butterfly_data, use_inline_backend
from ._color_luts import dspm_lut, p_lut
from ._colors import ColorList
from ._utsnd import Butterfly


def assert_can_save_movies():
    from ._brain_object import assert_can_save_movies
    assert_can_save_movies()


def annot(annot, subject='fsaverage', surf='smoothwm', borders=False, alpha=0.7,
          hemi=None, views=('lat', 'med'), w=None, h=None, axw=None, axh=None,
          foreground=None, background=None, parallel=True, cortex='classic',
          title=None, subjects_dir=None, name=None):
    """Plot the parcellation in an annotation file

    Parameters
    ----------
    annot : str
        Name of the annotation (e.g., "PALS_B12_LOBES").
    subject : str
        Name of the subject (default 'fsaverage').
    surf : 'inflated' | 'pial' | 'smoothwm' | 'sphere' | 'white'
        Freesurfer surface to use as brain geometry.
    borders : bool | int
        Show only label borders (PySurfer Brain.add_annotation() argument).
    alpha : scalar
        Alpha of the annotation (1=opaque, 0=transparent, default 0.7).
    hemi : 'lh' | 'rh' | 'both' | 'split'
        Which hemispheres to plot (default includes hemisphere with more than one
        label in the annot file).
    views : str | sequence of str
        One or several views to show in the figure. The options are:
        ``'lateral', 'medial', 'ventral', 'dorsal', 'rostral', 'parietal',
        'frontal', 'caudal'``.
    w, h, axw, axh : scalar
        Layout parameters (figure width/height, subplot width/height).
    foreground : mayavi color
        Figure foreground color (i.e., the text color).
    background : mayavi color
        Figure background color.
    parallel : bool
        Set views to parallel projection (default ``True``).
    cortex : str | tuple | dict
        Mark gyri and sulci on the cortex. Presets: ``'classic'`` (default), 
        ``'high_contrast'``, ``'low_contrast'``, ``'bone'``. Can also be a 
        single color (e.g. ``'red'``, ``(0.1, 0.4, 1.)``) or a tuple of two 
        colors for gyri and sulci (e.g. ``['red', 'blue']`` or ``[(1, 0, 0), 
        (0, 0, 1)]``). For all options see the PySurfer documentation.
    title : str
        title for the window (default is the parcellation name).
    subjects_dir : None | str
        Override the default subjects_dir.
    name : str
        Equivalent to ``title``, for consistency with other plotting functions. 

    Returns
    -------
    brain : surfer.Brain
        PySurfer Brain instance.

    Notes
    -----
    The ``Brain`` object that is returned has a
    :meth:`~plot._brain_fixes.plot_legend` method to plot the color legend.

    See Also
    --------
    eelbrain.plot.brain.annot_legend : plot a corresponding legend without the brain
    """
    if hemi is None:
        annot_lh = mne.read_labels_from_annot(subject, annot, 'lh',
                                              subjects_dir=subjects_dir)
        use_lh = len(annot_lh) > 1
        annot_rh = mne.read_labels_from_annot(subject, annot, 'rh',
                                              subjects_dir=subjects_dir)
        use_rh = len(annot_rh) > 1
        if use_lh and use_rh:
            hemi = 'split'
        elif use_lh:
            hemi = 'lh'
        elif use_rh:
            hemi = 'rh'
        else:
            raise ValueError("Neither hemisphere contains more than one label")

    if title is None:
        title = '%s - %s' % (subject, annot)

    from ._brain_object import Brain
    brain = Brain(subject, hemi, surf, title, cortex,
                  views=views, w=w, h=h, axw=axw, axh=axh,
                  foreground=foreground, background=background,
                  subjects_dir=subjects_dir, name=name)

    brain._set_annot(annot, borders, alpha)
    if parallel:
        brain.set_parallel_view(scale=True)
    return brain


def annot_legend(lh, rh, *args, **kwargs):
    """Plot a legend for a freesurfer parcellation

    Parameters
    ----------
    lh : str
        Path to the lh annot-file.
    rh : str
        Path to the rh annot-file.
    labels : dict (optional)
        Alternative (text) label for (brain) labels.
    h : 'auto' | scalar
        Height of the figure in inches. If 'auto' (default), the height is
        automatically increased to fit all labels.

    Returns
    -------
    legend : :class:`~eelbrain.plot.ColorList`
        Figure with legend for the parcellation.

    Notes
    -----
    Instead of :func:`~eelbrain.plot.brain.annot_legend` it is usually
    easier to use::

    >>> brain = plot.brain.annoot(annot, ...)
    >>> legend = brain.plot_legend()

    See Also
    --------
    eelbrain.plot.brain.annot : plot the parcellation on a brain model
    """
    _, lh_colors, lh_names = read_annot(lh)
    _, rh_colors, rh_names = read_annot(rh)
    lh_names = [name.decode() for name in lh_names]
    rh_names = [name.decode() for name in rh_names]
    lh_colors = dict(zip(lh_names, lh_colors[:, :4] / 255.))
    rh_colors = dict(zip(rh_names, rh_colors[:, :4] / 255.))
    names = set(lh_names)
    names.update(rh_names)
    colors = {}
    seq = []  # sequential order in legend
    seq_lh = []
    seq_rh = []
    for name in names:
        if name in lh_colors and name in rh_colors:
            if np.array_equal(lh_colors[name], rh_colors[name]):
                colors[name] = lh_colors[name]
                seq.append(name)
            else:
                colors[name + '-lh'] = lh_colors[name]
                colors[name + '-rh'] = rh_colors[name]
                seq_lh.append(name + '-lh')
                seq_rh.append(name + '-rh')
        elif name in lh_colors:
            colors[name + '-lh'] = lh_colors[name]
            seq_lh.append(name + '-lh')
        else:
            colors[name + '-rh'] = rh_colors[name]
            seq_rh.append(name + '-rh')
    return ColorList(colors, seq + seq_lh + seq_rh, *args, **kwargs)


def _plot(data, *args, **kwargs):
    "Plot depending on source space kind"
    if data.source.kind == 'vol':
        return _voxel_brain(data, *args, **kwargs)
    else:
        return brain(data, *args, **kwargs)


def dspm(src, fmin=13, fmax=22, fmid=None, *args, **kwargs):
    """
    Plot a source estimate with coloring for dSPM values (bipolar).

    Parameters
    ----------
    src : NDVar, dims = ([case,] source, [time])
        NDVar with SourceSpace dimension. If stc contains a case dimension,
        the average across cases is taken.
    fmin, fmax : scalar >= 0
        Start- and end-point for the color gradient for positive values. The
        gradient for negative values goes from -fmin to -fmax. Values between
        -fmin and fmin are transparent.
    fmid : None | scalar
        Midpoint for the color gradient. If fmid is None (default) it is set
        half way between fmin and fmax.
    surf : 'inflated' | 'pial' | 'smoothwm' | 'sphere' | 'white'
        Freesurfer surface to use as brain geometry.
    views : str | sequence of str
        One or several views to show in the figure. The options are:
        ``'lateral', 'medial', 'ventral', 'dorsal', 'rostral', 'parietal',
        'frontal', 'caudal'``.
    hemi : 'lh' | 'rh' | 'both' | 'split'
        Which hemispheres to plot (default based on data).
    colorbar : bool
        Add a colorbar to the figure (use ``.plot_colorbar()`` to plot a
        colorbar separately).
    time_label : str
        Label to show time point. Use ``'ms'`` or ``'s'`` to display time in
        milliseconds or in seconds, or supply a custom format string to format
        time values (in seconds; default is ``'ms'``).
    w, h, axw, axh : scalar
        Layout parameters (figure width/height, subplot width/height).
    foreground : mayavi color
        Figure foreground color (i.e., the text color).
    background : mayavi color
        Figure background color.
    parallel : bool
        Set views to parallel projection (default ``True``).
    cortex : str | tuple | dict
        Mark gyri and sulci on the cortex. Presets: ``'classic'`` (default), 
        ``'high_contrast'``, ``'low_contrast'``, ``'bone'``. Can also be a 
        single color (e.g. ``'red'``, ``(0.1, 0.4, 1.)``) or a tuple of two 
        colors for gyri and sulci (e.g. ``['red', 'blue']`` or ``[(1, 0, 0), 
        (0, 0, 1)]``). For all options see the PySurfer documentation.
    title : str
        title for the window (default is the subject name).
    smoothing_steps : None | int
        Number of smoothing steps if data is spatially undersampled (pysurfer
        ``Brain.add_data()`` argument).
    mask : bool | matplotlib color
        Shade areas that are not in ``src``. Can be matplotlib color, including
        alpha (e.g., ``(1, 1, 1, 0.5)`` for semi-transparent white).
    subjects_dir : None | str
        Override the subjects_dir associated with the source space dimension.
    name : str
        Equivalent to ``title``, for consistency with other plotting functions. 

    Returns
    -------
    brain : surfer.Brain
        PySurfer Brain instance containing the plot.
    """
    if fmid is None:
        fmid = (fmax + fmin) / 2
    lut = dspm_lut(fmin, fmid, fmax)
    return _plot(src, lut, -fmax, fmax, *args, **kwargs)


def p_map(p_map, param_map=None, p0=0.05, p1=0.01, p0alpha=0.5, *args,
          **kwargs):
    """Plot a map of p-values in source space.

    Parameters
    ----------
    p_map : NDVar | NDTest
        Map of p values, or test result.
    param_map : NDVar
        Statistical parameter covering the same data points as p_map. Only the
        sign is used, for incorporating the directionality of the effect into
        the plot.
    p0 : scalar
        Highest p-value that is visible.
    p1 : scalar
        P-value where the colormap changes from ramping alpha to ramping color.
    p0alpha : 1 >= float >= 0
        Alpha at ``p0``. Set to 0 for a smooth transition, or a larger value to
        clearly delineate significant regions (default 0.5).
    surf : 'inflated' | 'pial' | 'smoothwm' | 'sphere' | 'white'
        Freesurfer surface to use as brain geometry.
    views : str | sequence of str
        One or several views to show in the figure. The options are:
        ``'lateral', 'medial', 'ventral', 'dorsal', 'rostral', 'parietal',
        'frontal', 'caudal'``.
    hemi : 'lh' | 'rh' | 'both' | 'split'
        Which hemispheres to plot (default based on data).
    colorbar : bool
        Add a colorbar to the figure (use ``.plot_colorbar()`` to plot a
        colorbar separately).
    time_label : str
        Label to show time point. Use ``'ms'`` or ``'s'`` to display time in
        milliseconds or in seconds, or supply a custom format string to format
        time values (in seconds; default is ``'ms'``).
    w, h, axw, axh : scalar
        Layout parameters (figure width/height, subplot width/height).
    foreground : mayavi color
        Figure foreground color (i.e., the text color).
    background : mayavi color
        Figure background color.
    parallel : bool
        Set views to parallel projection (default ``True``).
    cortex : str | tuple | dict
        Mark gyri and sulci on the cortex. Presets: ``'classic'`` (default), 
        ``'high_contrast'``, ``'low_contrast'``, ``'bone'``. Can also be a 
        single color (e.g. ``'red'``, ``(0.1, 0.4, 1.)``) or a tuple of two 
        colors for gyri and sulci (e.g. ``['red', 'blue']`` or ``[(1, 0, 0), 
        (0, 0, 1)]``). For all options see the PySurfer documentation.
    title : str
        title for the window (default is the subject name).
    smoothing_steps : None | int
        Number of smoothing steps if data is spatially undersampled (pysurfer
        ``Brain.add_data()`` argument).
    mask : bool | matplotlib color
        Shade areas that are not in ``p_map``. Can be matplotlib color,
        including alpha (e.g., ``(1, 1, 1, 0.5)`` for semi-transparent white).
    subjects_dir : None | str
        Override the subjects_dir associated with the source space dimension.
    name : str
        Equivalent to ``title``, for consistency with other plotting functions. 

    Returns
    -------
    brain : surfer.Brain
        PySurfer Brain instance containing the plot.

    Notes
    -----
    In order to make economical use of the color lookup table, p-values are
    remapped for display. P-values larger than ``p0`` are mapped to 0, p-values
    for positive effects to ``[step, p0 + step]`` and p-values
    for negative effects to ``[-step, -(p0 + step)]``.

    Due to this, in order to plot a colorbar only including positive
    differences yse::

    >>> brain.plot_colorbar(clipmin=0)

    and to include only negative effects::

    >>> brain.plot_colorbar(clipmax=0)
    """
    from .._stats.testnd import NDTest, MultiEffectNDTest

    if isinstance(p_map, NDTest):
        if isinstance(p_map, MultiEffectNDTest):
            raise NotImplementedError(f"plot.brain.p_map for {p_map.__class__.__name__}")
        source = p_map.p.source
    else:
        source = p_map.source
    p = brain(source, None, None, None, *args, **kwargs)
    p.add_ndvar_p_map(p_map, param_map, p0, p1, p0alpha)
    return p


def cluster(cluster, vmax=None, *args, **kwargs):
    """Plot a spatio-temporal cluster

    Plots a cluster with the assumption that all non-zero data should be
    visible, while areas that not part of the cluster are 0.

    Parameters
    ----------
    cluster : NDVar
        The cluster.
    vmax : scalar != 0
        Maximum value in the colormap. Default is the maximum value in the
        cluster.
    surf : 'inflated' | 'pial' | 'smoothwm' | 'sphere' | 'white'
        Freesurfer surface to use as brain geometry.
    views : str | sequence of str
        One or several views to show in the figure. The options are:
        ``'lateral', 'medial', 'ventral', 'dorsal', 'rostral', 'parietal',
        'frontal', 'caudal'``.
    hemi : 'lh' | 'rh' | 'both' | 'split'
        Which hemispheres to plot (default based on data).
    colorbar : bool
        Add a colorbar to the figure (use ``.plot_colorbar()`` to plot a
        colorbar separately).
    time_label : str
        Label to show time point. Use ``'ms'`` or ``'s'`` to display time in
        milliseconds or in seconds, or supply a custom format string to format
        time values (in seconds; default is ``'ms'``).
    w, h, axw, axh : scalar
        Layout parameters (figure width/height, subplot width/height).
    foreground : mayavi color
        Figure foreground color (i.e., the text color).
    background : mayavi color
        Figure background color.
    parallel : bool
        Set views to parallel projection (default ``True``).
    cortex : str | tuple | dict
        Mark gyri and sulci on the cortex. Presets: ``'classic'`` (default), 
        ``'high_contrast'``, ``'low_contrast'``, ``'bone'``. Can also be a 
        single color (e.g. ``'red'``, ``(0.1, 0.4, 1.)``) or a tuple of two 
        colors for gyri and sulci (e.g. ``['red', 'blue']`` or ``[(1, 0, 0), 
        (0, 0, 1)]``). For all options see the PySurfer documentation.
    title : str
        title for the window (default is the subject name).
    smoothing_steps : None | int
        Number of smoothing steps if data is spatially undersampled (pysurfer
        ``Brain.add_data()`` argument).
    mask : bool | matplotlib color
        Shade areas that are not in ``cluster``. Can be matplotlib color,
        including alpha (e.g., ``(1, 1, 1, 0.5)`` for semi-transparent white).
    subjects_dir : None | str
        Override the subjects_dir associated with the source space dimension.
    name : str
        Equivalent to ``title``, for consistency with other plotting functions. 

    Returns
    -------
    brain : surfer.Brain
        PySurfer Brain instance containing the plot.
    """
    if vmax is None:
        vmax = max(cluster.x.max(), -cluster.x.min())
        if vmax == 0:
            raise ValueError("The cluster's data is all zeros")
    elif vmax == 0:
        raise ValueError("vmax can't be 0")
    elif vmax < 0:
        vmax = -vmax

    lut = dspm_lut(0, vmax / 10, vmax)
    return _plot(cluster, lut, -vmax, vmax, *args, **kwargs)


def brain(src, cmap=None, vmin=None, vmax=None, surf='inflated',
          views='lateral', hemi=None, colorbar=False, time_label='ms',
          w=None, h=None, axw=None, axh=None, foreground=None, background=None,
          parallel=True, cortex='classic', title=None, smoothing_steps=None,
          mask=True, subjects_dir=None, name=None, pos=None):
    """Create a :class:`Brain` object with a data layer

    Parameters
    ----------
    src : NDVar ([case,] source, [time]) | SourceSpace | str
        Data to plot; can be specified as :class:`NDVar` with source-space data,
        :class:`SourceSpace` dimension, or as subject name (:class:`str`).
        If ``src`` contains a ``Case`` dimension, the average across cases is
        taken. If it contains integer data, it is plotted as annotation,
        otherwise as data layer.
    cmap : str | array
        Colormap (name of a matplotlib colormap) or LUT array. If ``src`` is an
        integer NDVar, ``cmap`` can be a color dictionary mapping label IDs to
        colors.
    vmin, vmax : scalar
        Endpoints for the colormap. Need to be set explicitly if ``cmap`` is
        a LUT array.
    surf : 'inflated' | 'pial' | 'smoothwm' | 'sphere' | 'white'
        Freesurfer surface to use as brain geometry.
    views : str | sequence of str
        One or several views to show in the figure. The options are:
        ``'lateral', 'medial', 'ventral', 'dorsal', 'rostral', 'parietal',
        'frontal', 'caudal'``.
    hemi : 'lh' | 'rh' | 'both' | 'split'
        Which hemispheres to plot (default based on data).
    colorbar : bool
        Add a colorbar to the figure (use ``.plot_colorbar()`` to plot a
        colorbar separately).
    time_label : str
        Label to show time point. Use ``'ms'`` or ``'s'`` to display time in
        milliseconds or in seconds, or supply a custom format string to format
        time values (in seconds; default is ``'ms'``).
    w, h, axw, axh : scalar
        Layout parameters (figure width/height, subplot width/height).
    foreground : mayavi color
        Figure foreground color (i.e., the text color).
    background : mayavi color
        Figure background color.
    parallel : bool
        Set views to parallel projection (default ``True``).
    cortex : str | tuple | dict
        Mark gyri and sulci on the cortex. Presets: ``'classic'`` (default), 
        ``'high_contrast'``, ``'low_contrast'``, ``'bone'``. Can also be a 
        single color (e.g. ``'red'``, ``(0.1, 0.4, 1.)``) or a tuple of two 
        colors for gyri and sulci (e.g. ``['red', 'blue']`` or ``[(1, 0, 0), 
        (0, 0, 1)]``). For all options see the PySurfer documentation.
    title : str
        title for the window (default is based on the subject name and
        ``src``).
    smoothing_steps : None | int
        Number of smoothing steps if data is spatially undersampled (pysurfer
        ``Brain.add_data()`` argument).
    mask : bool | matplotlib color
        Shade areas that are not in ``src``. Can be matplotlib color, including
        alpha (e.g., ``(1, 1, 1, 0.5)`` for semi-transparent white). If
        smoothing is enabled through ``smoothing_steps``, the mask is added as
        data layer, otherwise it is added as label. To add a mask independently,
        use the :meth:`Brain.add_mask` method.
    subjects_dir : None | str
        Override the subjects_dir associated with the source space dimension.
    name : str
        Equivalent to ``title``, for consistency with other plotting functions. 
    pos : tuple of int
        Position of the new window on the screen.

    Returns
    -------
    brain : Brain
        Brain instance containing the plot.
    """
    if not use_inline_backend():
        from .._wxgui import get_app
        get_app(jumpstart=True)
    from ._brain_object import Brain, get_source_dim

    if isinstance(src, SourceSpace):
        if cmap is not None or vmin is not None or vmax is not None:
            raise TypeError("When plotting SourceSpace, cmap, vmin and vmax "
                            "can not be specified (got %s)" %
                            ', '.join((cmap, vmin, vmax)))
        ndvar = None
        source = src
        subject = source.subject
    elif isinstance(src, str):
        subject = src
        subjects_dir = mne.utils.get_subjects_dir(subjects_dir, True)
        ndvar = None
        source = None
        mask = False
        if hemi is None:
            hemi = 'split'
    else:
        ndvar = brain_data(src)
        if ndvar.has_case:
            ndvar = ndvar.summary()
        source = get_source_dim(ndvar)
        subject = source.subject
        # check that ndvar has the right dimensions
        if ndvar.ndim == 2 and not ndvar.has_dim('time') or ndvar.ndim > 2:
            raise ValueError("NDVar should have dimesions source and "
                             "optionally time, got %r" % (ndvar,))
        if title is None and name is None and ndvar.name is not None:
            title = "%s - %s" % (source.subject, ndvar.name)

    if hemi is None:
        if source.lh_n and source.rh_n:
            hemi = 'split'
        elif source.lh_n:
            hemi = 'lh'
        elif not source.rh_n:
            raise ValueError('No data')
        else:
            hemi = 'rh'
    elif source is None:
        pass
    elif (hemi == 'lh' and source.rh_n) or (hemi == 'rh' and source.lh_n):
        if ndvar is None:
            source = source[source._array_index(hemi)]
        else:
            ndvar = ndvar.sub(**{source.name: hemi})
            source = ndvar.get_dim(source.name)

    if subjects_dir is None:
        subjects_dir = source.subjects_dir

    brain = Brain(subject, hemi, surf, title, cortex,
                  views=views, w=w, h=h, axw=axw, axh=axh,
                  foreground=foreground, background=background,
                  subjects_dir=subjects_dir, name=name, pos=pos,
                  source_space=source)

    if ndvar is not None:
        if ndvar.x.dtype.kind in 'ui':
            brain.add_ndvar_annotation(ndvar, cmap, False)
        else:
            brain.add_ndvar(ndvar, cmap, vmin, vmax, smoothing_steps, colorbar, time_label)

    if mask is not False:
        brain.add_mask(source, mask, smoothing_steps, None, subjects_dir)

    if parallel:
        brain.set_parallel_view(scale=True)
    return brain


@deprecated("0.25", brain)
def surfer_brain(*args, **kwargs):
    pass


def _voxel_brain(data, lut, vmin, vmax):
    """Plot spheres for volume source space

    Parameters
    ----------
    data : NDVar
        Data to plot.
    lut : array
        Color LUT.
    vmin, vmax : scalar
        Data range.
    """
    if data.dimnames != ('source',):
        raise ValueError("Can only plot 1 dimensional source space NDVars")

    from mayavi import mlab

    x, y, z = data.source.coordinates.T

    figure = mlab.figure()
    mlab.points3d(x, y, z, scale_factor=0.002, opacity=0.5)
    pts = mlab.points3d(x, y, z, data.x, vmin=vmin, vmax=vmax)
    pts.module_manager.scalar_lut_manager.lut.table = lut
    return figure


################################################################################
# Bin-Tables
############
# Top-level functions for fmtxt image tables and classes for Eelfigures.
# - _x_bin_table_ims() wrap 'x' brain plot function
# - _bin_table_ims() creates ims given a brain plot function

class ImageTable(ColorBarMixin, EelFigure):
    # Initialize in two steps
    #
    #  1) Initialize class to generate layout
    #  2) Use ._res_h and ._res_w to generate images
    #  3) Finalize by calling ._add_ims()
    #

    def __init__(
            self,
            n_rows: int,
            n_columns: int,
            row_labels: list = False,
            column_labels: list = False,
            title: str = None,
            margins: dict = None,
            **kwargs,
    ):
        default_margins = {}
        if row_labels:
            default_margins['left'] = 0.3
        layout = ImLayout(n_rows * n_columns, 4/3, 2, margins, default_margins, title, column_labels, nrow=n_rows, ncol=n_columns, autoscale=True, **kwargs)
        EelFigure.__init__(self, None, layout)

        self._n_rows = n_rows
        self._n_columns = n_columns
        fig_dpi = matplotlib.rcParams['savefig.dpi']
        if isinstance(fig_dpi, str):
            dpi = layout.dpi
        else:
            dpi = max(layout.dpi, fig_dpi)
        self._res_w = int(round(layout.axw * dpi))
        self._res_h = int(round(layout.axh * dpi))
        if row_labels:
            self.add_row_titles(row_labels, rotation='vertical')
        if column_labels:
            self.add_column_titles(column_labels)

    def _add_ims(self, ims, cmap_params, cmap_data):
        for row, column in product(range(self._n_rows), range(self._n_columns)):
            ax = self._axes[row * self._n_columns + column]
            ax.imshow(ims[row][column])

        ColorBarMixin.__init__(self, lambda: cmap_params, cmap_data)
        self._show()

    def _fill_toolbar(self, tb):
        ColorBarMixin._fill_toolbar(self, tb)

    def add_column_titles(self, titles, x=None, y=0.25, va='center', ha='center', **kwargs):
        """Add a title for each column of images

        Parameters
        ----------
        titles : sequence of str
            Titles, from top to bottom.
        x : scalar
            Horizontal distance from left of the axes (default is to center
            over the axes).
        y : scalar
            Vertical distance from the top of the figure.
        ...
            Matplotlib text parameters.
        """
        if len(titles) > self._n_columns:
            raise ValueError(f"titles={titles}: {len(titles)} titles for {self._n_columns} columns")
        if x is None:
            x = self._layout.axw / 2
        x_left = self._layout.margins['left'] + x
        x_offset = self._layout.margins['wspace'] + self._layout.axw
        y_ = 1 - y / self._layout.h
        for i, label in enumerate(titles):
            x_ = (x_left + i * x_offset) / self._layout.w
            self.figure.text(x_, y_, label, va=va, ha=ha, **kwargs)
        self.draw()

    def add_row_titles(self, titles, x=0.1, y=None, va='center', ha='center', **kwargs):
        """Add a title for each row of images

        Parameters
        ----------
        titles : sequence of str
            Titles, from top to bottom.
        x : scalar
            Horizontal distance from left of the figure.
        y : scalar
            Vertical distance from the bottom of the axes (default is the
            center of the axes).
        ...
            Matplotlib text parameters.
        """
        if len(titles) > self._n_rows:
            raise ValueError(f"titles={titles}: {len(titles)} titles for {self._n_rows} rows")
        if y is None:
            y = self._layout.axh / 2
        y_top = self._layout.margins['top'] + self._layout.axh - y
        y_offset = self._layout.margins['hspace'] + self._layout.axh
        x_ = x / self._layout.w
        for i, label in enumerate(titles):
            y_ = 1 - (y_top + i * y_offset) / self._layout.h
            self.figure.text(x_, y_, label, va=va, ha=ha, **kwargs)
        self.draw()


class _BinTable(EelFigure, ColorBarMixin):
    """Super-class"""
    def __init__(self, ndvar, tstart, tstop, tstep, im_func, surf, views, hemi,
                 summary, title, foreground=None, background=None,
                 parallel=True, smoothing_steps=None, mask=True, margins=None,
                 **kwargs):
        if isinstance(views, str):
            views = (views,)
        data = ndvar.bin(tstep, tstart, tstop, summary)
        n_columns = len(data.time)
        n_hemis = (data.source.lh_n > 0) + (data.source.rh_n > 0)
        n_rows = len(views) * n_hemis

        layout = ImLayout(n_rows * n_columns, 4/3, 2, margins, {'bottom': 0.5}, title, nrow=n_rows, ncol=n_columns, **kwargs)
        EelFigure.__init__(self, None, layout)

        res_w = int(layout.axw * layout.dpi)
        res_h = int(layout.axh * layout.dpi)
        ims, header, cmap_params = im_func(data, surf, views, hemi, axw=res_w,
                                           axh=res_h, foreground=foreground,
                                           background=background,
                                           parallel=parallel,
                                           smoothing_steps=smoothing_steps,
                                           mask=mask)
        for row in range(n_rows):
            for column in range(n_columns):
                ax = self._axes[row * n_columns + column]
                ax.imshow(ims[row][column])

        # time labels
        y = 0.25 / layout.h
        for i, label in enumerate(header):
            x = (0.5 + i) / layout.ncol
            self.figure.text(x, y, label, va='center', ha='center')

        ColorBarMixin.__init__(self, lambda: cmap_params, data)
        self._show()

    def _fill_toolbar(self, tb):
        ColorBarMixin._fill_toolbar(self, tb)


class BinTable(_BinTable):
    """DSPM plot bin-table"""
    def __init__(self, ndvar, tstart=None, tstop=None, tstep=0.1,
                 fmin=13, fmax=22, fmid=None,
                 surf='smoothwm', views=('lat', 'med'), hemi=None,
                 summary='sum', title=None, *args, **kwargs):
        im_func = partial(_dspm_bin_table_ims, fmin, fmax, fmid)
        _BinTable.__init__(self, ndvar, tstart, tstop, tstep, im_func, surf,
                           views, hemi, summary, title, *args, **kwargs)


class ClusterBinTable(_BinTable):
    """Data plotted on brain for different time bins and views

    Parameters
    ----------
    ndvar : NDVar (time x source)
        Data to be plotted.
    tstart : None | scalar
        Time point of the start of the first bin (inclusive; None to use the
        first time point in ndvar).
    tstop : None | scalar
        End of the last bin (exclusive; None to end with the last time point
        in ndvar).
    tstep : scalar
        Size of each bin (in seconds).
    surf : 'inflated' | 'pial' | 'smoothwm' | 'sphere' | 'white'
        Freesurfer surface to use as brain geometry.
    views : list of str
        Views to display (for each hemisphere, lh first). Options are:
        'rostral', 'parietal', 'frontal', 'ventral', 'lateral', 'caudal',
        'medial', 'dorsal'.
    hemi : 'lh' | 'rh' | 'both'
        Which hemispheres to plot (default based on data).
    summary : str
        How to summarize data in each time bin. Can be the name of a numpy
        function that takes an axis parameter (e.g., 'sum', 'mean', 'max') or
        'extrema' which selects the value with the maximum absolute value.
        Default is sum.
    vmax : scalar != 0
        Maximum value in the colormap. Default is the maximum value in the
        cluster.
    title : str
        Figure title.
    """
    def __init__(self, ndvar, tstart=None, tstop=None, tstep=0.1,
                 surf='smoothwm', views=('lat', 'med'), hemi=None,
                 summary='sum', vmax=None, title=None, *args, **kwargs):
        im_func = partial(_cluster_bin_table_ims, vmax)
        _BinTable.__init__(self, ndvar, tstart, tstop, tstep, im_func, surf,
                           views, hemi, summary, title, *args, **kwargs)


def dspm_bin_table(ndvar, fmin=2, fmax=8, fmid=None,
                   tstart=None, tstop=None, tstep=0.1, surf='smoothwm',
                   views=('lat', 'med'), hemi=None, summary='extrema',
                   axw=300, axh=250, *args, **kwargs):
    """Create a table with images for time bins

    Parameters
    ----------
    ndvar : NDVar (time x source)
        Data to be plotted.
    fmin, fmax : scalar >= 0
        Start- and end-point for the color gradient for positive values. The
        gradient for negative values goes from -fmin to -fmax. Values between
        -fmin and fmin are transparent.
    fmid : None | scalar
        Midpoint for the color gradient. If fmid is None (default) it is set
        half way between fmin and fmax.
    tstart : None | scalar
        Time point of the start of the first bin (inclusive; None to use the
        first time point in ndvar).
    tstop : None | scalar
        End of the last bin (exclusive; None to end with the last time point
        in ndvar).
    tstep : scalar
        Size of each bin (in seconds).
    surf : 'inflated' | 'pial' | 'smoothwm' | 'sphere' | 'white'
        Freesurfer surface to use as brain geometry.
    views : list of str
        Views to display (for each hemisphere, lh first). Options are:
        'rostral', 'parietal', 'frontal', 'ventral', 'lateral', 'caudal',
        'medial', 'dorsal'.
    hemi : 'lh' | 'rh' | 'both'
        Which hemispheres to plot (default based on data).
    summary : str
        How to summarize data in each time bin. Can be the name of a numpy
        function that takes an axis parameter (e.g., 'sum', 'mean', 'max') or
        'extrema' which selects the value with the maximum absolute value.
        Default is extrema.
    axw, axh : scalar
        Subplot width/height (default axw=300, axh=250).
    foreground : mayavi color
        Figure foreground color (i.e., the text color).
    background : mayavi color
        Figure background color.
    parallel : bool
        Set views to parallel projection (default ``True``).
    cortex : str | tuple | dict
        Mark gyri and sulci on the cortex. Presets: ``'classic'`` (default), 
        ``'high_contrast'``, ``'low_contrast'``, ``'bone'``. Can also be a 
        single color (e.g. ``'red'``, ``(0.1, 0.4, 1.)``) or a tuple of two 
        colors for gyri and sulci (e.g. ``['red', 'blue']`` or ``[(1, 0, 0), 
        (0, 0, 1)]``). For all options see the PySurfer documentation.
    smoothing_steps : None | int
        Number of smoothing steps if data is spatially undersampled (pysurfer
        ``Brain.add_data()`` argument).
    mask : bool | matplotlib color
        Shade areas that are not in ``ndvar``. Can be matplotlib color,
        including alpha (e.g., ``(1, 1, 1, 0.5)`` for semi-transparent white).
    subjects_dir : None | str
        Override the subjects_dir associated with the source space dimension.
    name : str
        Equivalent to ``title``, for consistency with other plotting functions. 


    Returns
    -------
    images : Image
        FMTXT Image object that can be saved as SVG or integrated into an
        FMTXT document.


    Notes
    -----
    Plotting is based on :func:`plot.brain.dspm`.

    The resulting image can be saved with either of the following (currently
    the only supported formats)::

    >>> image.save_html("name.html")
    >>> image.save_image("name.svg")


    See Also
    --------
    plot.brain.bin_table: plotting clusters as bin-table
    """
    data = ndvar.bin(tstep, tstart, tstop, summary)
    ims, header, _ = _dspm_bin_table_ims(fmin, fmax, fmid, data, surf, views,
                                         hemi, axw, axh, *args, **kwargs)
    return im_table(ims, header)


def bin_table(ndvar, tstart=None, tstop=None, tstep=0.1, surf='smoothwm',
              views=('lat', 'med'), hemi=None, summary='sum', vmax=None,
              axw=300, axh=250, *args, **kwargs):
    """Create a table with images for time bins

    Parameters
    ----------
    ndvar : NDVar (time x source)
        Data to be plotted.
    tstart : None | scalar
        Time point of the start of the first bin (inclusive; None to use the
        first time point in ndvar).
    tstop : None | scalar
        End of the last bin (exclusive; None to end with the last time point
        in ndvar).
    tstep : scalar
        Size of each bin (in seconds).
    surf : 'inflated' | 'pial' | 'smoothwm' | 'sphere' | 'white'
        Freesurfer surface to use as brain geometry.
    views : list of str
        Views to display (for each hemisphere, lh first). Options are:
        'rostral', 'parietal', 'frontal', 'ventral', 'lateral', 'caudal',
        'medial', 'dorsal'.
    hemi : 'lh' | 'rh' | 'both'
        Which hemispheres to plot (default based on data).
    summary : str
        How to summarize data in each time bin. Can be the name of a numpy
        function that takes an axis parameter (e.g., 'sum', 'mean', 'max') or
        'extrema' which selects the value with the maximum absolute value.
        Default is sum.
    vmax : scalar != 0
        Maximum value in the colormap. Default is the maximum value in the
        cluster.
    out : 'image' | 'figure'
        Format in which to return the plot. ``'image'`` (default) returns an
        Image object that
    axw, axh : scalar
        Subplot width/height (default axw=300, axh=250).
    foreground : mayavi color
        Figure foreground color (i.e., the text color).
    background : mayavi color
        Figure background color.
    parallel : bool
        Set views to parallel projection (default ``True``).
    cortex : str | tuple | dict
        Mark gyri and sulci on the cortex. Presets: ``'classic'`` (default), 
        ``'high_contrast'``, ``'low_contrast'``, ``'bone'``. Can also be a 
        single color (e.g. ``'red'``, ``(0.1, 0.4, 1.)``) or a tuple of two 
        colors for gyri and sulci (e.g. ``['red', 'blue']`` or ``[(1, 0, 0), 
        (0, 0, 1)]``). For all options see the PySurfer documentation.
    smoothing_steps : None | int
        Number of smoothing steps if data is spatially undersampled (pysurfer
        ``Brain.add_data()`` argument).
    mask : bool | matplotlib color
        Shade areas that are not in ``ndvar``. Can be matplotlib color,
        including alpha (e.g., ``(1, 1, 1, 0.5)`` for semi-transparent white).
    subjects_dir : None | str
        Override the subjects_dir associated with the source space dimension.
    name : str
        Equivalent to ``title``, for consistency with other plotting functions. 


    Returns
    -------
    images : Image
        FMTXT Image object that can be saved as SVG or integrated into an
        FMTXT document.


    Notes
    -----
    Plotting is based on :func:`plot.brain.cluster`.

    The resulting image can be saved with either of the following (currently
    the only supported formats)::

    >>> image.save_html("name.html")
    >>> image.save_image("name.svg")


    See Also
    --------
    plot.brain.dspm_bin_table: plotting SPMs as bin-table
    """
    data = ndvar.bin(tstep, tstart, tstop, summary)
    ims, header, _ = _cluster_bin_table_ims(vmax, data, surf, views, hemi,
                                            axw, axh, *args, **kwargs)
    return im_table(ims, header)


def _dspm_bin_table_ims(fmin, fmax, fmid, data, surf, views, hemi, axw, axh,
                        *args, **kwargs):
    if fmax is None:
        fmax = max(data.max(), -data.min())

    def brain_(hemi_):
        return dspm(data, fmin, fmax, fmid, surf, views[0], hemi_, False, None,
                    axw, axh, *args, **kwargs)

    return _bin_table_ims(data, hemi, views, brain_)


def _cluster_bin_table_ims(vmax, data, surf, views, hemi, axw, axh, *args,
                           **kwargs):
    if vmax is None:
        vmax = max(-data.min(), data.max())
        if vmax == 0:
            raise NotImplementedError("The data of ndvar is all zeros")
    elif vmax == 0:
        raise ValueError("vmax can't be 0")
    elif vmax < 0:
        vmax = -vmax

    def brain_(hemi_):
        return cluster(data, vmax, surf, views[0], hemi_, False, None, axw,
                       axh, None, None, *args, **kwargs)

    return _bin_table_ims(data, hemi, views, brain_)


def _bin_table_ims(data, hemi, views, brain_func):
    if isinstance(views, str):
        views = (views,)
    ims = []
    if hemi is None:
        hemis = []
        if data.source.lh_n:
            hemis.append('lh')
        if data.source.rh_n:
            hemis.append('rh')
    elif hemi == 'both':
        hemis = ['lh', 'rh']
    elif hemi == 'lh' or hemi == 'rh':
        hemis = [hemi]
    else:
        raise ValueError("hemi=%s" % repr(hemi))

    cmap_params = None
    for hemi in hemis:
        brain = brain_func(hemi)

        hemi_lines = [[] for _ in views]
        for i in range(len(data.time)):
            brain.set_data_time_index(i)
            for line, view in zip(hemi_lines, views):
                brain.show_view(view)
                im = brain.screenshot_single('rgba', True)
                line.append(im)
        ims += hemi_lines
        if cmap_params is None:
            cmap_params = brain._get_cmap_params()
        brain.close()

    header = ['%i - %i ms' % (ms(t0), ms(t1)) for t0, t1 in data.info['bins']]
    return ims, header, cmap_params


class SPLayer(Enum):
    ITEM = 1  # multiple separate NDVars
    SEQUENCE = 2  # One NDVar with multiple images (e.g. time sequence)
    OVERLAY = 3  # static overlay applying to all items/the whole sequence


class SPPlotType(Enum):
    DATA = 1
    LABEL = 2
    FUNC = 3


@dataclass
class SequencePlotterLayer:
    kind: SPLayer
    ndvar: NDVar
    args: tuple
    kwargs: dict
    label: Sequence[str] = None
    index: int = None  # when adding multiple items, index of the item
    plot_type: SPPlotType = SPPlotType.DATA

    def __post_init__(self):
        if self.label is not None:
            if self.kind == SPLayer.SEQUENCE:
                if not isinstance(self.label, (tuple, list)):
                    raise TypeError(f"label={self.label!r}; list or tuple of str expected")
            else:
                if not isinstance(self.label, str):
                    raise TypeError(f"label={self.label!r}; str expected")
        if self.kind == SPLayer.ITEM:
            assert isinstance(self.index, int)
        else:
            assert self.index is None

    def plot(self, brain):
        if self.plot_type == SPPlotType.DATA:
            brain.add_ndvar(self.ndvar, *self.args, time_label='', **self.kwargs)
        elif self.plot_type == SPPlotType.LABEL:
            brain.add_ndvar_label(self.ndvar, *self.args, **self.kwargs)
        elif self.plot_type == SPPlotType.FUNC:
            func = self.args[0]
            func(brain)


class SequencePlotter:
    """Grid of anatomical images in one figure

    Examples
    --------
    Plot an evoked response or TRF (time by source ``ndvar``) in 50 ms bins::

        ndvar_binned = ndvar.bin(0.05, 0, 0.3, 'extrema')
        sp = plot.brain.SequencePlotter()
        sp.set_brain_args(surf='smoothwm')
        sp.add_ndvar(ndvar_binned)
        p = sp.plot_table(view='lateral')
        p.save('Figure.pdf')

    Plot specific time points in an evoked response or TRF (``ndvar``)::

        cmap = plot.soft_threshold_colormap('xpolar-a', 0.0001, 0.010)
        sp = plot.brain.SequencePlotter()
        sp.set_brain_args(surf='smoothwm')
        for t in [0.050, 0.100, 0.200]:
            sp.add_ndvar(ndvar.sub(time=t), cmap=cmap, label=f'{int(t*1000)} ms')
        p = sp.plot_table(view='lateral', orientation='vertical')

    Plot a test result::

        res = testnd.TTestRelated('srcm', 'condition')
        vmax = 3  # explicitly set vmax to make sure that the color-maps agree
        sp = plot.brain.SequencePlotter()
        sp.set_brain_args(surf='inflated')
        sp.add_ndvar(res.c1_mean, vmax=vmax, label='a')
        sp.add_ndvar(res.c0_mean, vmax=vmax, label = 'b')
        sp.add_ndvar(res.masked_difference(), vmax=vmax, label='a - b')
        p = sp.plot_table(view='lateral', orientation='vertical')
    """
    max_n_bins = 25

    def __init__(self):
        self._data = []
        self._source = None
        self._frame_dim = None
        self._bin_kind = None
        self._frame_order = None
        self._brain_args = {}
        self._parallel_view = {}

    def _assert_has_frame_dim(self):
        if self._frame_dim is None:
            raise RuntimeError("Need to set at least one NDVar first")
        elif self._frame_dim is False:
            raise RuntimeError("Only applies to SequencePlotters with 2d NDVars")

    def set_brain(self, source):
        """Set the brain model on which to plot

        This is usually handled automatically, and only needs to be invoked
        directly for plots not otherwise involving an :class:`NDVar` with a
        :class:`SourceSpace` dimension.

        Parameters
        ----------
        source : SourceSpace
            Brain model on which to plot.
        """
        if not isinstance(source, SourceSpace):
            raise TypeError(f"{source!r}")
        elif self._source is None:
            self._source = source
        elif source.subject != self._source.subject:
            raise ValueError(f"NDVar has different subject ({source.subject}) than previously added data ({self._source.subject})")
        elif source.subjects_dir != self._source.subjects_dir:
            raise ValueError(f"NDVar has different subjects_dir ({source.subjects_dir}) than previously added data ({self._source.subjects_dir})")

    def _n_items(self):
        if self._bin_kind == SPLayer.SEQUENCE:
            raise RuntimeError("Trying to retrieve number of items for dimension-based plot")
        indices = [l.index for l in self._data if l.index is not None]
        if indices:
            return max(indices) + 1
        self._bin_kind = SPLayer.ITEM
        return 0

    def set_brain_args(self, surf='inflated', foreground=None, background=None, parallel=True, cortex='classic', mask=True):
        "Set parameters for anatomical plot (see :func:`.brain`)"
        self._brain_args = {'surf': surf, 'foreground': foreground, 'background': background, 'parallel': parallel, 'cortex': cortex, 'mask': mask}

    def set_parallel_view(self, forward=None, up=None, scale=None):
        "Set view for all plots (see :meth:`~.brain_object.Brain.set_parallel_view`"
        if forward is not None:
            self._parallel_view['forward'] = forward
        if up is not None:
            self._parallel_view['up'] = up
        if scale is not None:
            self._parallel_view['scale'] = scale

    def _index(self, index: int) -> int:
        # index arg to valid index
        if index is None:
            return self._n_items()
        elif index < 0:
            return self._n_items() + index
        else:
            return index

    def add_function(self, func, label=None, overlay=False):
        "Custom modification of the brain object (calls ``func(brain)``)"
        args = (func,)
        if overlay:
            index = None
            kind = SPLayer.OVERLAY
        else:
            index = self._n_items()
            kind = SPLayer.ITEM
        layer = SequencePlotterLayer(kind, None, args, {}, label, index, SPPlotType.FUNC)
        self._data.append(layer)

    def add_ndvar(self, ndvar, *args, static=None, index=None, label=None, **kwargs):
        """Add a data layer to the brain plot

        Multiple data layers can be added sequentially, but each additional
        layer needs to have a time dimension that is compatible with previous
        layers (or no time dimension).

        Parameters
        ----------
        ndvar : NDVar
            Data to add. ``Source`` dimension only for a static layer,
            additional ``time`` or ``case`` dimension for dynamic layers.
        ...
            :meth:`~._brain_object.Brain.add_ndvar` parameters.
        static : bool
            When supplying a one dimensional ``ndvar``, whether to consider it
            as a static layer (an overlay appearing on all plots) or as one of
            several plots (default).
        index : int
            When adding separate frames (rows/columns), explicitly specify the
            frame index (the default is to add a frame at the end; use -1 to
            add an overlay to the most recent frame).
        label : str | sequence of str
            Label when adding multiple separate NDVars. Labels for bins when
            adding ``ndvar`` with multiple bins.
        """
        self.set_brain(ndvar.get_dim('source'))

        # find row/column dimension
        if ndvar.ndim == 1:
            frame_dim = None
        elif ndvar.ndim == 2:
            dim_name = ndvar.get_dimnames((None, 'source'))[0]
            frame_dim = ndvar.get_dim(dim_name)
        else:
            raise ValueError(f"{ndvar!r}: Need NDVar with 1 or 2 dimensions")

        if frame_dim is None:
            # apply defaults
            if static is None:
                static = True if self._frame_dim else False  # None: unset or use multiple NDVars
            index = self._index(index)
            # extract
            if static:
                kind = SPLayer.OVERLAY
            elif self._frame_dim:
                raise ValueError(f"static={static!r} when adding to plot with dimension {self._frame_dim}")
            else:
                kind = SPLayer.ITEM
                self._bin_kind = SPLayer.ITEM
            layer = SequencePlotterLayer(kind, ndvar, args, kwargs, label, index)
        elif self._bin_kind == SPLayer.ITEM:
            raise ValueError(f"Can't add 2d NDVar to SequencePlotter with multiple NDVars")
        elif index is not None:
            raise TypeError(f"index={index!r}")
        elif static:
            raise ValueError(f"static={static!r} for multi-dimensional NDVar")
        else:
            self._bin_kind = SPLayer.SEQUENCE
            if self._frame_dim is None:
                if len(frame_dim) > self.max_n_bins:
                    raise ValueError(f"Trying to plot {frame_dim} with {len(frame_dim)} bins. If this is intentional, set SequencePlotter.max_n_bins to a larger value.")
                self._frame_dim = frame_dim
            elif frame_dim != self._frame_dim:
                raise ValueError(f"New axis {frame_dim} is incompatible with previously set axis {self._frame_dim}")

            if label is None and 'bins' in ndvar.info:
                label = ndvar.info['bins']

            layer = SequencePlotterLayer(SPLayer.SEQUENCE, ndvar, args, kwargs, label)

        self._data.append(layer)

    def add_ndvar_label(
            self,
            ndvar: NDVar,
            color: Any = (1, 0, 0),
            borders: int = False,
            name: str = None,
            alpha: float = None,
            lighting: bool = False,
            overlay: bool = False,
            index: int = None,
            label: str = None,
    ):
        """Add a boolean label to the brain plot

        Parameters
        ----------
        ...
            See :meth:`~._brain_object.Brain.add_ndvar_label`
        overlay
            Plot the label over all plots in the sequence.
        index
            When adding separate frames (rows/columns), explicitly specify the
            frame index (the default is to add a frame at the end; use -1 to
            add an overlay to the most recent frame).
        label
            Label when adding multiple separate NDVars. Labels for bins when
            adding ``ndvar`` with multiple bins.
        """
        self.set_brain(ndvar.get_dim('source'))
        args = (color, borders, name, alpha, lighting)
        if overlay:
            kind = SPLayer.OVERLAY
        else:
            index = self._index(index)
            kind = SPLayer.ITEM
        layer = SequencePlotterLayer(kind, ndvar, args, {}, label, index, SPPlotType.LABEL)
        self._data.append(layer)

    def add_pmap(self, res: Union[NDTest, NDVar], label=None, **kwargs):
        "See :meth:`~._brain_object.Brain.add_ndvar_p_map`"
        # interpret NDTest subtypes
        if isinstance(res, MultiEffectNDTest):
            iterator = zip(res.p, res._statistic_map, res.effects)
        elif isinstance(res, NDVar):
            iterator = [res, None, res.name]
        else:
            if isinstance(res, NDDifferenceTest):
                desc = res.difference.name
            else:
                desc = res._name()
            iterator = [(res.p, res._statistic_map, desc)]
        # add p-maps
        for p_map, stat_map, desc in iterator:
            ndvar, cmap, vmax = p_lut(p_map, stat_map)
            layer_label = desc if label is None else label
            self.add_ndvar(ndvar, cmap, -vmax, vmax, label=layer_label, **kwargs)

    def set_frame_order(self, order):
        """Set the order in which frames are plotted

        Parameters
        ----------
        order : list
            Sequence of frame dimension indices.
        """
        self._assert_has_frame_dim()
        missing = [x for x in order if x not in self._frame_dim]
        if missing:
            raise ValueError(f"order={order!r}; the following elements are not part of the frame dimension: {', '.join(missing)}")
        self._frame_order = order

    def _get_frame_labels(self, labels):
        if labels is None:
            return
        elif labels is True:
            if self._bin_kind == SPLayer.ITEM:
                labels = []
                for i in range(self._n_items()):
                    layers = [l for l in self._data if l.index == i]
                    items = [l.label for l in layers if l.label is not None]
                    if len(items) == 0:
                        label = ''
                    else:
                        label = items[0]
                    labels.append(label)
            else:
                if self._frame_order is None:
                    labels = list(self._frame_dim)
                else:
                    index = self._frame_dim._array_index(self._frame_order)
                    labels = [self._frame_dim[i] for i in index]
            if not any(labels):
                return

        # float -> ms
        out = []
        for label in labels:
            if isinstance(label, str):
                out.append(label)
            elif isinstance(label, Number):
                out.append(f'{ms(label)} ms')
            elif len(label) == 2:
                out.append(f'{ms_window(*label)} ms')
            else:
                out.append(str(label))
        return out

    def plot_table(self, hemi=None, view=('lateral', 'medial'), orientation='horizontal', labels=True, mode='rgb', antialiased=False, **kwargs):
        """Create a figure with the images

        Parameters
        ----------
        hemi : 'lh' | 'rh' | 'both'
            Hemispheres to plot (default is all hemispheres with data).
        view : str | list of {str | tuple}
            Views to plot. A view can be specified as a string, or as a tuple
            including parallel-view parameters ``(view, forward, up, scale)``,
            e.g., ``('lateral', 0, 10, 70)``.
        orientation : 'vertical' | 'horizontal'
            Direction of the time/case axis.
        labels : bool | list of str
            Headers for columns/rows of images (default is inferred from the data).
        mode : 'rgb' | 'rgba'
            Image mode (default ```'rgb'``, set to ``'rgba'`` to include alpha
            channel).
        antialiased : bool
            Apply antialiasing to the images (default ``False``).
        ...
            Layout parameters for the figure.

        Returns
        -------
        fig : plot.ImageTable
            Figure created by the plot.

        Notes
        -----
        Use the ``margins`` parameter to control image spacing. For example (all
        numbers in inches)::

            margins = {
                'left': 0.1,    # left mergin
                'right': 0.1,   # right margin
                'top': 0.5,     # margin at the top, include space for title
                'bottom': 0.1,  # bottom
                'hspace': 0.1,  # height of the space between images
                'wspace': 0.1,  # width of the space between images
            }
        """
        if self._source is None:
            raise RuntimeError("No brain model specified for plotting; use .set_brain()")
        if not self._data:
            raise RuntimeError("No data")
        labels = self._get_frame_labels(labels)
        # determine hemisphere(s) to plot
        if hemi is None:
            hemis = []
            sss = [data.ndvar.source for data in self._data if data.ndvar is not None]
            if any(ss.lh_n for ss in sss):
                hemis.append('lh')
            if any(ss.rh_n for ss in sss):
                hemis.append('rh')
            assert hemis, "Data in neither hemisphere"
        elif hemi == 'both':
            hemis = ('lh', 'rh')
        elif hemi in ('lh', 'rh'):
            hemis = (hemi,)
        else:
            raise ValueError(f"hemi={hemi!r}")
        # views
        if isinstance(view, str):
            views = (view,)
        elif len(view) > 1 and not isinstance(view[1], str):
            views = (view,)
        else:
            views = view

        n_views = len(hemis) * len(views)
        if self._frame_order:
            bins = self._frame_dim._array_index(self._frame_order)
        elif self._frame_dim:
            bins = list(range(len(self._frame_dim)))
        elif self._bin_kind == SPLayer.ITEM:
            bins = list(range(self._n_items()))
        else:
            bins = [None]
        n_bins = len(bins)
        if orientation == 'horizontal':
            n_columns = n_bins
            n_rows = n_views
            transpose = False
            column_labels = labels
            row_labels = None
        elif orientation == 'vertical':
            n_columns = n_views
            n_rows = n_bins
            transpose = True
            column_labels = None
            row_labels = labels
        else:
            raise ValueError(f"orientation={orientation!r}")

        figure = ImageTable(n_rows, n_columns, row_labels, column_labels, **kwargs)

        im_rows = []
        cmap_params = None
        cmap_data = None
        for hemi in hemis:
            hemi_rows = [[] for _ in views]

            # plot brain
            b = brain(self._source, hemi=hemi, views='lateral', w=figure._res_w, h=figure._res_h, time_label='', **self._brain_args)

            if self._bin_kind == SPLayer.SEQUENCE:
                for l in self._data:
                    l.plot(b)
                    if cmap_params is None and l.kind == SPLayer.SEQUENCE:
                        cmap_params = b._get_cmap_params()
                        cmap_data = l.ndvar

                # capture images
                for i in bins:
                    if i is not None:
                        b.set_data_time_index(i)
                        self._capture(b, hemi_rows, views, mode, antialiased)
            elif self._bin_kind == SPLayer.ITEM:
                for i in bins:
                    for l in self._data:
                        if l.kind == SPLayer.OVERLAY or l.index == i:
                            l.plot(b)
                            if cmap_params is None and l.plot_type == SPPlotType.DATA and l.kind == SPLayer.ITEM:
                                cmap_params = b._get_cmap_params()
                                cmap_data = l.ndvar
                    self._capture(b, hemi_rows, views, mode, antialiased)
                    b.remove_data()
                    b.remove_labels()
            else:
                raise NotImplementedError(f"{self._bin_kind}")
            im_rows += hemi_rows
            b.close()

        if transpose:
            im_rows = list(zip(*im_rows))
        figure._add_ims(im_rows, cmap_params, cmap_data)
        return figure

    def _capture(self, b, hemi_rows, views, mode, antialiased):
        # Alternative saving image files
        # import os
        # import tempfile
        # import PIL.Image
        # from mayavi import mlab
        # with tempfile.TemporaryDirectory() as tempdir:
        # path = os.path.join(tempdir, 'brain.tiff')
        for row, view in zip(hemi_rows, views):
            if isinstance(view, str):
                b.show_view(view)
                if self._parallel_view:
                    b.set_parallel_view(**self._parallel_view)
            else:
                b.show_view(view[0])
                b.set_parallel_view(*view[1:])
            # mlab.savefig(path, figure=b.brain_matrix[-1, -1]._f)
            # image = PIL.Image.open(path)
            # im = np.array(image)
            im = b.screenshot_single(mode, antialiased)
            row.append(im)


def connectivity(source):
    """Plot source space connectivity

    Parameters
    ----------
    source : SourceSpace | NDVar
        Source space or NDVar containing the source space.

    Returns
    -------
    figure : mayavi Figure
        The figure.
    """
    from mayavi import mlab

    if isinstance(source, NDVar):
        source = source.get_dim('source')

    connections = source.connectivity()
    coords = source.coordinates
    x, y, z = coords.T

    figure = mlab.figure()
    src = mlab.pipeline.scalar_scatter(x, y, z, figure=figure)
    src.mlab_source.dataset.lines = connections
    lines = mlab.pipeline.stripper(src)
    mlab.pipeline.surface(lines, colormap='Accent', line_width=1, opacity=1.,
                          figure=figure)
    return figure


def copy(brain):
    "Copy the figure to the clip board"
    return brain.copy_screenshot()


def butterfly(y, cmap=None, vmin=None, vmax=None, surf='inflated',
              views='lateral', hemi=None,
              w=5, h=2.5, smoothing_steps=None, mask=True,
              xlim=None, name=None):
    """Shortcut for a Butterfly-plot with a time-linked brain plot

    Parameters
    ----------
    y : NDVar  ([case,] time, source)
        Data to plot; if ``y`` has a case dimension, the mean is plotted.
        ``y`` can also be a :mod:`~eelbrain.testnd` t-test result, in which
        case a masked parameter map is plotted (p ≤ 0.05).
    cmap : str | array
        Colormap (name of a matplotlib colormap).
    vmin : scalar
        Plot data range minimum.
    vmax : scalar
        Plot data range maximum.
    surf : 'inflated' | 'pial' | 'smoothwm' | 'sphere' | 'white'
        Freesurfer surface to use as brain geometry.
    views : str | sequence of str
        One or several views to show in the figure. The options are:
        ``'lateral', 'medial', 'ventral', 'dorsal', 'rostral', 'parietal',
        'frontal', 'caudal'``.
    hemi : 'lh' | 'rh'
        Plot only this hemisphere (the default is to plot all hemispheres with
        data in ``y``).
    w : scalar
        Butterfly plot width (inches).
    h : scalar
        Plot height (inches; applies to butterfly and brain plot).
    smoothing_steps : None | int
        Number of smoothing steps if data is spatially undersampled (pysurfer
        ``Brain.add_data()`` argument).
    mask : bool | matplotlib color
        Shade areas that are not in ``src``. Can be matplotlib color, including
        alpha (e.g., ``(1, 1, 1, 0.5)`` for semi-transparent white). If
        smoothing is enabled through ``smoothing_steps``, the mask is added as
        data layer, otherwise it is added as label. To add a mask independently,
        use the :meth:`Brain.add_mask` method.
    xlim : scalar | (scalar, scalar)
        Initial x-axis view limits as ``(left, right)`` tuple or as ``length``
        scalar (default is the full x-axis in the data).
    name : str
        The window title (default is y.name).

    Returns
    -------
    butterfly_plot : plot.Butterfly
        Butterfly plot.
    brain : Brain
        Brain plot.
    """
    hemis, bfly_data, brain_data = butterfly_data(y, hemi)

    if name is None:
        name = brain_data.name

    # butterfly-plot
    p = Butterfly(bfly_data, vmin=vmin, vmax=vmax, xlim=xlim, h=h, w=w, ncol=1, name=name, color='black', ylabel=hemis, axtitle=False)

    # Brain plot
    brain_h = h * p._layout.dpi
    p_brain = brain(brain_data, cmap, vmin, vmax, surf, views, hemi, mask=mask, smoothing_steps=smoothing_steps, axh=brain_h, name=name)

    p._auto_position(p_brain)
    p.link_time_axis(p_brain)

    return p, p_brain
