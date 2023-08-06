# Author: Christian Brodbeck <christianbrodbeck@nyu.edu>
"A few basic operations needed throughout Eelbrain"
from collections import defaultdict
from dataclasses import dataclass, fields
import functools
import logging
import re
from warnings import warn

from .notebooks import tqdm


LOG_LEVELS = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO,
              'WARNING': logging.WARNING, 'ERROR': logging.ERROR,
              'CRITICAL': logging.CRITICAL}


def as_list(item):
    if isinstance(item, list):
        return item
    else:
        return [item]


def as_sequence(items, item_type=str):
    if isinstance(items, item_type):
        return items,
    return items


def ask(message, options, allow_empty=False, help=None) -> str:
    """Ask user for input

    Parameters
    ----------
    message : str
        Message.
    options : dict
        ``{command: description}`` mapping.
    allow_empty : bool
        Allow empty string as command.
    help : str
        If provided, add a "help" option that prints ``help``.

    Returns
    -------
    command : str
        The user command.
    """
    options = dict(options)
    if help is not None:
        assert 'help' not in options
        options['help'] = 'display help'
    print(message)
    print('---')
    print('\n'.join(f'{k}:  {v}' for k, v in options.items()))
    while True:
        command = input(" > ")
        if command in options or (allow_empty and not command):
            if help is not None and command == 'help':
                print(help)
            else:
                return command
        else:
            print(f"Invalid entry - type one of ({', '.join(options)})")


def deprecated(version, replacement):
    """Decorator to deprecate functions and methods

    Also handles docstring of the deprecated function.

    Parameters
    ----------
    version : str
        Version in which the feature will be removed.
    replacement : callable | str
        Either a verbal description, or a pointer to the direct replacement
        function which takes the same arguments. In the latter case, the
        replacement is automatically called and the deprecated function is not
        used anymore.
    """
    def dec(func):
        msg = f"{func.__name__} is deprecated and will be removed in version {version}"
        if isinstance(replacement, str):
            msg += '; ' + replacement
            call_func = func
        elif replacement is not None:
            msg += f"; use {replacement.__name__} instead"
            call_func = replacement
        else:
            raise TypeError(f"replacement={replacement!r}")
        func.__doc__ = msg

        @functools.wraps(func)
        def new(*args, **kwargs):
            warn(msg, DeprecationWarning)
            return call_func(*args, **kwargs)

        return new
    return dec


def _deprecated_alias(alias, for_, version):
    """Create a deprecated alias

    Parameters
    ----------
    alias : str
        Name of the alias.
    for_ : callable
        New function (replacement).
    version : str
        Version in which the feature will be removed.
    """
    @functools.wraps(for_)
    def new(*args, **kwargs):
        warn(f"{alias} has been renamed to {for_.__name__}. {alias} will be removed in version {version}", DeprecationWarning)
        return for_(*args, **kwargs)
    return new


def deprecated_attribute(version, class_name, replacement):
    if not isinstance(replacement, str):
        raise TypeError("replacement=%r" % (replacement,))

    class Dec:

        def __init__(self, meth):
            self._meth = meth
            self.__name__ = meth.__name__
            self._msg = (
                'The %s.%s attribute is deprecated and will be removed in '
                'version %s, use %s.%s instead.' %
                (class_name, meth.__name__, version, class_name, replacement))

        def __get__(self, obj, klass=None):
            if obj is None:
                return None
            warn(self._msg, DeprecationWarning)
            return getattr(obj, replacement)

    return Dec


def log_level(arg):
    """Convert string to logging module constant"""
    if isinstance(arg, int):
        return arg
    elif isinstance(arg, str):
        try:
            return LOG_LEVELS[arg.upper()]
        except KeyError:
            raise ValueError("Invalid log level: %s. mus be one of %s" %
                             (arg, ', '.join(LOG_LEVELS)))
    else:
        raise TypeError("Invalid log level: %s. need int or str." % repr(arg))


def set_log_level(level, logger_name='eelbrain'):
    """Set the minimum level of messages to be logged

    Parameters
    ----------
    level : str | int
        Level as string (debug, info, warning, error, critical) or
        corresponding constant from the logging module.
    logger_name : str
        Name of the logger for which to set the logging level. The default is
        the Eelbrain logger.
    """
    logging.getLogger(logger_name).setLevel(log_level(level))


class ScreenHandler(logging.StreamHandler):
    "Log handler compatible with TQDM"

    def __init__(self, formatter=None):
        logging.StreamHandler.__init__(self)
        if formatter is None:
            formatter = logging.Formatter("%(levelname)-8s:  %(message)s")
        self.setFormatter(formatter)

    def emit(self, record):
        tqdm.write(self.format(record))


def intervals(seq):
    """Iterate over each successive pair in a sequence.

    Examples
    --------
    >>> for i in intervals([1, 2, 3, 45]):
    ...     print(i)
    ...
    (1, 2)
    (2, 3)
    (3, 45)
    """
    iterator = iter(seq)
    try:
        last = next(iterator)
    except StopIteration:
        return

    for item in iterator:
        yield last, item
        last = item


class LazyProperty:
    """Decorator for attribute with lazy evaluation

    Notes
    -----
    Based on: http://blog.pythonisito.com/2008/08/lazy-descriptors.html
    Similar concept: https://github.com/jackmaney/lazy-property
    """
    def __init__(self, func):
        self._func = func
        functools.update_wrapper(self, func)

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        result = instance.__dict__[self.__name__] = self._func(instance)
        return result


@dataclass
class PickleableDataClass:

    def __getstate__(self) -> dict:
        return {f.name: getattr(self, f.name) for f in fields(self)}

    def __setstate__(self, state: dict):
        self.__init__(**state)


def _natural_keys(text):
    "Sorting key for natural sorting"
    # after http://stackoverflow.com/a/5967539/166700
    return [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', text)]


def natsorted(seq):
    return sorted(seq, key=_natural_keys)


def n_decimals(number):
    "Number of meaningful decimals in ``number``, at least 1"
    s = str(number)
    if '.' in s:
        return s[::-1].index('.')
    else:
        return 1


class keydefaultdict(defaultdict):
    "http://stackoverflow.com/a/2912455/166700"
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret
