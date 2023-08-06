from collections.abc import Iterator
from dataclasses import dataclass, fields
from functools import reduce
from operator import mul
from typing import List, Tuple, Union

import numpy as np
import scipy.signal
from scipy.linalg import norm

from .. import _info
from .._data_obj import CategorialArg, NDVarArg, Dataset, NDVar, Case, UTS, dataobj_repr, ascategorial, asndvar
from .._utils import LazyProperty, PickleableDataClass
from .._utils.numpy_utils import newaxis


class EQMixIn:

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for field in fields(self):
            a, b = getattr(self, field.name), getattr(other, field.name)
            if isinstance(a, b.__class__):
                if isinstance(a, np.ndarray):
                    if not np.array_equal(a, b):
                        break
                elif a != b:
                    break
            else:
                break
        else:
            return True
        return False


@dataclass(eq=False)
class Split(PickleableDataClass, EQMixIn):
    train: np.ndarray  # (, 2) array of int, segment (start, stop)
    validate: np.ndarray = None
    test: np.ndarray = None
    i_test: int = 0  # Index (to group splits with the same test segmet)

    @LazyProperty
    def train_and_validate(self):
        return np.vstack([self.train, self.validate])


def merge_segments(
        segments: np.ndarray,
        soft_splits: Union[bool, np.ndarray] = None,
):
    """Take a selection of input segments and remove soft boundaries"""
    # return out_segments
    if soft_splits is None or isinstance(soft_splits, np.ndarray) and len(soft_splits) == 0:
        return segments
    out_segments = list(segments)
    for i in range(len(out_segments)-1, 0, -1):
        pre_seg, post_seg = out_segments[i-1], out_segments[i]
        if pre_seg[1] >= post_seg[0]:
            if soft_splits is True or post_seg[0] in soft_splits:
                out_segments[i-1] = [pre_seg[0], max(pre_seg[1], post_seg[1])]
                del out_segments[i]
    return np.vstack(out_segments)


@dataclass(eq=False)
class Splits(PickleableDataClass, EQMixIn):
    splits: List[Split]
    partitions_arg: Union[int, None]
    n_partitions: int
    n_validate: int
    n_test: int
    model: CategorialArg = None
    segments: np.ndarray = None  # Original data segments
    split_segments: np.ndarray = None  # Data subdivision for splits

    def __repr__(self):
        if len(self.segments) == 1:
            desc = "continuous data"
        else:
            desc = f"{len(self.segments)} data segments"
        items = ['']
        if self.n_validate:
            items.append(f'n_validate={self.n_validate}')
        if self.n_test:
            items.append(f'n_test={self.n_test}')
        if self.model is not None:
            items.append(f'model={dataobj_repr(self.model)}')
        items = ', '.join(items)
        return f"<Splits: {desc} split into {len(self.split_segments)} sections{items}>"

    def plot(self, **kwargs):
        """Plot data splits (see :class:`plot.SplitFigure` for parameters)"""
        from ..plot import DataSplit

        return DataSplit(self, **kwargs)


