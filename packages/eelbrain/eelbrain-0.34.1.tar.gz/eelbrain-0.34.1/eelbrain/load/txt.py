"""
Tools for loading data from text files.

.. autosummary::
   :toctree: generated

   tsv
   var
"""
import csv
import os
from pathlib import Path
import re
from numbers import Number
from typing import Sequence, Union

import numpy as np

from .._types import PathArg
from .._utils import ui
from .._utils.parse import FLOAT_NAN_PATTERN
from .. import _data_obj as _data

__all__ = ('tsv', 'var')


def to_num(v: str):
    if v.isdigit():
        return int(v)
    else:
        return float(v)


# could use csv module:  http://docs.python.org/3/library/csv.html
def tsv(
        path: PathArg = None,
        names: Union[Sequence[str], bool] = True,
        types: Union[str, dict] = None,
        delimiter: str = 'auto',
        skiprows: int = 0,
        start_tag: str = None,
        ignore_missing: bool = False,
        empty: Union[str, float] = None,
        random: Union[str, Sequence[str]] = None,
        **fmtparams,
):
    r"""Load a :class:`Dataset` from a text file.

    Parameters
    ----------
    path : str
        Path to the file (if omitted, use a system file dialog).
    names : Sequence of str | bool
        Column/variable names.

        * ``True`` (default): look for names on the first line of the file
        * ``['name1', ...]`` use these names
        * ``False``: use "v1", "v2", ...
    types : str | dict
        Column data types::

         - 'a': determine automatically
         - 'f': Factor
         - 'v': Var
         - 'b': boolean Var

        Specified either as string, with one type per columnc (e.g.
        ``'ffvva'``) or as ``{column_name: data_type}`` dictionary (e.g.
        ``{'participant': 'f'}``); unspecified columns default to ``'a'``.
    delimiter : str
        Value delimiting cells in the input file (default depends on ``path``:
        ``','`` if the extension is ``'.csv'``, otherwise ``'\t'``).
    skiprows : int
        Skip so many rows at the beginning of the file (for tsv files with
        headers). Column names are expected to come after the skipped rows.
        ``skiprows`` is applied after ``start_tag``.
    start_tag : str
        Alternative way to skip header rows. The table is assumed to start
        on the line following the last line in the file that starts with
        ``start_tag``.
    ignore_missing : bool
        Ignore rows with missing values (i.e., lines that contain fewer
        ``delimiter`` than the others; by default this raises an IOError). For
        rows with missing values, ``NaN`` is substituted for numerical and
        ``""`` for categorial variables.
    empty : number | 'nan'
        For numerical variables, substitute this value for empty entries. For
        example, if a column in a file contains ``['5', '3', '']``, this is read
        by default as ``Factor(['5', '3', ''])``.
        With ``empty=0``, it is read as ``Var([5, 3, 0])``.
        With ``empty='nan'``, it is read as ``Var([5, 3, nan])``.
    random : str | sequence of str
        Names of the columns that should be assigned as random factor.
    **fmtparams
        Further formatting parameters for :func:`csv.reader`. For example, a
        fixed-width column file can be loaded with ``skipinitialspace=True``
        (as long as there are no empty cells).
    """
    if path is None:
        path = ui.ask_file("Load TSV", "Select tsv file to import as Dataset")
        if not path:
            return
    path = Path(path)

    if isinstance(random, str):
        random = [random]
    elif random is None:
        random = []
    else:
        random = list(random)

    if delimiter is None:  # legacy option
        delimiter = ' '
        fmtparams['skipinitialspace'] = True
    elif delimiter == 'auto':
        suffix = path.suffix.lower()
        if suffix == '.csv':
            delimiter = ','
        else:
            delimiter = '\t'

    with open(path, newline='') as fid:
        reader = csv.reader(fid, delimiter=delimiter, **fmtparams)
        lines = list(reader)

    # find start position
    if start_tag:
        start = 0
        for i, line in enumerate(lines, 1):
            if line[0].startswith(start_tag):
                start = i
        if start:
            lines = lines[start:]
    if skiprows:
        lines = lines[skiprows:]

    # read / create names
    if names is True:
        names = lines.pop(0)
    elif names:
        names = list(names)

    row_lens = set(len(row) for row in lines)
    if not ignore_missing and len(row_lens) > 1:
        raise IOError("Not all rows have same number of entries. Set ignore_missing to True in order to ignore this error.")
    n_cols = max(row_lens)
    n_rows = len(lines)

    if names:
        n_names = len(names)
        if n_names == n_cols - 1:
            # R write.table saves unnamed column with row names
            name = "row"
            while name in names:
                name += '_'
            names.insert(0, name)
        elif n_names != n_cols:
            raise IOError(f"The number of names in the header ({n_names}) does not correspond to the number of columns in the table ({n_cols})")
    else:
        names = [f'v{i}' for i in range(n_cols)]

    # check random
    missing = [k for k in random if k not in names]
    if missing:
        raise ValueError(f"random={random} includes non-existent names: {', '.join(missing)}")

    # coerce types parameter
    if types is None:
        types_ = 'a' * n_cols
    elif isinstance(types, dict):
        types_ = [types.get(n, 'a') for n in names]
    elif isinstance(types, str):
        types_ = types
    elif isinstance(types, (list, tuple)):
        # backwards compatibility
        types_ = ['afv'[v] for v in types]
    else:
        raise TypeError(f'types={types!r}')

    # check types values
    if len(types_) != n_cols:
        raise ValueError(f'types={types!r}: {len(types)} values for file with {n_cols} columns')
    elif set(types_).difference('afvb'):
        invalid = ', '.join(map(repr, set(types_).difference('afvb')))
        raise ValueError(f'types={types!r}: invalid values {invalid}')

    # find quotes (imply type 1)
    # quotes = "'\""
    data = np.empty((n_rows, n_cols), object)
    for r, line in enumerate(lines):
        for c, v in enumerate(line):
            # for str_del in quotes:
            #     if len(v) > 0 and v[0] == str_del:
            #         v = v.strip(str_del)
            #         types_[c] = 'f'
            data[r, c] = v

    # convert values to data-objects
    float_pattern = re.compile(FLOAT_NAN_PATTERN)
    ds = _data.Dataset(name=os.path.basename(path))
    np_vars = {
        'NA': np.nan,
        'na': np.nan,
        'NaN': np.nan,
        'nan': np.nan,
        'NAN': np.nan,
        None: np.nan,
    }
    if empty is not None:
        if isinstance(empty, str):
            np_vars[''] = to_num(empty)
        elif isinstance(empty, Number):
            np_vars[''] = empty
        else:
            raise TypeError(f'empty={empty!r}')
    bool_dict = {'True': True, 'False': False, None: False}
    keys = {}
    for name, values, type_ in zip(names, data.T, types_):
        # infer type
        if type_ in 'fvb':
            pass
        elif all(v in bool_dict for v in values):
            type_ = 'b'
        elif empty is not None:
            if all(v in (None, '') or float_pattern.match(v) for v in values):
                type_ = 'v'
            else:
                type_ = 'f'
        elif all(v is None or float_pattern.match(v) for v in values):
            type_ = 'v'
        else:
            type_ = 'f'

        # substitute values
        if type_ == 'v':
            values = [np_vars[v] if v in np_vars else to_num(v) for v in values]
        elif type_ == 'b':
            values = [bool_dict[v] for v in values]

        # create data-object
        if type_ == 'f':
            f_random = name in random
            dob = _data.Factor(values, labels={None: ''}, name=name, random=f_random)
        elif name in random:
            raise ValueError(f"random={random}: {name} is not categorial")
        else:
            dob = _data.Var(values, name)
        key = _data.Dataset.as_key(name)
        keys[name] = key
        ds[key] = dob

    if any(k != v for k, v in keys.items()):
        ds.info['keys'] = keys

    return ds


def var(path: PathArg = None, name: str = None):
    """
    Load a :class:`Var` object from a text file by splitting at white-spaces.

    Parameters
    ----------
    path : str
        Source file. If not specified, a system file dialog is opened.
    name : str
        Name for the Var.
    """
    if path is None:
        path = ui.ask_file("Load Var File", "Select Var File")
        if not path:
            return

    FILE = open(path)
    lines = FILE.read().split()
    FILE.close()
    is_bool = all(line in ['True', 'False'] for line in lines)

    if is_bool:
        x = np.genfromtxt(path, dtype=bool)
    else:
        x = np.loadtxt(path)

    return _data.Var(x, name)
