# Author: Christian Brodbeck <christianbrodbeck@nyu.edu>
"""Configure Eelbrain"""
import multiprocessing
import os
import sys

from matplotlib.colors import to_rgb

from ._utils import IS_OSX


SUPPRESS_WARNINGS = True
CONFIG = {
    'n_workers': multiprocessing.cpu_count(),
    'eelbrain': True,
    'autorun': None,
    'show': True,
    'format': 'svg',
    'figure_background': 'white',
    'prompt_toolkit': True,
    'animate': True,
    'nice': 0,
    'tqdm': False,  # disable=CONFIG['tqdm']
}

# Python 3.8 switched default to spawn, which makes pytest hang  (https://docs.python.org/3/whatsnew/3.8.html#multiprocessing)
method = multiprocessing.get_start_method()
if sys.version_info.minor >= 8 and IS_OSX:
    method = 'fork'
mpc = multiprocessing.get_context(method)


def configure(
        n_workers=None,
        frame=None,
        autorun=None,
        show=None,
        format=None,
        figure_background=None,
        prompt_toolkit=None,
        animate=None,
        nice=None,
        tqdm=None,
):
    """Set basic configuration parameters for the current session

    Parameters
    ----------
    n_workers : bool | int
        Number of worker processes to use in multiprocessing enabled
        computations. ``False`` to disable multiprocessing. ``True`` (default)
        to use as many processes as cores are available. Negative numbers to use
        all but n available CPUs.
    frame : bool
        Open figures in the Eelbrain application. This provides additional
        functionality such as copying a figure to the clipboard. If False, open
        figures as normal matplotlib figures.
    autorun : bool
        When a figure is created, automatically enter the GUI mainloop. By
        default, this is True when the figure is created in interactive mode
        but False when the figure is created in a script (in order to run the
        GUI at a specific point in a script, call :func:`eelbrain.gui.run`).
    show : bool
        Show plots on the screen when they're created (disable this to create
        plots and save them without showing them on the screen).
    format : str
        Default format for plots (for example "png", "svg", ...).
    figure_background : bool | matplotlib color
        While :mod:`matplotlib` uses a gray figure background by default,
        Eelbrain uses white. Set this parameter to ``False`` to use the default
        from :attr:`matplotlib.rcParams`, or set it to a valid matplotblib
        color value to use an arbitrary color. ``True`` to revert to the default
        white.
    prompt_toolkit : bool
        In IPython 5, prompt_toolkit allows running the GUI main loop in
        parallel to the Terminal, meaning that the IPython terminal and GUI
        windows can be used without explicitly switching between Terminal and
        GUI. This feature is enabled by default, but can be disabled by setting
        ``prompt_toolkit=False``.
    animate : bool
        Animate plot navigation (default True).
    nice : int [-20, 19]
        Scheduling priority for muliprocessing (larger number yields more to
        other processes; negative numbers require root privileges).
    tqdm : bool
        Enable or disable :mod:`tqdm` progress bars.
    """
    # don't change values before raising an error
    new = {}
    if n_workers is not None:
        if n_workers is True:
            new['n_workers'] = multiprocessing.cpu_count()
        elif n_workers is False:
            new['n_workers'] = 0
        elif isinstance(n_workers, int):
            cpu_count = multiprocessing.cpu_count()
            if n_workers < 0:
                if cpu_count - n_workers < 1:
                    raise ValueError(f"n_workers={n_workers}, but only {cpu_count} CPUs are available")
                new['n_workers'] = cpu_count - n_workers
            else:
                new['n_workers'] = n_workers
        else:
            raise TypeError("n_workers=%r" % (n_workers,))
    if frame is not None:
        new['eelbrain'] = bool(frame)
    if autorun is not None:
        new['autorun'] = bool(autorun)
    if show is not None:
        new['show'] = bool(show)
    if format is not None:
        new['format'] = format.lower()
    if figure_background is not None:
        if figure_background is True:
            figure_background = 'white'
        elif figure_background is not False:
            to_rgb(figure_background)
        new['figure_background'] = figure_background
    if prompt_toolkit is not None:
        new['prompt_toolkit'] = bool(prompt_toolkit)
    if animate is not None:
        new['animate'] = bool(animate)
    if nice is not None:
        nice = int(nice)
        if not -20 <= nice < 20:
            raise ValueError("nice=%i; needs to be in range [-20, 19]" % (nice,))
        elif nice < 0 and not os.getuid() == 0:
            raise ValueError("nice=%i; values < 0 require root privileges" % (nice,))
        new['nice'] = nice
    if tqdm is not None:
        new['tqdm'] = not tqdm

    CONFIG.update(new)