def split_data(
        segments: np.ndarray,  # (n, 2) array of [start, stop] indices
        partitions: int = None,  # Number of segments to split the data
        model: CategorialArg = None,  # sample evenly from cells
        ds: Dataset = None,
        validate: int = 1,  # Number of segments in validation set
        test: int = 0,  # Number of segments in test set
):
    """Split data segments into train, validate and test segments"""
    if partitions is not None and partitions <= validate + test:
        raise ValueError(f"partitions={partitions} with validate={validate}, test={test}")
    partitions_arg = partitions
    assert validate >= 0
    if validate > 1:
        raise NotImplementedError
    assert test >= 0
    if test > 1:
        raise NotImplementedError
    if len(segments) == 1:
        if partitions is None:
            partitions = 2 + test + validate if test else 10
        if model is not None:
            raise TypeError(f'model={dataobj_repr(model)!r}: model cannot be specified in unsegmented data')
        n_times = segments[0, 1] - segments[0, 0]
        split_points = np.round(np.linspace(0, n_times, partitions + 1)).astype(np.int64)
        soft_splits = split_points[1:-1]
        split_segments = np.vstack([split_points[i: i+2] for i in range(partitions)])
        categories = [None]
    else:
        n_segments = len(segments)
        # determine model cells
        if model is None:
            categories = [None]
            cell_size = n_segments
        else:
            model = ascategorial(model, ds=ds, n=n_segments)
            categories = [np.flatnonzero(model == cell) for cell in model.cells]
            cell_sizes = [len(i) for i in categories]
            cell_size = min(cell_sizes)
            cell_sizes_are_equal = len(set(cell_sizes)) == 1
            if partitions is None and not cell_sizes_are_equal:
                raise NotImplementedError(f'Automatic partition for variable cell size {dict(zip(model.cells, cell_sizes))}')
        # automatic selection of partitions
        if partitions is None:
            if 3 <= cell_size <= 10:
                partitions = cell_size
            else:
                raise NotImplementedError(f"Automatic partition for {cell_size} cases")
        # create segments
        if cell_size >= partitions:
            soft_splits = None
            split_segments = segments
        else:
            # need to subdivide segments
            if model is not None:
                raise NotImplementedError(f'partitions={partitions}: with model')
            elif partitions % cell_size:
                raise ValueError(f'partitions={partitions}: not a multiple of n_cases ({cell_size})')
            n_parts = partitions // cell_size
            split_segments = []
            soft_splits = []
            for start, stop in segments:
                split_points = np.round(np.linspace(start, stop, n_parts)).astype(np.int64)
                soft_splits.append(split_points[1:-1])
                split_segments.extend(split_points[i: i + 2] for i in range(n_parts))
            soft_splits = np.concatenate(soft_splits)
            split_segments = np.vstack(split_segments)
    # create actual splits
    splits = []  # list of Split
    test_iter = range(partitions) if test else [None]
    validate_iter = range(partitions) if validate else [None]
    n_segments = len(split_segments)
    for i_test in test_iter:
        for i_validate in validate_iter:
            if i_test == i_validate:
                continue
            train_set = np.ones(n_segments, bool)
            # test set
            if i_test is None:
                test_segments = None
            else:
                test_set = np.zeros(n_segments, bool)
                for cell_index in categories:
                    index = slice(i_test, None, partitions)
                    if cell_index is not None:
                        index = cell_index[index]
                    test_set[index] = True
                train_set ^= test_set
                test_segments = merge_segments(split_segments[test_set], soft_splits)
            # validation set
            if i_validate is None:
                validate_segments = None
            else:
                validate_set = np.zeros(n_segments, bool)
                for cell_index in categories:
                    index = slice(i_validate, None, partitions)
                    if cell_index is not None:
                        index = cell_index[index]
                    validate_set[index] = True
                train_set ^= validate_set
                validate_segments = merge_segments(split_segments[validate_set], soft_splits)
            # create split
            train_segments = merge_segments(split_segments[train_set], soft_splits)
            splits.append(Split(train_segments, validate_segments, test_segments, i_test))
    return Splits(splits, partitions_arg, partitions, validate, test, model, segments, split_segments)


