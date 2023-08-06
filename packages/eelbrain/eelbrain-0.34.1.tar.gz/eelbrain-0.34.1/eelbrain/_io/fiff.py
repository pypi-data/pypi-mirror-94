# Author: Christian Brodbeck <christianbrodbeck@nyu.edu>
"""I/O for MNE"""
from collections.abc import Iterable
import fnmatch
from itertools import zip_longest
from logging import getLogger
from math import floor
import os
from pathlib import Path
import re
from typing import Sequence, Union
import warnings

import numpy as np

import mne
from mne.source_estimate import _BaseSourceEstimate
from mne.io.constants import FIFF
from mne.io.kit.constants import KIT
from mne.minimum_norm import prepare_inverse_operator, apply_inverse_raw

from .. import _info
from .._types import PathArg
from .._data_obj import Factor, Var, NDVar, Dataset, Case, Sensor, Space, SourceSpace, VolumeSourceSpace, UTS, _matrix_graph
from .._info import BAD_CHANNELS
from .._text import n_of
from .._utils import ui, as_list
from ..mne_fixes import MNE_EVOKED, MNE_RAW, MNE_VOLUME_STC


try:  # mne >= 0.19
    from mne.io.kit.constants import KIT_NEIGHBORS
except ImportError:
    KIT_NEIGHBORS = {
        KIT.SYSTEM_NYU_2008: 'KIT-157',
        KIT.SYSTEM_NYU_2009: 'KIT-157',
        KIT.SYSTEM_NYU_2010: 'KIT-157',
        KIT.SYSTEM_NYUAD_2011: 'KIT-208',
        KIT.SYSTEM_NYUAD_2012: 'KIT-208',
        KIT.SYSTEM_NYUAD_2014: 'KIT-208',
        KIT.SYSTEM_UMD_2004: 'KIT-UMD-1',
        KIT.SYSTEM_UMD_2014_07: 'KIT-UMD-2',
        KIT.SYSTEM_UMD_2014_12: 'KIT-UMD-3',
    }


def mne_raw(path=None, proj=False, **kwargs):
    """Load a :class:`mne.io.Raw` object

    Parameters
    ----------
    path : None | str
        path to a raw fiff or sqd file. If no path is supplied, a file can be
        chosen from a file dialog.
    proj : bool | str
        Add projections from a separate file to the Raw object.
        **``False``**: No proj file will be added.
        **``True``**: ``'{raw}*proj.fif'`` will be used.
        ``'{raw}'`` will be replaced with the raw file's path minus '_raw.fif',
        and '*' will be expanded using fnmatch. If multiple files match the
        pattern, a ValueError will be raised.
        **``str``**: A custom path template can be provided, ``'{raw}'`` and
        ``'*'`` will be treated as with ``True``.
    kwargs
        Additional keyword arguments are forwarded to :class:`mne.io.Raw`
        initialization.
    """
    if path is None:
        path = ui.ask_file("Pick a raw data file", "Pick a raw data file",
                           [('Functional image file (*.fif)', '*.fif'),
                            ('KIT Raw File (*.sqd,*.con', '*.sqd;*.con')])
        if not path:
            return

    if isinstance(path, str):
        path = Path(path)
    if isinstance(path, Path):
        ext = path.suffix.lower()
        if ext.startswith('.fif'):
            raw = mne.io.read_raw_fif(path, **kwargs)
        elif ext in ('.sqd', '.con'):
            raw = mne.io.read_raw_kit(path, **kwargs)
        else:
            raise ValueError(f"{path}: Unknown extension")
    elif isinstance(path, Iterable):
        # MNE Raw supports list of file-names
        raw = mne.io.read_raw_fif(path, **kwargs)
    else:
        raise TypeError("path=%r" % (path,))

    if proj:
        if proj is True:
            proj = '{raw}*proj.fif'

        if '{raw}' in proj:
            raw_file = raw.filenames[0]
            raw_root, _ = os.path.splitext(raw_file)
            raw_root = raw_root.rstrip('raw')
            proj = proj.format(raw=raw_root)

        if '*' in proj:
            head, tail = os.path.split(proj)
            names = fnmatch.filter(os.listdir(head), tail)
            if len(names) == 1:
                proj = os.path.join(head, names[0])
            else:
                if len(names) == 0:
                    err = "No file matching %r"
                else:
                    err = "Multiple files matching %r"
                raise ValueError(err % proj)

        # add the projections to the raw file
        proj = mne.read_proj(proj)
        raw.add_proj(proj, remove_existing=True)

    return raw


def events(raw=None, merge=None, proj=False, name=None, bads=None,
           stim_channel=None, events=None, annotations=None, **kwargs):
    """
    Load events from a raw fiff file.

    Parameters
    ----------
    raw : str(path) | None | mne Raw
        The raw fiff file from which to extract events (if raw and events are
        both ``None``, a file dialog will be displayed to select a raw file).
    merge : int
        Merge stimulus channel steps occurring in neighboring samples.
        The integer value indicates across how many samples events should
        be merged, and the sign indicates in which direction they should be
        merged (negative means towards the earlier event, positive towards
        the later event). By default, this parameter is based on the data:
        -1 for KIT data, 0 otherwise.
        The main reason for merging events is an artifact from analog event
        recording systems. If events are recorded in an analog channel,
        event onsets can be blurred (what should be ``0, 0, 0, 1, 1, 1, ...``,
        can look like ``0, 0, 0, 0.5, 1, 1, ...``; ``merge=-1`` would
        turn the latter into the former).
    proj : bool | str
        Path to the projections file that will be loaded with the raw file.
        ``'{raw}'`` will be expanded to the raw file's path minus extension.
        With ``proj=True``, ``'{raw}_*proj.fif'`` will be used,
        looking for any projection file starting with the raw file's name.
        If multiple files match the pattern, a ValueError will be raised.
    name : str | None
        A name for the Dataset. If ``None``, the raw filename will be used.
    bads : None | list
        Specify additional bad channels in the raw data file (these are added
        to the ones that are already defined in the raw file).
    stim_channel : None | string | list of string
        Name of the stim channel or all the stim channels
        affected by the trigger. If None, the config variables
        'MNE_STIM_CHANNEL', 'MNE_STIM_CHANNEL_1', 'MNE_STIM_CHANNEL_2',
        etc. are read. If these are not found, it will default to
        'STI 014'.
    events : None | str
        If events are stored in a fiff file separate from the Raw object, the
        path to the events file can be supplied here. The events in the Dataset
        will reflect the event sin the events file rather than the raw file.
    annotations : bool
        Generate events from annotations instead of the stim channel (by
        default, annotations are used when present).
    **
        Keyword arguments for loading the raw file (see
        :func:`mne.io.read_raw_kit` or :func:`mne.io.read_raw_kit`).

    Returns
    -------
    events : Dataset
        A Dataset with the following variables:
         - *i_start*: the index of the event in the raw file.
         - *trigger*: the event value/id.
         - *event*: the event label (only for events from annotations).
        The Dataset's info dictionary contains the following values:
         - *raw*: the mne Raw object.

    """
    if (raw is None and events is None) or isinstance(raw, (str, Path)):
        raw = mne_raw(raw, proj=proj, **kwargs)

    if bads is not None and raw is not None :
        raw.info['bads'].extend(bads)

    if name is None and raw is not None:
        raw_path = raw.filenames[0]
        if isinstance(raw_path, str):
            name = os.path.basename(raw_path)
        else:
            name = None

    labels = None
    if events is None:
        if annotations is None:
            regex = re.compile('(bad|edge)', re.IGNORECASE)
            index = [not regex.match(desc) for desc in raw.annotations.description]
            if any(index):
                annotations = raw.annotations[index]

        if annotations:
            evts, event_ids = mne.events_from_annotations(raw)
        else:
            raw.load_data()
            if merge is None:
                if raw.info.get('kit_system_id') is None:
                    merge = 0
                else:
                    merge = -1
            evts = mne.find_stim_steps(raw, merge=merge, stim_channel=stim_channel)
            evts = evts[np.flatnonzero(evts[:, 2])]
            event_ids = getattr(raw, 'event_id', None)

        if event_ids:
            labels = {event_id: label for label, event_id in event_ids.items()}
    else:
        evts = mne.read_events(events)

    ds = Dataset({
        'i_start': Var(evts[:, 0]),
        'trigger': Var(evts[:, 2]),
    }, name, info={'raw': raw})
    if labels is not None:
        ds['event'] = Factor(ds['trigger'], labels=labels)
    return ds


def find_mne_channel_types(info):
    chs = {(ch['kind'], ch['unit']) for ch in info['chs']}
    types = {ch[0] for ch in chs}
    if FIFF.FIFFV_MEG_CH in types:
        units = {ch[1] for ch in chs if ch[0] == FIFF.FIFFV_MEG_CH}
        mag = FIFF.FIFF_UNIT_T in units
        grad = FIFF.FIFF_UNIT_T_M in units
    else:
        mag = grad = False
    eeg = FIFF.FIFFV_EEG_CH in types
    eog = FIFF.FIFFV_EOG_CH in types
    out = []
    if mag:
        out.append('mag')
    if grad:
        out.append('planar1')
        out.append('planar2')
    if eeg:
        out.append('eeg')
    if eog:
        out.append('eog')
    return out


def _guess_ndvar_data_type(info):
    """Guess which type of data to extract from an mne object.

    Checks for the presence of channels in that order: "mag", "eeg", "grad".
    If none are found, a ValueError is raised.

    Parameters
    ----------
    info : dict
        MNE info dictionary.

    Returns
    -------
    data : str
        Kind of data to extract
    """
    data_types = find_mne_channel_types(info)
    if data_types:
        return data_types[0]
    else:
        raise ValueError("No MEG, EEG or EOG channel found in data")


def _picks(info, data, exclude) -> np.ndarray:
    if data is None:
        data = _guess_ndvar_data_type(info)
    if data == 'eeg':
        meg = False
        eeg = True
        eog = False
    elif data == 'eog':
        meg = False
        eeg = False
        eog = True
    elif data == 'eeg&eog':
        meg = False
        eeg = True
        eog = True
    elif data in ['grad', 'mag', 'planar1', 'planar2']:
        meg = data
        eeg = False
        eog = False
    elif data is True:
        meg = True
        eeg = True
        eog = False
    else:
        raise ValueError(f"data={data!r} (needs to be one of: eeg, eog, mag, grad, planar1, planar2)")
    return mne.pick_types(info, meg, eeg, False, eog, ref_meg=False, exclude=exclude)


def _ndvar_epochs_reject(data, reject):
    if reject:
        if not np.isscalar(reject):
            err = ("Reject must be scalar (rejection threshold); got %s." %
                   repr(reject))
            raise ValueError(err)
        reject = {data: reject}
    else:
        reject = None
    return reject


def _sensor_info(data, vmax, mne_info, user_info=None, mult=1):
    if data == 'eeg' or data == 'eog' or data == 'eeg&eog':
        info = _info.for_eeg(vmax, mult)
        summary_vmax = 0.1 * vmax if vmax else None
        summary_info = _info.for_eeg(summary_vmax, mult)
    elif data == 'mag':
        info = _info.for_meg(vmax, mult)
        summary_vmax = 0.1 * vmax if vmax else None
        summary_info = _info.for_meg(summary_vmax, mult)
    elif data in ['grad', 'planar1', 'planar2']:
        info = _info.for_meg(vmax, mult, 'T/cm', '∆U')
        summary_vmax = 0.1 * vmax if vmax else None
        summary_info = _info.for_meg(summary_vmax, mult, 'T/cm', '∆U')
    else:
        raise ValueError("data=%r" % data)
    info.update(proj='z root', samplingrate=mne_info['sfreq'], summary_info=summary_info)
    if user_info:
        info.update(user_info)
    return info


def epochs(ds, tmin=-0.1, tmax=None, baseline=None, decim=1, mult=1, proj=False,
           data=None, reject=None, exclude='bads', info=None, name=None,
           raw=None, sensors=None, i_start='i_start', tstop=None, sysname=None):
    """
    Load epochs as :class:`NDVar`.

    Parameters
    ----------
    ds : Dataset
        Dataset containing a variable which defines epoch cues (i_start).
    tmin : scalar
        First sample to include in the epochs in seconds (Default is -0.1).
    tmax : scalar
        Last sample to include in the epochs in seconds (Default 0.6; use
        ``tstop`` instead to specify index exclusive of last sample).
    baseline : (float, float) | None
        Time interval for baseline correction. ``(tmin, tmax)`` tuple in
        seconds, or ``None`` to use all the data (e.g., ``(None, 0)`` uses all
        the data from the beginning of the epoch up to ``t = 0``). Set to
        ``None`` for no baseline correction (default).
    decim : int
        Downsample the data by this factor when importing. ``1`` means no
        downsampling. Note that this function does not low-pass filter
        the data. The data is downsampled by picking out every
        n-th sample (see `Wikipedia <http://en.wikipedia.org/wiki/Downsampling>`_).
    mult : scalar
        multiply all data by a constant.
    proj : bool
        mne.Epochs kwarg (subtract projections when loading data)
    data : 'eeg' | 'mag' | 'grad'
        Which data channels data to include (default based on channels in data).
    reject : None | scalar
        Threshold for rejecting epochs (peak to peak). Requires a for of
        mne-python which implements the Epochs.model['index'] variable.
    exclude : list of string | str
        Channels to exclude (:func:`mne.pick_types` kwarg).
        If 'bads' (default), exclude channels in info['bads'].
        If empty do not exclude any.
    info : None | dict
        Entries for the ndvar's info dict.
    name : str
        name for the new NDVar.
    raw : None | mne Raw
        Raw file providing the data; if ``None``, ``ds.info['raw']`` is used.
    sensors : None | Sensor
        The default (``None``) reads the sensor locations from the fiff file.
        If the fiff file contains incorrect sensor locations, a different
        Sensor instance can be supplied through this kwarg.
    i_start : str
        name of the variable containing the index of the events.
    tstop : scalar
        Alternative to ``tmax``: While ``tmax`` specifies the last samples to 
        include, ``tstop`` can be used to specify the epoch time excluding the 
        last time point (i.e., standard Python/Eelbrain indexing convention).
        For example, at 100 Hz the epoch with ``tmin=-0.1, tmax=0.4`` will have 
        51 samples, while the epoch specified with ``tmin=-0.1, tstop=0.4`` will
        have 50 samples.
    sysname : str
        Name of the sensor system to load sensor connectivity (e.g. 'neuromag',
        inferred automatically for KIT data converted with a recent version of
        MNE-Python).

    Returns
    -------
    epochs : NDVar
        The epochs as NDVar object.
    """
    if raw is None:
        raw = ds.info['raw']

    if data is None:
        data = _guess_ndvar_data_type(raw.info)
    picks = _picks(raw.info, data, exclude)
    reject = _ndvar_epochs_reject(data, reject)

    epochs_ = mne_epochs(ds, tmin, tmax, baseline, i_start, raw, decim=decim,
                         picks=picks, reject=reject, proj=proj, tstop=tstop)
    ndvar = epochs_ndvar(epochs_, name, data, mult=mult, info=info,
                         sensors=sensors, sysname=sysname)

    if len(epochs_) == 0:
        raise RuntimeError(f"No events left in {raw.filenames[0]}")
    return ndvar


def add_epochs(ds, tmin=-0.1, tmax=0.6, baseline=None, decim=1, mult=1,
               proj=False, data=None, reject=None, exclude='bads', info=None,
               name="meg", raw=None, sensors=None, i_start='i_start',
               sysname=None, tstop=None):
    """
    Load epochs and add them to a dataset as :class:`NDVar`.

    Unless the ``reject`` argument is specified, ``ds``
    is modified in place. With ``reject``, a subset of ``ds`` is returned
    containing only those events for which data was loaded.

    Parameters
    ----------
    ds : Dataset
        Dataset containing a variable which defines epoch cues (i_start) and to
        which the epochs are added.
    tmin : scalar
        First sample to include in the epochs in seconds (Default is -0.1).
    tmax : scalar
        Last sample to include in the epochs in seconds (Default 0.6; use
        ``tstop`` instead to specify index exclusive of last sample).
    baseline : (float, float) | None
        Time interval for baseline correction. ``(tmin, tmax)`` tuple in
        seconds, or ``None`` to use all the data (e.g., ``(None, 0)`` uses all
        the data from the beginning of the epoch up to ``t = 0``). Set to
        ``None`` for no baseline correction (default).
    decim : int
        Downsample the data by this factor when importing. ``1`` means no
        downsampling. Note that this function does not low-pass filter
        the data. The data is downsampled by picking out every
        n-th sample (see `Wikipedia <http://en.wikipedia.org/wiki/Downsampling>`_).
    mult : scalar
        multiply all data by a constant.
    proj : bool
        mne.Epochs kwarg (subtract projections when loading data)
    data : 'eeg' | 'mag' | 'grad'
        Which data channels data to include (default based on channels in data).
    reject : None | scalar
        Threshold for rejecting epochs (peak to peak). Requires a for of
        mne-python which implements the Epochs.model['index'] variable.
    exclude : list of string | str
        Channels to exclude (:func:`mne.pick_types` kwarg).
        If 'bads' (default), exclude channels in info['bads'].
        If empty do not exclude any.
    info : None | dict
        Entries for the ndvar's info dict.
    name : str
        name for the new NDVar.
    raw : None | mne Raw
        Raw file providing the data; if ``None``, ``ds.info['raw']`` is used.
    sensors : None | Sensor
        The default (``None``) reads the sensor locations from the fiff file.
        If the fiff file contains incorrect sensor locations, a different
        Sensor instance can be supplied through this kwarg.
    i_start : str
        name of the variable containing the index of the events.
    sysname : str
        Name of the sensor system to load sensor connectivity (e.g. 'neuromag',
        inferred automatically for KIT data converted with a recent version of
        MNE-Python).
    tstop : scalar
        Alternative to ``tmax``: While ``tmax`` specifies the last samples to 
        include, ``tstop`` can be used to specify the epoch time excluding the 
        last time point (i.e., standard Python/Eelbrain indexing convention).
        For example, at 100 Hz the epoch with ``tmin=-0.1, tmax=0.4`` will have 
        51 samples, while the epoch specified with ``tmin=-0.1, tstop=0.4`` will
        have 50 samples.

    Returns
    -------
    ds : Dataset
        Dataset containing the epochs. If no events are rejected, ``ds`` is the
        same object as the input ``ds`` argument, otherwise a copy of it.
    """
    if raw is None:
        raw = ds.info['raw']

    if data is None:
        data = _guess_ndvar_data_type(raw.info)
    picks = _picks(raw.info, data, exclude)
    reject = _ndvar_epochs_reject(data, reject)

    epochs_ = mne_epochs(ds, tmin, tmax, baseline, i_start, raw, decim=decim,
                         picks=picks, reject=reject, proj=proj, tstop=tstop)
    ds = _trim_ds(ds, epochs_)
    ds[name] = epochs_ndvar(epochs_, name, data, mult=mult, info=info,
                            sensors=sensors, sysname=sysname)
    return ds


def add_mne_epochs(ds, tmin=-0.1, tmax=None, baseline=None, target='epochs',
                   **kwargs):
    """
    Load epochs and add them to a dataset as :class:`mne.Epochs`.

    If, after loading, the Epochs contain fewer cases than the Dataset, a copy
    of the Dataset is made containing only those events also contained in the
    Epochs. Note that the Epochs are always loaded with ``preload==True``.

    If the Dataset's info dictionary contains a 'bad_channels' entry, those bad
    channels are added to the epochs.


    Parameters
    ----------
    ds : Dataset
        Dataset with events from a raw fiff file (i.e., created by
        load.fiff.events).
    tmin : scalar
        First sample to include in the epochs in seconds (Default is -0.1).
    tmax : scalar
        Last sample to include in the epochs in seconds (Default 0.6; use
        ``tstop`` instead to specify index exclusive of last sample).
    baseline : (float, float) | None
        Time interval for baseline correction. ``(tmin, tmax)`` tuple in
        seconds, or ``None`` to use all the data (e.g., ``(None, 0)`` uses all
        the data from the beginning of the epoch up to ``t = 0``). Set to
        ``None`` for no baseline correction (default).
    target : str
        Name for the Epochs object in the Dataset.
    ...
        See :func:`~eelbrain.load.fiff.mne_epochs`.
    """
    epochs_ = mne_epochs(ds, tmin, tmax, baseline, **kwargs)
    ds = _trim_ds(ds, epochs_)
    ds[target] = epochs_
    return ds


def _mne_events(ds=None, i_start='i_start', trigger='trigger'):
    """Convert events from a Dataset into mne events"""
    if isinstance(i_start, str):
        i_start = ds[i_start]

    N = len(i_start)

    if isinstance(trigger, str):
        trigger = ds[trigger]
    elif trigger is None:
        trigger = np.ones(N)

    events = np.empty((N, 3), dtype=np.int32)
    events[:, 0] = i_start.x
    events[:, 1] = 0
    events[:, 2] = trigger
    return events


def mne_epochs(ds, tmin=-0.1, tmax=None, baseline=None, i_start='i_start',
               raw=None, drop_bad_chs=True, picks=None, reject=None, tstop=None,
               decim=1, **kwargs):
    """Load epochs as :class:`mne.Epochs`.

    Parameters
    ----------
    ds : Dataset
        Dataset containing a variable which defines epoch cues (i_start).
    tmin : scalar
        First sample to include in the epochs in seconds (Default is -0.1).
    tmax : scalar
        Last sample to include in the epochs in seconds (Default 0.6; use
        ``tstop`` instead to specify index exclusive of last sample).
    baseline : (float, float) | None
        Time interval for baseline correction. ``(tmin, tmax)`` tuple in
        seconds, or ``None`` to use all the data (e.g., ``(None, 0)`` uses all
        the data from the beginning of the epoch up to ``t = 0``). Set to
        ``None`` for no baseline correction (default).
    i_start : str
        name of the variable containing the index of the events.
    raw : None | mne Raw
        If None, ds.info['raw'] is used.
    drop_bad_chs : bool
        Drop all channels in raw.info['bads'] form the Epochs. This argument is
        ignored if the picks argument is specified.
    picks, reject
        :class:`mne.Epochs` parameters.
    tstop : scalar
        Alternative to ``tmax``: While ``tmax`` specifies the last samples to 
        include, ``tstop`` can be used to specify the epoch time excluding the 
        last time point (i.e., standard Python/Eelbrain indexing convention).
        For example, at 100 Hz the epoch with ``tmin=-0.1, tmax=0.4`` will have 
        51 samples, while the epoch specified with ``tmin=-0.1, tstop=0.4`` will
        have 50 samples.
    ...
        :class:`mne.Epochs` parameters.
    """
    if baseline is False:
        baseline = None
    if raw is None:
        raw = ds.info['raw']
    if tmax is None:
        if tstop is None:
            tmax = 0.6
        else:
            sfreq = raw.info['sfreq'] / decim
            start_index = int(round(tmin * sfreq))
            stop_index = int(round(tstop * sfreq))
            tmax = tmin + (stop_index - start_index - 1) / sfreq
    elif tstop is not None:
        raise TypeError(f"tmax and tstop can not both be specified at the same time, got tmax={tmax}, tstop={tstop}")

    if drop_bad_chs and picks is None and raw.info['bads']:
        picks = mne.pick_types(raw.info, meg=True, eeg=True, eog=True, ref_meg=False)

    events = _mne_events(ds=ds, i_start=i_start)
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', 'The events passed to the Epochs constructor', RuntimeWarning)
        epochs = mne.Epochs(raw, events, None, tmin, tmax, baseline, picks, preload=True, reject=reject, decim=decim, **kwargs)
    if reject is None and len(epochs) != len(events):
        getLogger('eelbrain').warning("%s: MNE generated only %i Epochs for %i events. The raw file might end before the end of the last epoch.", raw.filenames[0], len(epochs), len(events))

    #  add bad channels from ds
    if BAD_CHANNELS in ds.info:
        invalid = []
        for ch_name in ds.info[BAD_CHANNELS]:
            if ch_name in raw.info['bads']:
                pass
            elif ch_name not in epochs.ch_names:
                invalid.append(ch_name)
            elif ch_name not in epochs.info['bads']:
                epochs.info['bads'].append(ch_name)
        if invalid:
            raise ValueError(f"{n_of(len(invalid), 'invalid channel')} in ds.info[{BAD_CHANNELS!r}]: {', '.join(invalid)}")

    return epochs


def sensor_dim(
        info: mne.Info,
        picks: np.ndarray = None,
        sysname: str = None,
        connectivity: Union[str, Sequence] = None,
):
    """Create a :class:`Sensor` dimension from an :class:`mne.Info` object.

    Parameters
    ----------
    info
        Measurement info dictionary (or mne-python object that has a ``.info``
        attribute that contains measurement info).
    picks
        Channel picks (integer array, as used in mne-python).
        By default all MEG and EEG channels are included.
    sysname
        Name of the sensor system to load sensor connectivity (e.g. 'neuromag',
        inferred automatically for KIT data converted with a recent version of
        MNE-Python).
    connectivity : str | list of (str, str) | array of int, (n_edges, 2)
        Connectivity between elements. Can be specified as:

        - ``"none"`` for no connections
        - list of connections (e.g., ``[('OZ', 'O1'), ('OZ', 'O2'), ...]``)
        - :class:`numpy.ndarray` of int, shape (n_edges, 2), to specify
          connections in terms of indices. Each row should specify one
          connection [i, j] with i < j. If the array's dtype is uint32,
          property checks are disabled to improve efficiency.
        - ``"grid"`` to use adjacency in the sensor names

        If unspecified, it is inferred from ``sysname`` if possible.

    Returns
    -------
    sensor_dim : Sensor
        Sensor dimension object.
    """
    if not isinstance(info, mne.Info):
        info_ = getattr(info, 'info', info)
        if not isinstance(info_, mne.Info):
            raise TypeError("No mne.Info object: %r" % (info,))
        info = info_

    if picks is None:
        picks = mne.pick_types(info, meg=True, eeg=True, ref_meg=False, exclude=())
    else:
        picks = np.asarray(picks, int)

    chs = [info['chs'][i] for i in picks]
    ch_locs = [ch['loc'][:3] for ch in chs]
    ch_names = [ch['ch_name'] for ch in chs]

    # use KIT system ID if available
    sysname = KIT_NEIGHBORS.get(info.get('kit_system_id'), sysname)
    if sysname and sysname.startswith('neuromag'):
        ch_unit = {ch['unit'] for ch in chs}
        if len(ch_unit) > 1:
            raise RuntimeError(f"More than one channel kind for sysname={sysname!r}: {tuple(ch_unit)}")
        ch_unit = ch_unit.pop()
        if ch_unit == FIFF.FIFF_UNIT_T_M:
            sysname = 'neuromag306planar'
        elif ch_unit == FIFF.FIFF_UNIT_T:
            sysname = 'neuromag306mag'
        elif ch_unit == FIFF.FIFF_UNIT_V:
            sysname = 'neuromag306eeg'
            if connectivity is None:
                connectivity = 'auto'
        else:
            raise ValueError(f"Unknown channel unit for sysname={sysname!r}: {ch_unit!r}")

    if connectivity is None:
        connectivity = sysname  # or 'auto'

    if connectivity in ('grid', 'none'):
        pass
    elif isinstance(connectivity, str):
        if connectivity == 'auto':
            ch_type = _guess_ndvar_data_type({'chs': chs})
            c_matrix, names = mne.channels.find_ch_adjacency(info, ch_type)
        else:
            c_matrix, names = mne.channels.read_ch_adjacency(connectivity)
            if connectivity.startswith('neuromag'):
                vec_ids = {name[-1] for name in ch_names}
                if len(vec_ids) > 1:
                    raise NotImplementedError("Connectivity for Neuromag vector data")
                vec_id = vec_ids.pop()
                # fix channel names
                names = [f'MEG {n[3:-1]}{vec_id}' for n in names]

        # fix channel order
        if names != ch_names:
            index = np.array([names.index(name) for name in ch_names])
            c_matrix = c_matrix[index][:, index]

        connectivity = _matrix_graph(c_matrix)
    elif connectivity in (None, False):
        connectivity = 'none'

    return Sensor(ch_locs, ch_names, sysname, connectivity=connectivity)


def variable_length_mne_epochs(ds, tmin, tmax, baseline=None, allow_truncation=False, picks=None, **kwargs):
    """Load mne Epochs where each epoch has a different length

    Parameters
    ----------
    ds : Dataset
        Dataset containing a variable which defines epoch cues (i_start).
    tmin : scalar
        First sample to include in the epochs in seconds (Default is -0.1).
    tmax : sequence of scalar
        Last sample to include in each epoch in seconds.
    baseline : (float, float) | None
        Time interval for baseline correction. ``(tmin, tmax)`` tuple in
        seconds, or ``None`` to use all the data (e.g., ``(None, 0)`` uses all
        the data from the beginning of the epoch up to ``t = 0``). Set to
        ``None`` for no baseline correction (default).
    allow_truncation : bool
        If a ``tmax`` value falls outside the data available in ``raw``,
        automatically truncate the epoch (by default this raises a
        ``ValueError``).
    ...
        :class:`mne.Epochs` parameters.
    """
    if baseline is False:
        baseline = None
    raw = ds.info['raw']
    if picks is None and raw.info['bads']:
        picks = mne.pick_types(raw.info, meg=True, eeg=True, eog=True, ref_meg=False, exclude=[])
    events = _mne_events(ds)
    out = []
    for i, tmax_i in enumerate(tmax):
        i_max = events[i, 0] + floor(tmax_i * raw.info['sfreq'])
        if raw.last_samp < i_max:
            if allow_truncation:
                tmax_i = (raw.last_samp - events[i, 0]) / raw.info['sfreq']
            else:
                missing = (i_max - raw.last_samp) / raw.info['sfreq']
                raise ValueError(f"tmax={tmax}, tmax[{i}] {tmax_i} is outside of data range by {missing:g} s")
        epochs_i = mne.Epochs(raw, events[i:i+1], None, tmin, tmax_i, baseline, picks, preload=True, **kwargs)
        out.append(epochs_i)
    return out