class PredictorData:
    """Restructure model NDVars (like RevCorrData but for x only)"""

    def __init__(
            self,
            x: Union[NDVarArg, List[NDVarArg]],
            ds: Dataset = None,
    ):
        if isinstance(x, (tuple, list, Iterator)):
            multiple_x = True
            xs = [asndvar(x_, ds=ds) for x_ in x]
            if len(xs) == 0:
                raise ValueError(f"x={x!r} of length 0")
            x_name = [x_.name for x_ in xs]
        else:
            multiple_x = False
            xs = [asndvar(x, ds=ds)]
            x_name = xs[0].name

        time_dim = xs[0].get_dim('time')
        if any(xi.get_dim('time') != time_dim for xi in xs[1:]):
            raise ValueError("Not all NDVars in x have the same time dimension")
        n_times = len(time_dim)

        # determine cases (used as segments)
        has_case = n_cases = segments = None
        for xi in xs:
            # determine cases
            if n_cases is None:
                has_case = xi.has_case
                if xi.has_case:
                    n_cases = len(xi)
                    # prepare segment index
                    seg_i = np.arange(0, n_cases * n_times + 1, n_times, np.int64)[:, newaxis]
                    segments = np.hstack((seg_i[:-1], seg_i[1:]))
                else:
                    n_cases = 0
                    segments = np.array([[0, n_times]], np.int64)
            elif xi.has_case ^ has_case:
                raise ValueError(f'x={xs}: some but not all x have case')
            elif has_case and len(xi) != n_cases:
                raise ValueError(f'x={xs}: not all items have the same number of cases')

        # x_data:  predictor x time array
        x_data = []
        x_meta = []
        x_names = []
        n_x = 0
        for xi in xs:
            ndim = xi.ndim - bool(n_cases)
            if ndim == 1:
                xdim = None
                dimnames = ('case' if n_cases else newaxis, 'time')
                data = xi.get_data(dimnames)
                index = n_x
                x_names.append(dataobj_repr(xi))
            elif ndim == 2:
                dimnames = xi.get_dimnames(last='time')
                xdim = xi.get_dim(dimnames[-2])
                if n_cases:
                    dimnames = (xdim.name, 'case', 'time')
                data = xi.get_data(dimnames)
                index = slice(n_x, n_x + len(data))
                x_repr = dataobj_repr(xi)
                for v in xdim:
                    x_names.append("%s-%s" % (x_repr, v))
            else:
                raise NotImplementedError("x with more than 2 dimensions")
            if n_cases:
                data = data.reshape((-1, n_cases * n_times))
            x_data.append(data)
            x_meta.append((xi.name, xdim, index))
            n_x += len(data)

        if len(x_data) == 1:
            x_data = x_data[0]
            x_data_is_copy = False
        else:
            x_data = np.concatenate(x_data)
            x_data_is_copy = True

        self.has_case = has_case
        self.n_cases = n_cases
        self.case_to_segments = n_cases > 0
        self.time_dim = time_dim
        self.n_times = n_times
        self.n_times_flat = n_cases * n_times if n_cases else n_times
        self.multiple_x = multiple_x
        self.x_name = x_name
        self.x_names = x_names
        self.x_meta = x_meta
        self.data = x_data
        self.data_is_copy = x_data_is_copy
        self.segments = segments