def raw_ndvar(raw, i_start=None, i_stop=None, decim=1, data=None, exclude='bads', sysname=None,  connectivity=None):
    """Raw data as NDVar

    Parameters
    ----------
    raw : Raw | str
        Raw instance, or path of a raw FIFF file..
    i_start : int | sequence of int
        Start sample (see notes; default is the beginning of the ``raw``).
    i_stop : int | sequence of int
        Stop sample (see notes; default is end of the ``raw``).
    decim : int
        Downsample the data by this factor when importing. ``1`` (default)
        means no downsampling. Note that this function does not low-pass filter
        the data. The data is downsampled by picking out every n-th sample.
    data : 'eeg' | 'mag' | 'grad' | None
        The kind of data to include (default based on data).
    exclude : list of string | str
        Channels to exclude (:func:`mne.pick_types` kwarg).
        If 'bads' (default), exclude channels in info['bads'].
        If empty do not exclude any.
    sysname : str
        Name of the sensor system to load sensor connectivity (e.g. 'neuromag306',
        inferred automatically for KIT data converted with a recent version of
        MNE-Python).
    connectivity : str | list of (str, str) | array of int, (n_edges, 2)
        Connectivity between elements. Can be specified as:

        - ``"none"`` for no connections
        - list of connections (e.g., ``[('OZ', 'O1'), ('OZ', 'O2'), ...]``)
        - :class:`numpy.ndarray` of int, shape (n_edges, 2), to specify
          connections in terms of indices. Each row should specify one
          connection [i, j] with i < j. If the array's dtype is uint32,
          property checks are disabled to improve efficiency.
        - ``"grid"`` to use adjacency in the sensor names

        If unspecified, it is inferred from ``sysname`` if possible.

    Returns
    -------
    data : NDVar | list of NDVar
        Data (sensor or source space). If ``i_start`` and ``i_stopr`` are scalar
        then a single NDVar is returned, if they are lists then a list of NDVars
        is returned.

    Notes
    -----
    ``i_start`` and ``i_stop`` are interpreted as event indexes (from
    :func:`mne.find_events`), i.e. relative to ``raw.first_samp``.
    """
    if not isinstance(raw, MNE_RAW):
        raw = mne_raw(raw)
    if raw.filenames and raw.filenames[0]:
        name = os.path.basename(raw.filenames[0])
    else:
        name = None
    start_scalar = i_start is None or isinstance(i_start, int)
    stop_scalar = i_stop is None or isinstance(i_stop, int)
    if start_scalar != stop_scalar:
        raise TypeError(f"i_start and i_stop must either both be scalar or both iterable, got i_start={i_start!r}, i_stop={i_stop!r}")
    elif start_scalar:
        i_start = (i_start,)
        i_stop = (i_stop,)
        scalar = True
    else:
        scalar = False

    # event index to raw index
    i_start = [i if i is None else i - raw.first_samp for i in i_start]
    i_stop = [i if i is None else i - raw.first_samp for i in i_stop]

    # target dimension
    if data is None:
        data = _guess_ndvar_data_type(raw.info)
    picks = _picks(raw.info, data, exclude)
    dim = sensor_dim(raw, picks, sysname, connectivity)
    info = _sensor_info(data, None, raw.info)

    out = []
    for start, stop in zip(i_start, i_stop):
        x = raw[picks, start:stop][0]

        if decim != 1:
            x = x[:, ::decim]
        time = UTS(0, float(decim) / raw.info['sfreq'], x.shape[1])
        out.append(NDVar(x, (dim, time), name, info))

    if scalar:
        return out[0]
    else:
        return out


def epochs_ndvar(epochs, name=None, data=None, exclude='bads', mult=1,
                 info=None, sensors=None, vmax=None, sysname=None,
                 connectivity=None):
    """
    Convert an :class:`mne.Epochs` object to an :class:`NDVar`.

    Parameters
    ----------
    epochs : mne.Epochs | str
        The epochs object or path to an epochs FIFF file.
    name : None | str
        Name for the NDVar.
    data : 'eeg' | 'mag' | 'grad'
        Which data channels data to include (default based on channels in data).
    exclude : list of string | str
        Channels to exclude (:func:`mne.pick_types` kwarg).
        If 'bads' (default), exclude channels in info['bads'].
        If empty do not exclude any.
    mult : scalar
        multiply all data by a constant.
    info : None | dict
        Additional contents for the info dictionary of the NDVar.
    sensors : None | Sensor
        The default (``None``) reads the sensor locations from the fiff file.
        If the fiff file contains incorrect sensor locations, a different
        Sensor can be supplied through this kwarg.
    vmax : None | scalar
        Set a default range for plotting.
    sysname : str
        Name of the sensor system to load sensor connectivity (e.g. 'neuromag306',
        inferred automatically for KIT data converted with a recent version of
        MNE-Python).
    connectivity : str | list of (str, str) | array of int, (n_edges, 2)
        Connectivity between elements. Can be specified as:

        - ``"none"`` for no connections
        - list of connections (e.g., ``[('OZ', 'O1'), ('OZ', 'O2'), ...]``)
        - :class:`numpy.ndarray` of int, shape (n_edges, 2), to specify
          connections in terms of indices. Each row should specify one
          connection [i, j] with i < j. If the array's dtype is uint32,
          property checks are disabled to improve efficiency.
        - ``"grid"`` to use adjacency in the sensor names

        If unspecified, it is inferred from ``sysname`` if possible.
    """
    if isinstance(epochs, str):
        epochs = mne.read_epochs(epochs)

    if data is None:
        data = _guess_ndvar_data_type(epochs.info)
    picks = _picks(epochs.info, data, exclude)
    info_ = _sensor_info(data, vmax, epochs.info, info, mult)

    x = epochs.get_data()
    if len(picks) < x.shape[1]:
        x = x[:, picks]

    if mult != 1:
        x *= mult

    sensor = sensors or sensor_dim(epochs, picks, sysname, connectivity)
    time = UTS(epochs.times[0], 1. / epochs.info['sfreq'], len(epochs.times))
    return NDVar(x, ('case', sensor, time), info=info_, name=name)