class RevCorrData:
    """Restructure input NDVars into arrays for reverse correlation
    
    Attributes
    ----------
    y : NDVar
        Dependent variable.
    x : NDVar | sequence of NDVar
        Predictors.
    segments : np.ndarray
        ``(n_segments, 2)`` array of segment ``[start, stop]`` indices. The
        segments delimit chunks of continuous data, such as trials.
    splits : list of Split
        Cross-validation scheme.
    """
    # data
    x_mean = None
    x_scale = None
    y_mean = None
    y_scale = None
    x_pads = None
    _x_is_copy: bool = False
    _y_is_copy: bool = False
    # prefit
    scale_data: bool = False
    _prefit_repr: str = None
    # cross-validation
    splits: Splits = None

    def __init__(
            self,
            y: NDVarArg,
            x: Union[NDVarArg, List[NDVarArg]],
            ds: Dataset = None,
            in_place: bool = False,
    ):
        x_data = PredictorData(x, ds)

        # check y
        y = asndvar(y, ds=ds)
        if y.get_dim('time') != x_data.time_dim:
            raise ValueError("y does not have the same time dimension as x")
        if y.has_case ^ x_data.has_case:
            raise ValueError(f'y={y!r}: case dimension does not match x')
        elif y.has_case and len(y) != x_data.n_cases:
            raise ValueError(f'y={y!r}: different number of cases from x ({x_data.n_cases})')

        # vector dimension
        vector_dims = [dim.name for dim in y.dims if dim._connectivity_type == 'vector']
        if not vector_dims:
            vector_dim = None
        elif len(vector_dims) == 1:
            vector_dim = y.get_dim(vector_dims.pop())
        else:
            raise NotImplementedError(f"y={y!r}: more than one vector dimension ({', '.join(vector_dims)})")

        # y_data: flatten to ydim x time array
        last = ('time',)
        n_ydims = -1
        if x_data.case_to_segments:
            last = ('case', *last)
            n_ydims -= 1
        if vector_dim:
            last = (vector_dim.name, *last)
        y_dimnames = y.get_dimnames(last=last)
        ydims = y.get_dims(y_dimnames[:n_ydims])
        n_flat = reduce(mul, map(len, ydims), 1)
        shape = (n_flat, x_data.n_times_flat)
        y_data = y.get_data(y_dimnames).reshape(shape)
        # shape for exposing vector dimension
        if vector_dim:
            n_flat_prevector = reduce(mul, map(len, ydims[:-1]), 1)
            n_vector = len(ydims[-1])
            assert n_vector > 1
            vector_shape = (n_flat_prevector, n_vector, x_data.n_times_flat)
        else:
            vector_shape = None

        self.time = x_data.time_dim
        self.segments = x_data.segments
        self.shortest_segment_n_times = x_data.n_times
        self.in_place = in_place
        # y
        self.y = y_data  # (n_signals, n_times)
        self.y_name = y.name
        self._y_repr = dataobj_repr(y)
        self.y_info = _info.copy(y.info)
        self.ydims = ydims  # without case and time
        self.yshape = tuple(map(len, ydims))
        self.full_y_dims = y.get_dims(y_dimnames)
        self.vector_dim = vector_dim  # vector dimension
        self.vector_shape = vector_shape  # flat shape with vector dim separate
        # x
        self.x = x_data.data  # (n_predictors, n_times)
        self.x_name = x_data.x_name
        self.x_names = x_data.x_names
        self._x_meta = x_data.x_meta  # [(x.name, xdim, index), ...]; index is int or slice
        self._multiple_x = x_data.multiple_x
        self._x_is_copy = x_data.data_is_copy
        # basis
        self.basis = 0
        self.basis_window = None

    def _copy_data(self, y=False):
        "Make sure the data is a copy before modifying"
        if self.in_place:
            return
        if not self._x_is_copy:
            self.x = self.x.copy()
            self._x_is_copy = True
        if y and not self._y_is_copy:
            self.y = self.y.copy()
            self._y_is_copy = True

    def apply_basis(self, basis: float, basis_window: str):
        """Apply basis to x

        Notes
        -----
        Normalize after applying basis (basis can smooth out variance).
        """
        if self.basis != 0:
            raise NotImplementedError("Applying basis more than once")
        elif not basis:
            return
        self._copy_data()
        n = int(round(basis / self.time.tstep))
        w = scipy.signal.get_window(basis_window, n, False)
        if len(w) <= 1:
            raise ValueError(f"basis={basis!r}: Window is {len(w)} samples long")
        w /= w.sum()
        for xi in self.x:
            xi[:] = scipy.signal.convolve(xi, w, 'same')
        self.basis = basis
        self.basis_window = basis_window

    @LazyProperty
    def x_pads(self):
        return np.zeros(len(self.x))

    def normalize(self, error: str):
        self._copy_data(y=True)
        y_mean = self.y.mean(1)
        x_mean = self.x.mean(1)
        self.y -= y_mean[:, newaxis]
        self.x -= x_mean[:, newaxis]
        # for vector data, scale by vector norm
        if self.vector_shape:
            y_data_vector_shape = self.y.reshape(self.vector_shape)
            y_data_for_scale = norm(y_data_vector_shape, axis=1)
        else:
            y_data_vector_shape = None
            y_data_for_scale = self.y

        if error == 'l1':
            y_scale = np.abs(y_data_for_scale).mean(-1)
            x_scale = np.abs(self.x).mean(-1)
        elif error == 'l2':
            y_scale = (y_data_for_scale ** 2).mean(-1) ** 0.5
            x_scale = (self.x ** 2).mean(-1) ** 0.5
        else:
            raise RuntimeError(f"error={error!r}")

        if self.vector_shape:
            y_data_vector_shape /= y_scale[:, newaxis, newaxis]
        else:
            self.y /= y_scale[:, newaxis]
        self.x /= x_scale[:, newaxis]

        self.scale_data = error
        self.y_mean = y_mean
        self.y_scale = y_scale
        self.x_mean = x_mean
        self.x_scale = x_scale
        # zero-padding for convolution
        self.x_pads = -x_mean / x_scale

    def _check_data(self):
        if self.x_scale is None:
            x_check = self.x.var(1)
            y_check = self.y.var(1)
        else:
            x_check = self.x_scale
            y_check = self.y_scale
        # check for flat data
        zero_var = y_check == 0
        if np.any(zero_var):
            raise ValueError(f"y={self._y_repr}: contains {zero_var.sum()} flat time series")
        zero_var = x_check == 0
        if np.any(zero_var):
            names = [self.x_names[i] for i in np.flatnonzero(zero_var)]
            raise ValueError(f"x: flat data in {', '.join(names)}")
        # check for NaN
        has_nan = np.isnan(y_check.sum())
        if has_nan:
            raise ValueError(f"y={self._y_repr}: contains NaN")
        has_nan = np.isnan(x_check)
        if np.any(has_nan):
            names = [self.x_names[i] for i in np.flatnonzero(has_nan)]
            raise ValueError(f"x: NaN in {', '.join(names)}")

    def prefit(self, res):
        if not res:
            return
        from ._boosting import convolve
        hs = (res.h_source,) if isinstance(res.h_source, NDVar) else res.h_source
        n_y = self.y.shape[0]
        n_x = self.x.shape[0]
        # check that names are unique
        x_names = [name for name, *_ in self._x_meta]
        if len(set(x_names)) != len(x_names):
            raise ValueError(f"prefit={res}: prefit requires that all predictors have unique names; x has names {x_names}")
        # check that prefit matches y dims
        h0 = hs[0]
        index = {}
        for ydim in self.ydims:
            hdim = h0.get_dim(ydim.name)
            if hdim == ydim:
                continue
            elif not hdim._is_superset_of(ydim):
                raise ValueError(f"prefit: y dimension {ydim.name} has elements that are not contained in the prefit")
            index[ydim.name] = hdim.index_into_dim(ydim)
        if index:
            hs = [h.sub(**index) for h in hs]
        # check predictor dims
        y_dimnames = [dim.name for dim in self.ydims]
        meta = {name: (dim, index) for name, dim, index in self._x_meta}
        for h in hs:
            if h.name not in meta:
                raise ValueError(f"prefit: {h.name!r} not in x")
            dim, index = meta[h.name]
            need_dimnames = (*y_dimnames, 'time') if dim is None else (*y_dimnames, dim.name, 'time')
            if h.dimnames != need_dimnames:
                raise ValueError(f"prefit: {h.name!r} dimension mismatch, has {h.dimnames}, needs {need_dimnames}")
            if dim is not None and h.dims[-2] != dim:
                raise ValueError(f"prefit: {h.name!r} {dim.name} dimension mismatch")
        # generate flat h
        h_n_times = len(h0.get_dim('time'))
        h_flat = []
        h_index = []
        for h in hs:
            dimnames = h.get_dimnames(first=y_dimnames, last='time')
            h_data = h.get_data(dimnames)
            index = meta[h.name][1]
            if isinstance(index, int):
                h_flat.append(h_data.reshape((n_y, 1, h_n_times)))
                h_index.append(index)
            else:
                n_hdim = index.stop - index.start
                h_flat.append(h_data.reshape((n_y, n_hdim, h_n_times)))
                h_index.extend(range(index.start, index.stop))
        h_flat = np.concatenate(h_flat, 1)
        # assert scaling equivalent
        # assert np.all(res.x_mean == self.x_mean[h_index])
        # assert np.all(res.x_scale == self.x_scale[h_index])
        # subset to relevant data
        x = self.x[h_index]
        x_pads = self.x_pads[h_index]
        # subtract prefit predictions
        if isinstance(res.tstart, list):
            tstart1 = min(res.tstart)
        else:
            tstart1 = res.tstart
        i_start = int(round(tstart1 / self.time.tstep))
        for y, h in zip(self.y, h_flat):
            y -= convolve(h, x, x_pads, i_start, self.segments)
        # remove prefit predictors
        keep = np.setdiff1d(np.arange(n_x), h_index)
        self.x = self.x[keep]
        self.x_mean = self.x_mean[keep]
        self.x_scale = self.x_scale[keep]
        self.x_pads = self.x_pads[keep]
        self._x_is_copy = True
        # update x meta-information
        target_index = np.empty(n_x, int)
        target_index.fill(-1)
        target_index[keep] = np.arange(len(keep))
        new_meta = []
        self.x_name = []
        for name, xdim, index in self._x_meta:
            if isinstance(index, int):
                new_index = target_index[index]
                if new_index < 0:
                    continue
            else:
                new_start = target_index[index.start]
                if new_start < 0:
                    continue
                new_stop = target_index[index.stop - 1] + 1
                new_index = slice(new_start, new_stop)
            new_meta.append((name, xdim, new_index))
            self.x_name.append(name)
        self._x_meta = new_meta
        self._multiple_x = len(self._x_meta) > 1
        self._prefit_repr = repr(res)

    def initialize_cross_validation(
            self,
            partitions: int = None,  # Number of segments to split the data
            model: CategorialArg = None,  # sample evenly from cells
            ds: Dataset = None,
            validate: int = 1,  # Number of segments in validation set
            test: int = 0,  # Number of segments in test set
    ):
        """Initialize cross-validation scheme

        Notes
        -----
        General solution:

         - split data into even sized segments (hard and soft splits)
         - group segments by cell-index
         - create splits
         - merge segments at soft boundaries
        """
        self.splits = split_data(self.segments, partitions, model, ds, validate, test)

    def data_scale_ndvars(self):
        if self.scale_data:
            # y
            if self.yshape:
                y_mean = NDVar(self.y_mean.reshape(self.yshape), self.ydims, self.y_name, self.y_info)
            else:
                y_mean = self.y_mean[0]
            # scale does not include vector dim
            if self.vector_dim:
                dims = self.ydims[:-1]
                shape = self.yshape[:-1]
            else:
                dims = self.ydims
                shape = self.yshape
            if shape:
                y_scale = NDVar(self.y_scale.reshape(shape), dims, self.y_name, self.y_info)
            else:
                y_scale = self.y_scale[0]
            # x
            x_mean = []
            x_scale = []
            for name, dim, index in self._x_meta:
                if dim is None:
                    x_mean.append(self.x_mean[index])
                    x_scale.append(self.x_scale[index])
                else:
                    dims = (dim,)
                    x_mean.append(NDVar(self.x_mean[index], dims, name))
                    x_scale.append(NDVar(self.x_scale[index], dims, name))
            if self._multiple_x:
                x_mean = tuple(x_mean)
                x_scale = tuple(x_scale)
            else:
                x_mean = x_mean[0]
                x_scale = x_scale[0]
        else:
            y_mean = y_scale = x_mean = x_scale = None
        return y_mean, y_scale, x_mean, x_scale

    def package_kernel(self, h, tstart):
        """Package kernel as NDVar
        
        Parameters
        ----------
        h : array  (n_y, n_x, n_times)
            Kernel data.
        """
        h_time = UTS(tstart, self.time.tstep, h.shape[-1], self.time.unit)
        hs = []
        if self.scale_data:
            info = _info.for_normalized_data(self.y_info, 'Response')
        else:
            info = self.y_info

        for name, dim, index in self._x_meta:
            x = h[:, index, :]
            if dim is None:
                dims = (h_time,)
            else:
                dims = (dim, h_time)
            if self.ydims:
                dims = self.ydims + dims
                if len(self.ydims) > 1:
                    x = x.reshape(self.yshape + x.shape[1:])
            else:
                x = x[0]
            hs.append(NDVar(x, dims, name, info))

        if self._multiple_x:
            return tuple(hs)
        else:
            return hs[0]

    def package_value(
            self,
            value: np.ndarray,  # data
            name: str,  # NDVar name
            info: dict = None,  # NDVar info
            meas: str = None,  # for NDVar info
    ):
        if not self.yshape:
            return value[0]

        # shape
        has_vector = value.shape[0] > self.yshape[0]
        if self.vector_dim and not has_vector:
            dims = self.ydims[:-1]
            shape = self.yshape[:-1]
        else:
            dims = self.ydims
            shape = self.yshape
        if not dims:
            return value[0]
        elif len(shape) > 1:
            value = value.reshape(shape)

        # info
        if meas:
            info = _info.for_stat_map(meas, old=info)
        elif info is None:
            info = self.y_info

        return NDVar(value, dims, name, info)

    def package_y_like(self, data, name):
        shape = tuple(map(len, self.full_y_dims))
        data = data.reshape(shape)
        # roll Case to first axis
        for axis, dim in enumerate(self.full_y_dims):
            if isinstance(dim, Case):
                data = np.rollaxis(data, axis)
                dims = list(self.full_y_dims)
                dims.insert(0, dims.pop(axis))
                break
        else:
            dims = self.full_y_dims
        return NDVar(data, dims, name)