def evoked_ndvar(evoked, name=None, data=None, exclude='bads', vmax=None,
                 sysname=None, connectivity=None):
    """
    Convert one or more mne :class:`Evoked` objects to an :class:`NDVar`.

    Parameters
    ----------
    evoked : str | Evoked | list of Evoked
        The Evoked to convert to NDVar. Can be a string designating a file
        path to a evoked fiff file containing only one evoked.
    name : str
        Name of the NDVar.
    data : 'eeg' | 'mag' | 'grad'
        Which data channels data to include (default based on channels in data).
    exclude : list of string | string
        Channels to exclude (:func:`mne.pick_types` kwarg).
        If 'bads' (default), exclude channels in info['bads'].
        If empty do not exclude any.
    vmax : None | scalar
        Set a default range for plotting.
    sysname : str
        Name of the sensor system to load sensor connectivity (e.g. 'neuromag306',
        inferred automatically for KIT data converted with a recent version of
        MNE-Python).
    connectivity : str | list of (str, str) | array of int, (n_edges, 2)
        Connectivity between elements. Can be specified as:

        - ``"none"`` for no connections
        - list of connections (e.g., ``[('OZ', 'O1'), ('OZ', 'O2'), ...]``)
        - :class:`numpy.ndarray` of int, shape (n_edges, 2), to specify
          connections in terms of indices. Each row should specify one
          connection [i, j] with i < j. If the array's dtype is uint32,
          property checks are disabled to improve efficiency.
        - ``"grid"`` to use adjacency in the sensor names

        If unspecified, it is inferred from ``sysname`` if possible.

    Notes
    -----
    If evoked objects have different channels, the intersection is used (i.e.,
    only the channels present in all objects are retained).
    """
    if isinstance(evoked, str):
        evoked = mne.read_evokeds(evoked)

    if isinstance(evoked, MNE_EVOKED):
        case_out = False
        evoked = (evoked,)
    elif isinstance(evoked, (tuple, list)):
        case_out = True
    else:
        raise TypeError("evoked=%s" % repr(evoked))

    # data type to load
    if data is None:
        data_set = {_guess_ndvar_data_type(e.info) for e in evoked}
        if len(data_set) > 1:
            raise ValueError("Different Evoked objects contain different "
                             "data types: %s" % ', '.join(data_set))
        data = data_set.pop()

    # MEG system
    kit_sys_ids = {e.info.get('kit_system_id') for e in evoked}
    kit_sys_ids -= {None}
    if len(kit_sys_ids) > 1:
        raise ValueError("Evoked objects from different KIT systems can not be "
                         "combined because they have different sensor layouts")
    elif kit_sys_ids:
        sysname = KIT_NEIGHBORS.get(kit_sys_ids.pop(), sysname)

    if data == 'mag':
        info = _info.for_meg(vmax)
    elif data == 'eeg':
        info = _info.for_eeg(vmax)
    elif data == 'grad':
        info = _info.for_meg(vmax, unit='T/cm')
    else:
        raise ValueError("data=%s" % repr(data))

    e0 = evoked[0]
    if len(evoked) == 1:
        picks = _picks(e0.info, data, exclude)
        x = e0.data[picks]
        if case_out:
            x = x[None, :]
        first, last, sfreq = e0.first, e0.last, e0.info['sfreq']
    else:
        # timing:  round sfreq because precision is lost by FIFF format
        timing_set = {(e.first, e.last, e.info['sfreq']) for e in evoked}
        if len(timing_set) == 1:
            first, last, sfreq = timing_set.pop()
        else:
            raise ValueError(f"Evoked objects have different timing information (first, last, sfreq): {', '.join(map(str, timing_set))}")

        # find excluded channels
        ch_sets = [set(e.info['ch_names']) for e in evoked]
        all_chs = set.union(*ch_sets)
        common = set.intersection(*ch_sets)
        exclude = set.union(*list(map(set, (e.info['bads'] for e in evoked))))
        exclude.update(all_chs.difference(common))
        exclude = list(exclude)

        # get data
        x = []
        for e in evoked:
            picks = _picks(e.info, data, exclude)
            x.append(e.data[picks])

    sensor = sensor_dim(e0, picks, sysname, connectivity)
    time = UTS.from_int(first, last, sfreq)
    if case_out:
        dims = ('case', sensor, time)
    else:
        dims = (sensor, time)
    return NDVar(x, dims, name, info)


def forward_operator(fwd, src, subjects_dir=None, parc='aparc', name=None):
    """Load forward operator as :class:`NDVar`

    Parameters
    ----------
    fwd : str | mne Forward
        MNE Forward solution, or path to forward solution.
    src : str
        Tag describing the source space (e.g., "ico-4").
    subjects_dir : str
        Location of the MRI subjects directory.
    parc : str
        Parcellation to load (corresponding to existing annot files; default
        'aparc').
    name : str
        Name the NDVar (default is the filename if a path is provided,
        otherwise "fwd").

    Returns
    -------
    fwd : NDVar  (sensor, source)
        NDVar containing the gain matrix.
    """
    is_vol = src.startswith('vol')
    if isinstance(fwd, str):
        if name is None:
            name = os.path.basename(fwd)
        fwd = mne.read_forward_solution(fwd)
        mne.convert_forward_solution(fwd, force_fixed=not is_vol, use_cps=True,
                                     copy=False)
    elif name is None:
        name = 'fwd'
    sensor = sensor_dim(fwd['info'])
    assert np.all(sensor.names == fwd['sol']['row_names'])
    subject = fwd['src'][0]['subject_his_id']
    if is_vol:
        source = VolumeSourceSpace.from_file(subjects_dir, subject, src, parc, source_spaces=fwd['src'])
        x = fwd['sol']['data'].reshape((len(sensor), len(source), 3))
        dims = (sensor, source, Space('RAS'))
    else:
        source = SourceSpace.from_file(subjects_dir, subject, src, parc, source_spaces=fwd['src'])
        x = fwd['sol']['data']
        dims = (sensor, source)
    return NDVar(x, dims, name)


def inverse_operator(inv, src, subjects_dir=None, parc='aparc', name=None):
    """Load inverse operator as :class:`NDVar`
    
    Parameters
    ----------
    inv : str | mne.minimum_norm.InverseOperator
        MNE inverse operator, or path to inverse operator.
    src : str
        Tag describing the source space (e.g., "ico-4").
    subjects_dir : str
        Location of the MRI subjects directory.
    parc : str
        Parcellation to load (corresponding to existing annot files; default
        'aparc').
    name : str
        Name the NDVar (default is the filename if a path is provided,
        otherwise "inv").

    Returns
    -------
    inv : NDVar  (source, sensor)
        NDVar containing the inverse operator.
    """
    if isinstance(inv, str):
        if name is None:
            name = os.path.basename(inv)
        inv = mne.minimum_norm.read_inverse_operator(inv)
    elif name is None:
        name = 'inv'
    sensor = sensor_dim(inv['info'], _picks(inv['info'], True, 'bads'))
    assert np.all(sensor.names == inv['eigen_fields']['col_names'])
    subject = inv['src'][0]['subject_his_id']
    source = SourceSpace.from_file(subjects_dir, subject, src, parc, source_spaces=inv['src'])
    inv = mne.minimum_norm.prepare_inverse_operator(inv, 1, 1., 'MNE')
    k = mne.minimum_norm.inverse._assemble_kernel(inv, None, 'MNE', False)[0]
    return NDVar(k, (source, sensor), {}, name)


def stc_ndvar(
        stc: Union[_BaseSourceEstimate, Sequence[_BaseSourceEstimate], PathArg],
        subject: str,
        src: str,
        subjects_dir: PathArg = None,
        method: str = None,
        fixed: bool = None,
        name: str = None,
        check: bool = True,
        parc: Union[str, None] = 'aparc',
        connectivity: str = None,
        sss_filename: str = '{subject}-{src}-src.fif',
):
    """
    Convert one or more :class:`mne.SourceEstimate` objects to an :class:`NDVar`.

    Parameters
    ----------
    stc : SourceEstimate | list of SourceEstimates | str
        The source estimate object(s) or a path to an stc file. Volum and vector
        source estimates are supported.
    subject
        MRI subject (used for loading MRI in PySurfer plotting)
    src
        The kind of source space used (e.g., 'ico-4').
    subjects_dir
        The path to the subjects_dir (needed to locate the source space file).
    method : 'MNE' | 'dSPM' | 'sLORETA' | 'eLORETA'
        Source estimation method (optional, used for generating info).
    fixed
        Source estimation orientation constraint (optional, used for generating
        info).
    name
        Ndvar name.
    check
        If multiple stcs are provided, check if all stcs have the same times
        and vertices.
    parc
        Name of a parcellation to add to the source space. ``None`` to add no
        parcellation.
    connectivity : 'link-midline'
        Modify source space connectivity to link medial sources of the two
        hemispheres across the midline.
    sss_filename
        Filename template for the MNE source space file.
    """
    subjects_dir = mne.utils.get_subjects_dir(subjects_dir)
    if isinstance(stc, Path):
        stc = str(stc)
    if isinstance(stc, str):
        stc = mne.read_source_estimate(stc)

    # construct data array
    if isinstance(stc, _BaseSourceEstimate):
        case = False
        stcs = None
    else:
        case = True
        stcs = stc
        stc = stcs[0]

    vertices = as_list(stc.vertices)  # not always list for mne < 0.21
    if stcs and check:
        times = stc.times
        for stc_ in stcs[1:]:
            assert np.array_equal(stc_.times, times)
            stc_vertices = as_list(stc_.vertices)
            for v1, v0 in zip_longest(stc_vertices, vertices):
                assert np.array_equal(v1, v0)

    if stcs:
        x = np.array([s.data for s in stcs])
    else:
        x = stc.data

    # Construct NDVar Dimensions
    time = UTS(stc.tmin, stc.tstep, stc.times.size)
    if isinstance(stc, MNE_VOLUME_STC):
        ss = VolumeSourceSpace(vertices, subject, src, subjects_dir, None, filename=sss_filename)
        is_vector = stc.data.ndim == 3
    elif isinstance(stc, (mne.SourceEstimate, mne.VectorSourceEstimate)):
        ss = SourceSpace(vertices, subject, src, subjects_dir, parc, filename=sss_filename)
        is_vector = isinstance(stc, mne.VectorSourceEstimate)
    else:
        raise TypeError(f"stc={stc!r}")
    # Apply connectivity modification
    if isinstance(connectivity, str):
        if connectivity == 'link-midline':
            ss._link_midline()
        elif connectivity != '':
            raise ValueError(f"connectivity={connectivity!r}")
    elif connectivity is not None:
        raise TypeError(f"connectivity={connectivity!r}")
    # assemble dims
    dims = [ss, time]
    if is_vector:
        dims.insert(1, Space('RAS'))
    if case:
        dims.insert(0, Case)

    # find the right measurement info
    info = {}
    if fixed is False:
        info['meas'] = 'Activation'
        if method:
            info['unit'] = method
    elif fixed is True:
        info['meas'] = 'Current Estimate'
        if method == 'MNE':
            info['unit'] = 'A'
        elif method:
            info['unit'] = method
    elif fixed is not None:
        raise ValueError(f"fixed={fixed!r}")

    return NDVar(x, dims, name, info)


def _trim_ds(ds, epochs):
    """Trim a Dataset to account for rejected epochs.

    If no epochs were rejected, the original ds is rturned.

    Parameters
    ----------
    ds : Dataset
        Dataset that was used to construct epochs.
    epochs : Epochs
        Epochs loaded with mne_epochs()
    """
    if len(epochs) < ds.n_cases:
        ds = ds.sub(epochs.selection)
        ds.info['epochs.selection'] = epochs.selection

    return ds
