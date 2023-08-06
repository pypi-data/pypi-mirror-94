# Author: Christian Brodbeck <christianbrodbeck@nyu.edu>
"""Statistical tests for univariate variables"""
from functools import partial
import itertools
from typing import Union, Sequence

import numpy as np
import scipy.stats

from .. import fmtxt
from .._celltable import Celltable
from .._data_obj import (
    CategorialArg, CellArg, IndexArg, VarArg, NumericArg,
    Dataset, Factor, Interaction, Var, NDVar,
    ascategorial, asfactor, asnumeric, assub, asvar, asndvar,
    combine,
    cellname, dataobj_repr, nice_label,
)
from .permutation import resample
from . import stats


__test__ = False
DEFAULT_LEVELS = {.05: '*', .01: '**', .001: '***'}
DEFAULT_LEVELS_TREND = {.05: '*', .01: '**', .001: '***', .1: '`'}


def get_levels(
        levels: Union[bool, dict],
        trend: Union[bool, str] = False,
):
    if levels is True:
        if trend is True:
            return DEFAULT_LEVELS_TREND
        elif trend:
            return {**DEFAULT_LEVELS, .1: trend}
        else:
            return DEFAULT_LEVELS
    elif trend:
        raise TypeError("trend=%r only valid when levels=True" % (trend,))
    return levels


class Correlation:
    """Pearson product moment correlation between y and x

    Parameters
    ----------
    y : Var | NDVar
        First variable.
    x : Var | NDVar
        Second variable. Needs to have same type/shape as ``y``.
    sub : index
        Use only a subset of the data
    ds : Dataset
        If a Dataset is given, all data-objects can be specified as names of
        Dataset variables.

    Attributes
    ----------
    r : float
        Pearson correlation coefficient.
    p : float
        Two-tailed p-value.
    df : int
        Degrees of freedom.
    """
    def __init__(
            self,
            y: NumericArg,
            x: NumericArg,
            sub: IndexArg = None,
            ds: Dataset = None,
    ):
        sub, n = assub(sub, ds, return_n=True)
        y, n = asnumeric(y, sub, ds, n, return_n=True, array=True)
        x = asnumeric(x, sub, ds, n, array=True)
        if type(y) is not type(x):
            raise TypeError(f"y and x must be same type; got type(y)={type(y)}, type(x)={type(x)}")
        elif isinstance(y, Var):
            x_y = y.x
            x_x = x.x
        elif isinstance(y, NDVar):
            if y.dims != x.dims:
                raise ValueError(f"y and x have different dimensions; y.dims={y.dims}, x.dims={x.dims}")
            x_y = y.x.ravel()
            x_x = x.x.ravel()
        else:
            if y.shape != x.shape:
                raise ValueError(f"Shape mismatch: y.shape={y.shape}, x.shape={x.shape}")
            x_y = y.ravel()
            x_x = x.ravel()
        self.r, self.p, self.df = _corr(x_y, x_x)
        self._y = dataobj_repr(y)
        self._x = dataobj_repr(x)

    def __repr__(self):
        return f"<Correlation: {self._y} ~ {self._x}; {self._asfmtext()}> "

    def _asfmtext(self, **_):
        return fmtxt.FMText([fmtxt.eq('r', self.r, self.df), ', ', fmtxt.peq(self.p)])


def lilliefors(data, formatted=False, **kwargs):
    """Lilliefors' test for normal distribution

    The Lilliefors test is an adaptation of the Kolmogorov-Smirnov test. It
    is used to test the null hypothesis that data come from a normally
    distributed population, when the null hypothesis does not specify which
    normal distribution, i.e. does not specify the expected value and variance.

    Parameters
    ----------
    data : array_like

    formatted : bool
        Return a single string with the results instead of the numbers.
    kwargs :
        All keyword arguments are forwarded to :func:`scipy.stats.kstest`.

    Returns
    -------
    D : float
        The D-value of the Kolmogorov-Smirnov Test
    p_estimate : float
        The approximate p value according to Dallal and Wilkinson (1986).
        Requires minimal sample size of 5. p is reasonably accurate only when
        it is <= .1 (cf. Dallal and Wilkens).

    Notes
    -----
    Uses the scipy.stats.kstest implementation of the Kolmogorov-Smirnov test.

    References
    ----------
    Dallal, G. E. and Wilkinson, L. (1986). An Analytic Approximation to the
            Distribution of Lilliefors's Test Statistic for Normality. The
            American Statistician, 40(4), 294--296.
    Lilliefors, H. W. (1967). On the Kolmogorov-Smirnov Test for Normality
            with Mean and Variance Unknown. Journal of the American
            Statistical Association, 62(318), 399--402.
    """
    # p values agree with R lillie.test (nortest package) on low values of p.
    # lillie.test adjusts something at p>.1
    # http://pbil.univ-lyon1.fr/library/nortest/R/nortest
    data = np.asarray(data)
    N = len(data)  # data.shape[-1] #axis]
    assert N >= 5, "sample size must be greater than 4"
    # perform Kolmogorov-Smirnov with estimated mean and std
    m = np.mean(data)  # , axis=axis)
    s = np.std(data, ddof=1)  # , axis=axis)
    D, ks_p = scipy.stats.kstest(data, 'norm', args=(m, s), **kwargs)
    # approximate p (Dallal)
    if N > 100:
        D *= (N / 100) ** .49
        N = 100
    p_estimate = np.exp(- 7.01256 * D ** 2 * (N + 2.78019)
                        + 2.99587 * D * (N + 2.78019) ** .5
                        - .122119
                        + .974598 / (N ** .5)
                        + 1.67997 / N)
    # approximate P (Molin & Abdi)
    L = D  # ???
    b2 = 0.08861783849346
    b1 = 1.30748185078790
    b0 = 0.37872256037043
    A = (-(b1 + N) + np.sqrt((b1 + N) ** 2 - 4 * b2 * (b0 - L ** -2))) / 2 * b2
    Pr = (-.37782822932809
          + 1.67819837908004 * A
          - 3.02959249450445 * A ** 2
          + 2.80015798142101 * A ** 3
          - 1.39874347510845 * A ** 4
          + 0.40466213484419 * A ** 5
          - 0.06353440854207 * A ** 6
          + 0.00287462087623 * A ** 7
          + 0.00069650013110 * A ** 8
          - 0.00011872227037 * A ** 9
          + 0.00000575586834 * A ** 10)
    if formatted:
        txt = "D={0:.4f}, Dallal p={1:.4f}, Molin&Abdi p={2:.4f}"
        return txt.format(D, p_estimate, Pr)
    else:
        return D, p_estimate


def _hochberg_threshold(N, alpha=.05):
    j = np.arange(N)
    threshold = alpha / (N - j)
    return threshold


def mcp_adjust(ps, method='Hochberg'):
    """Adjust p-values for multiple comparison

    Parameters
    ----------
    ps : sequence of scalar
        P-values.
    method : 'hochberg' | 'bonferroni' | 'holm'
        Correction method. Default is 'hochberg'.

    Returns
    -------
    adjusted_ps : list of scalar
        Adjusted p-values.
    """
    if not method:
        return ps
    n = len(ps)
    if n <= 1:
        return ps
    method_ = method.lower()
    if method_ == 'bonferroni':
        ps_adjusted = [p * n for p in ps]
    elif method_ in ('hochberg', 'holm'):
        ascsort = np.argsort(ps)
        ps_asc = np.array(ps)[ascsort]
        iout_asc = np.arange(n)[ascsort]
        ps_adjusted = [-1] * n
        p_buffer = 1
        if method_ == 'holm':
            for i in range(n):
                p = ps_asc[i]
                p_adj = (n - i) * p
                p_buffer = max(p_buffer, p_adj)
                ps_adjusted[iout_asc[i]] = p_buffer
        elif method_ == 'hochberg':
            for i in range(1, n + 1):
                p = ps_asc[-i]
                p_adj = (i) * p
                p_buffer = min(p_adj, p_buffer)
                ps_adjusted[iout_asc[-i]] = p_buffer
    else:
        msg = ('%r is not a valid argument for multiple comparison correction '
               'method' % method)
        raise ValueError(msg)

    return ps_adjusted


def _get_correction_caption(corr, n):
    if corr == 'Hochberg':
        return "(* Corrected after Hochberg, 1988)"
    elif corr == 'Bonferroni':
        return "(* Bonferroni corrected for %i tests)" % n
    elif corr == 'Holm':
        return "(* Corrected after Holm)"
    else:
        return "(* Uncorrected)"


def _n_stars(p: float, levels: Sequence[float]):
    return sum(p <= l for l in levels)


def star(
        p_list: Union[float, Sequence[float]],
        out: type = str,
        levels: Union[bool, dict] = True,
        trend: Union[bool, str] = False,
        eq_strlen: bool = False,
):
    """Determine number of stars for p-value

    Parameters
    ----------
    p_list
        P-values.
    out : {str, int}
        Return string with stars ('**') or an integer indicating the number of
        stars.
    levels
        ``{p: str, ...}`` dictionary. The default is ``{.05 : '*',
        .01 : '**', .001: '***'}``; ``trend=True`` adds ``{.1: "'"}``.
    trend
        Add trend to default ``levels``.
    eq_strlen
        Equalize string lengths; when strings are returned, make sure they all
        have the same length (default ``False``).
    """
    levels = get_levels(levels, trend)

    levels_descending = sorted(levels.keys(), reverse=True)
    symbols_descending = [''] + [levels[l] for l in levels_descending]

    if out is int:
        int_out = True
    elif out is str:
        int_out = False
    else:
        raise TypeError("out=%r" % (out,))

    # allow input (p_list) to contain single p-value
    if not np.iterable(p_list):
        n = _n_stars(p_list, levels)
        if int_out:
            return out
        else:
            return symbols_descending[n]

    ns = [_n_stars(p, levels) for p in p_list]
    if int_out:
        return ns
    symbols = [symbols_descending[n] for n in ns]
    if eq_strlen:
        maxlen = max(map(len, symbols))
        return [s.ljust(maxlen) for s in symbols]
    else:
        return symbols


def star_factor(p, levels=True):
    """Create a factor with stars for a sequence of p-values

    Parameters
    ----------
    p : sequence of scalar
        Sequence of p-values.
    levels : dict {scalar: str}
        {value: star-mark} dictionary.

    Returns
    -------
    stars : Factor
        Factor with the appropriate star marking for each item in p.
    """
    levels = get_levels(levels)
    sorted_levels = sorted(levels, reverse=True)
    star_labels = {i: levels[v] for i, v in enumerate(sorted_levels, 1)}
    star_labels[0] = ''
    level_values = np.reshape(sorted_levels, (-1, 1))
    return Factor(np.sum(p <= level_values, 0), labels=star_labels)


def _independent_measures_args(y, x, c1, c0, match, ds, sub, nd_data=False):
    "Interpret parameters for independent measures tests (2 different argspecs)"
    if isinstance(x, str):
        x = ds.eval(x)

    if nd_data:
        two_y = isinstance(x, NDVar)
        coerce = asndvar
    else:
        two_y = isinstance(x, Var) and match is None
        coerce = asvar

    if two_y:
        assert match is None
        y1 = coerce(y, sub, ds)
        y0 = coerce(x, sub, ds)
        y = combine((y1, y0))
        c1_name = y1.name if c1 is None else c1
        c0_name = y0.name if c0 is None else c0
        x_name = y0.name
    else:
        ct = Celltable(y, x, match, sub, cat=(c1, c0), ds=ds, coercion=coerce, dtype=np.float64)
        c1, c0 = ct.cat
        c1_name = c1
        c0_name = c0
        x_name = ct.x.name
        match = ct.match
        y = ct.y
        y1 = ct.data[c1]
        y0 = ct.data[c0]
    return y, y1, y0, c1, c0, match, x_name, c1_name, c0_name


def _related_measures_args(y, x, c1, c0, match, ds, sub, nd_data=False):
    "Interpret parameters for related measures tests (2 different argspecs)"
    if isinstance(x, str):
        if ds is None:
            raise TypeError(f"x={x!r} specified as str without specifying ds")
        x = ds.eval(x)

    if nd_data:
        two_y = isinstance(x, NDVar)
        coerce = asndvar
    else:
        two_y = isinstance(x, Var) and match is None
        coerce = asvar

    if two_y:
        assert match is None
        y1 = coerce(y, sub, ds)
        n = len(y1)
        y0 = coerce(x, sub, ds, n)
        c1_name = y1.name if c1 is None else c1
        c0_name = y0.name if c0 is None else c0
        x_name = y0.name
    elif match is None:
        raise TypeError("The `match` argument needs to be specified for related measures tests")
    else:
        ct = Celltable(y, x, match, sub, cat=(c1, c0), ds=ds, coercion=coerce, dtype=np.float64)
        c1, c0 = ct.cat
        c1_name = c1
        c0_name = c0
        if not ct.all_within:
            raise ValueError(f"conditions {c1!r} and {c0!r} do not have the same values on {dataobj_repr(ct.match)}")
        n = len(ct.y) // 2
        y1 = ct.y[:n]
        y0 = ct.y[n:]
        x_name = ct.x.name
        match = ct.match
    return y1, y0, c1, c0, match, n, x_name, c1_name, c0_name


def ttest(y, x=None, against=0, match=None, sub=None, corr='Hochberg',
          title='{desc}', ds=None):
    """T-tests for one or more samples

    parameters
    ----------
    y : Var
        Dependent variable
    x : None | categorial
        Perform tests separately for all categories in x.
    against : scalar | str | tuple
        Baseline against which to test (scalar or category in x).
    match : None | Factor
        Repeated measures factor.
    sub : index
        Only use part of the data.
    corr : None | 'hochberg' | 'bonferroni' | 'holm'
        Method for multiple comparison correction (default 'hochberg').
    title : str
        Title for the table.
    ds : Dataset
        If a Dataset is given, all data-objects can be specified as names of
        Dataset variables

    Returns
    -------
    table : FMText Table
        Table with results.
    """
    ct = Celltable(y, x, match, sub, ds=ds, coercion=asvar)

    par = True
    if par:
        infl = '' if x is None else 's'
        if ct.y.name is None:
            title_desc = "T-test%s against %s" % (infl, cellname(against))
        else:
            title_desc = "T-test%s of %s against %s" % (infl, ct.y.name, cellname(against))
        statistic_name = 't'
    else:
        raise NotImplementedError

    names = []
    diffs = []
    ts = []
    dfs = []
    ps = []

    if isinstance(against, (str, tuple)):
        if against not in ct.cells:
            x_repr = 'x' if ct.x.name is None else repr(ct.x.name)
            raise ValueError("agains=%r: %r is not a cell in %s"
                             % (against, against, x_repr))
        k = len(ct.cells) - 1
        baseline = ct.data[against]

        for cell in ct.cells:
            if cell == against:
                continue
            names.append(cell)
            if match is not None and ct.within[cell, against]:
                diffs.append(ct.data[cell].mean() - baseline.mean())
                t, p = scipy.stats.ttest_rel(ct.data[cell], baseline)
                df = len(baseline) - 1
            else:
                data = ct.data[cell]
                diffs.append(data.mean() - baseline.mean())
                t, p = scipy.stats.ttest_ind(data, baseline)
                df = len(baseline) + len(data) - 2
            ts.append(t)
            dfs.append(df)
            ps.append(p)

    elif np.isscalar(against):
        k = len(ct.cells)

        for cell in ct.cells:
            label = cellname(cell)
            data = ct.data[cell].x
            t, p = scipy.stats.ttest_1samp(data, against)
            df = len(data) - 1
            names.append(label)
            diffs.append(data.mean() - against)
            ts.append(t)
            dfs.append(df)
            ps.append(p)
    else:
        raise TypeError("against=%s" % repr(against))

    if k <= 1:
        corr = None

    if corr:
        ps_adjusted = mcp_adjust(ps, corr)
    else:
        ps_adjusted = ps
    stars = star(ps_adjusted, out=str)
    if len(set(dfs)) == 1:
        df_in_header = True
    else:
        df_in_header = False

    table = fmtxt.Table('l' + 'r' * (4 - df_in_header + bool(corr)))
    table.title(title.format(desc=title_desc))
    if corr:
        table.caption(_get_correction_caption(corr, k))

    # header
    table.cell("Effect")
    table.cell("Difference")
    if df_in_header:
        table.cell(fmtxt.symbol(statistic_name, dfs[0]))
    else:
        table.cell(statistic_name, 'math')
        table.cell('df', 'math')
    table.cell('p', 'math')
    if corr:
        table.cell(fmtxt.symbol('p', corr))
    table.midrule()

    # body
    for name, diff, t, mark, df, p, p_adj in zip(names, diffs, ts, stars, dfs, ps, ps_adjusted):
        table.cell(name)
        table.cell(diff)
        table.cell(fmtxt.stat(t, stars=mark, of=3))
        if not df_in_header:
            table.cell(df)

        table.cell(fmtxt.p(p))
        if corr:
            table.cell(fmtxt.p(p_adj))
    return table


class TTest:

    def __init__(self, difference, t, df, tail):
        self._difference = difference
        self.t = t
        self.df = df
        self.p = stats.ttest_p(self.t, self.df, tail)
        self.tail = tail

    def _asfmtext(
            self,
            rasterize: bool = None,
            difference: bool = False,
            **_,
    ):
        out = [fmtxt.eq('t', self.t, self.df), ', ', fmtxt.peq(self.p)]
        if difference:
            out = [fmtxt.eq('d', self._difference), ', '] + out
        return fmtxt.FMText(out)


class TTestOneSample(TTest):
    """One-sample t-test

    Parameters
    ----------
    y : Var
        Dependent variable.
    match : categorial
        Units within which measurements are related (e.g. 'subject' in a
        within-subject comparison).
    sub : index-array
        Perform the test with a subset of the data.
    ds : Dataset
        If a Dataset is specified, all data-objects can be specified as
        names of Dataset variables.
    popmean : float
        Population mean to test against (default 0).
    tail : 0 | 1 | -1
        Which tail of the t-distribution to consider:
        0: both (two-tailed, default);
        1: upper tail (one-tailed);
        -1: lower tail (one-tailed).

    Attributes
    ----------
    mean : float
        Mean of ``y``.
    t : float
        T-value.
    p : float
        P-value.
    tail : 0 | 1 | -1
        Tailedness of the p value.
    df : int
        Degrees of freedom.
    """
    def __init__(
            self,
            y: VarArg,
            match: CategorialArg = None,
            sub: IndexArg = None,
            ds: Dataset = None,
            popmean: float = 0,
            tail: int = 0,
    ):
        ct = Celltable(y, None, match, sub, ds=ds, coercion=asvar)
        n = len(ct.y)
        if n <= 2:
            raise ValueError("Not enough observations for t-test (n=%i)" % n)

        self.mean = ct.y.mean()
        self.popmean = popmean
        self._y = dataobj_repr(ct.y)
        v = ct.y.x[:, None]
        if popmean:
            v = v - popmean
        t = stats.t_1samp(v)[0]
        TTest.__init__(self, v.mean(), t, n - 1, tail)

    def __repr__(self):
        cmp = '=><'[self.tail]
        return f"<{self.__class__.__name__}: {self._y} {cmp} {self.popmean}; {self._asfmtext(difference=True)}>"


class TTestIndependent(TTest):
    """Independent measures t-test

    The test data can be specified in two forms:

     - In long form, with ``y`` supplying the data, ``x`` specifying condition
       for each case.
     - With ``y`` and ``x`` supplying data for the two conditions.

    Parameters
    ----------
    y : Var
        Dependent variable.
    x : categorial
        Model containing the cells which should be compared.
    c1 : str | tuple | None
        Test condition (cell of ``x``). ``c1`` and ``c0`` can be omitted if
        ``x`` only contains two cells, in which case cells will be used in
        alphabetical order.
    c0 : str | tuple | None
        Control condition (cell of ``x``).
    match : categorial
        Units within which measurements are related and should be averaged over
        (e.g. 'subject' in a between-group comparison).
    sub : index-array
        Perform the test with a subset of the data.
    ds : Dataset
        If a Dataset is specified, all data-objects can be specified as
        names of Dataset variables.
    tail : 0 | 1 | -1
        Which tail of the t-distribution to consider:
        0: both (two-tailed, default);
        1: upper tail (one-tailed);
        -1: lower tail (one-tailed).

    Attributes
    ----------
    t : float
        T-value.
    p : float
        P-value.
    tail : 0 | 1 | -1
        Tailedness of the p value.
    df : int
        Degrees of freedom.
    """
    def __init__(
            self,
            y: VarArg,
            x: CategorialArg,
            c1: CellArg = None,
            c0: CellArg = None,
            match: CategorialArg = None,
            sub: IndexArg = None,
            ds: Dataset = None,
            tail: int = 0,
    ):
        y, y1, y0, c1, c0, match, x_name, c1_name, c0_name = _independent_measures_args(y, x, c1, c0, match, ds, sub)

        n1 = len(y1)
        n = len(y)
        df = n - 2
        groups = np.arange(n) < n1
        d = y[groups].mean() - y[groups == False].mean()
        groups.dtype = np.int8
        t = stats.t_ind(y.x[:, None], groups)[0]

        self._y = dataobj_repr(y)
        self._x = x_name
        TTest.__init__(self, d, t, df, tail)
        self._c1 = c1_name
        self._c0 = c0_name
        self._two_y = c1 is None

    def __repr__(self):
        cmp = '=><'[self.tail]
        if self._two_y:
            desc = f"{self._c1} {cmp} {self._c0}"
        else:
            desc = f"{self._y} ~ {self._x}, {self._c1} {cmp} {self._c0}"
        return f"<{self.__class__.__name__}: {desc}; {self._asfmtext(difference=True)}>"


class MannWhitneyU:
    """Mann-Whitney U-test (non-parametric independent measures test)

    The test data can be specified in two forms:

     - In long form, with ``y`` supplying the data, ``x`` specifying condition
       for each case.
     - With ``y`` and ``x`` supplying data for the two conditions.

    Parameters
    ----------
    y : Var
        Dependent variable. Alternatively, the first of two variables that are
        compared.
    x : categorial
        Model containing the cells which should be compared. Alternatively, the
        second of two varaibles that are compared.
    c1 : str | tuple | None
        Test condition (cell of ``x``). ``c1`` and ``c0`` can be omitted if
        ``x`` only contains two cells, in which case cells will be used in
        alphabetical order.
    c0 : str | tuple | None
        Control condition (cell of ``x``).
    match : categorial
        Units within which measurements are related (e.g. 'subject' in a
        within-subject comparison). If match is unspecified, it is assumed that
        ``y`` and ``x`` are two measurements with matched cases.
    sub : index-array
        Perform the test with a subset of the data.
    ds : Dataset
        If a Dataset is specified, all data-objects can be specified as
        names of Dataset variables.
    tail : 0 | 1 | -1
        Which tail of the t-distribution to consider:
        0: both (two-tailed, default);
        1: upper tail (one-tailed);
        -1: lower tail (one-tailed).
    continuity : bool
        Continuity correction (default ``True``).

    Attributes
    ----------
    u : float
        Mann-Whitney U statistic.
    p : float
        P-value.
    tail : 0 | 1 | -1
        Tailedness of the p value.

    See Also
    --------
    TTestRelated : parametric alternative

    Notes
    -----
    Based on :func:`scipy.stats.mannwhitneyu`.
    """
    def __init__(
            self,
            y: VarArg,
            x: Union[CategorialArg, VarArg],
            c1: CellArg = None,
            c0: CellArg = None,
            match: CategorialArg = None,
            sub: IndexArg = None,
            ds: Dataset = None,
            tail: int = 0,
            continuity: bool = True,
    ):
        y, y1, y0, c1, c0, match, x_name, c1_name, c0_name = _independent_measures_args(y, x, c1, c0, match, ds, sub)
        if tail == 0:
            alternative = 'two-sided'
        elif tail == 1:
            alternative = 'greater'
        elif tail == -1:
            alternative = 'less'
        else:
            raise ValueError(f"tail={tail!r}")
        self.u, self.p = scipy.stats.mannwhitneyu(y1.x, y0.x, continuity, alternative)
        self._y = dataobj_repr(y1)
        self._x = x_name
        self._c1 = c1
        self._c0 = c0
        self.tail = tail
        self.continuity = continuity
        self._two_y = c1 is None

    def __repr__(self):
        cmp = '=><'[self.tail]
        if self._two_y:
            desc = f"{self._c1} {cmp} {self._c0}"
        else:
            desc = f"{self._y} ~ {self._x}, {self._c1} {cmp} {self._c0}"
        return f"<MannWhitneyU: {desc}; {self._asfmtext()}>"

    def _asfmtext(self, **_):
        return fmtxt.FMText([fmtxt.eq('U', self.u), ', ', fmtxt.peq(self.p)])


class TTestRelated(TTest):
    """Related-measures t-test

    The test data can be specified in two forms:

     - In long form, with ``y`` supplying the data, ``x`` specifying condition
       for each case and ``match`` determining which cases are related.
     - In wide/repeated measures form, with ``y`` and ``x`` both supplying data
       with matching case order.

    Parameters
    ----------
    y : Var
        Dependent variable. Alternatively, the first of two variables that are
        compared.
    x : categorial
        Model containing the cells which should be compared. Alternatively, the
        second of two varaibles that are compared.
    c1 : str | tuple | None
        Test condition (cell of ``x``). ``c1`` and ``c0`` can be omitted if
        ``x`` only contains two cells, in which case cells will be used in
        alphabetical order.
    c0 : str | tuple | None
        Control condition (cell of ``x``).
    match : categorial
        Units within which measurements are related (e.g. 'subject' in a
        within-subject comparison). If match is unspecified, it is assumed that
        ``y`` and ``x`` are two measurements with matched cases.
    sub : index-array
        Perform the test with a subset of the data.
    ds : Dataset
        If a Dataset is specified, all data-objects can be specified as
        names of Dataset variables.
    tail : 0 | 1 | -1
        Which tail of the t-distribution to consider:
        0: both (two-tailed, default);
        1: upper tail (one-tailed);
        -1: lower tail (one-tailed).

    Attributes
    ----------
    t : float
        T-value.
    p : float
        P-value.
    tail : 0 | 1 | -1
        Tailedness of the p value.
    difference : Var
        Difference values.
    df : int
        Degrees of freedom.
    c1_mean : float
        Mean of condition ``c1``.
    c0_mean : float
        Mean of condition ``c0``.

    See Also
    --------
    WilcoxonSignedRank : non-parametric alternative
    """
    def __init__(
            self,
            y: VarArg,
            x: Union[CategorialArg, VarArg],
            c1: CellArg = None,
            c0: CellArg = None,
            match: CategorialArg = None,
            sub: IndexArg = None,
            ds: Dataset = None,
            tail: int = 0,
    ):
        y1, y0, c1, c0, match, n, x_name, c1_name, c0_name = _related_measures_args(y, x, c1, c0, match, ds, sub)
        if n <= 2:
            raise ValueError("Not enough observations for t-test (n=%i)" % n)
        self._y = dataobj_repr(y1)
        self._x = x_name
        self._c1 = c1
        self._c0 = c0
        self.c1_mean = y1.mean()
        self.c0_mean = y0.mean()
        self.difference = y1 - y0
        t = stats.t_1samp(self.difference.x[:, None])[0]
        TTest.__init__(self, self.difference.x.mean(), t, n - 1, tail)
        self._match = dataobj_repr(match, True)

    def __repr__(self):
        cmp = '=><'[self.tail]
        if self._match is None:
            desc = f"{self._c1} {cmp} {self._c0}"
        else:
            desc = f"{self._y} ~ {self._x}, {self._c1} {cmp} {self._c0}"
        return f"<{self.__class__.__name__}: {desc}; {self._asfmtext(difference=True)}>"


class WilcoxonSignedRank:
    """Wilcoxon signed-rank test (non-parametric related measures test)

    The test data can be specified in two forms:

     - In long form, with ``y`` supplying the data, ``x`` specifying condition
       for each case and ``match`` determining which cases are related.
     - In wide/repeated measures form, with ``y`` and ``x`` both supplying data
       with matching case order.

    Parameters
    ----------
    y : Var
        Dependent variable. Alternatively, the first of two variables that are
        compared.
    x : categorial
        Model containing the cells which should be compared. Alternatively, the
        second of two varaibles that are compared.
    c1 : str | tuple | None
        Test condition (cell of ``x``). ``c1`` and ``c0`` can be omitted if
        ``x`` only contains two cells, in which case cells will be used in
        alphabetical order.
    c0 : str | tuple | None
        Control condition (cell of ``x``).
    match : categorial
        Units within which measurements are related (e.g. 'subject' in a
        within-subject comparison). If match is unspecified, it is assumed that
        ``y`` and ``x`` are two measurements with matched cases.
    sub : index-array
        Perform the test with a subset of the data.
    ds : Dataset
        If a Dataset is specified, all data-objects can be specified as
        names of Dataset variables.
    tail : 0 | 1 | -1
        Which tail of the t-distribution to consider:
        0: both (two-tailed, default);
        1: upper tail (one-tailed);
        -1: lower tail (one-tailed).
    zero_method : str
        How to handle zero differences (see :func:`scipy.stats.wilcoxon`).
    correction : bool
        Continuity correction (default ``False``).

    Attributes
    ----------
    w : float
        Rank sum statistic.
    p : float
        P-value.
    tail : 0 | 1 | -1
        Tailedness of the p value.
    difference : Var
        Difference values.
    c1_mean : float
        Mean of condition ``c1``.
    c0_mean : float
        Mean of condition ``c0``.

    See Also
    --------
    TTestRelated : parametric alternative

    Notes
    -----
    Based on :func:`scipy.stats.wilcoxon`.
    """
    def __init__(
            self,
            y: VarArg,
            x: Union[CategorialArg, VarArg],
            c1: CellArg = None,
            c0: CellArg = None,
            match: CategorialArg = None,
            sub: IndexArg = None,
            ds: Dataset = None,
            tail: int = 0,
            zero_method: str = 'wilcox',
            correction: bool = False,
    ):
        y1, y0, c1, c0, match, n, x_name, c1_name, c0_name = _related_measures_args(y, x, c1, c0, match, ds, sub)
        if tail == 0:
            alternative = 'two-sided'
        elif tail == 1:
            alternative = 'greater'
        elif tail == -1:
            alternative = 'less'
        else:
            raise ValueError(f"tail={tail!r}")
        self.w, self.p = scipy.stats.wilcoxon(y1.x, y0.x, zero_method, correction, alternative)
        self._y = dataobj_repr(y1)
        self._x = x_name
        self._c1 = c1
        self._c0 = c0
        self.c1_mean = y1.mean()
        self.c0_mean = y0.mean()
        self.difference = y1 - y0
        self._match = dataobj_repr(match, True)
        self.tail = tail
        self.zero_method = zero_method
        self.correction = correction

    def __repr__(self):
        cmp = '=><'[self.tail]
        if self._match is None:
            desc = f"{self._c1} {cmp} {self._c0}"
        else:
            desc = f"{self._y} ~ {self._x}, {self._c1} {cmp} {self._c0}"
        return f"<{self.__class__.__name__}: {desc}; {self._asfmtext()}>"

    def _asfmtext(self, **_):
        return fmtxt.FMText([fmtxt.eq('W', self.w), ', ', fmtxt.peq(self.p)])


def pairwise(
        y: VarArg,
        x: CategorialArg,
        match: CategorialArg = None,
        sub: IndexArg = None,
        ds: Dataset = None,
        par: bool = True,
        corr: Union[None, str] = 'Hochberg',
        trend: Union[bool, str] = False,
        title: str = '{desc}',
        mirror: bool = False,
):
    """Pairwise comparison table

    Parameters
    ----------
    y : Var
        Dependent measure.
    x : categorial
        Categories to compare.
    match : None | Factor
        Repeated measures factor.
    sub : index-array
        Perform tests with a subset of the data.
    ds : Dataset
        If a Dataset is given, all data-objects can be specified as names of
        Dataset variables.
    par : bool
        Use parametric test for pairwise comparisons (use non-parametric
        tests if False).
    corr : None | 'hochberg' | 'bonferroni' | 'holm'
        Method for multiple comparison correction.
    trend
        Marker for a trend in pairwise comparisons.
    title
        Title for the table.
    mirror
        Redundant table including all row/column combinations.

    Returns
    -------
    table : FMText Table
        Table with results.
    """
    ct = Celltable(y, x, match=match, sub=sub, ds=ds, coercion=asvar)
    test = _pairwise(ct.get_data(), ct.all_within, par, corr, trend)

    # extract test results
    k = len(ct)
    indexes = test['pw_indexes']
    statistic = test['statistic']
    _K = test[statistic]
    _P = test['p']
    if corr:
        _Pc = mcp_adjust(_P, corr)
    _df = test['df']
    symbols = test['symbols']

    # create TABLE
    table = fmtxt.Table('l' + 'l' * (k - 1 + mirror))
    title_desc = "Pairwise {0}".format(test['test'])
    table.title(title.format(desc=title_desc))
    table.caption(test['caption'])

    # headings
    table.cell()
    cellnames = ct.cellnames()
    for name in cellnames[1 - mirror:]:
        table.cell(name)
    table.midrule()

    # tex_df = fmtxt.Element(df, "_", digits=0)
    if corr and not mirror:
        subrows = 3
    else:
        subrows = 2

    n_stars = 3 + bool(trend)
    for row in range(0, k - 1 + mirror):
        for subrow in range(subrows):  # contains t/p
            # names column
            if subrow == 0:
                table.cell(cellnames[row])
            else:
                table.cell()
            # rows
            for col in range(1 - mirror, k):
                if row == col:
                    table.cell()
                elif col > row:
                    index = indexes[(row, col)]
                    if subrow == 0:
                        table.cell(fmtxt.eq(statistic, _K[index], _df[index], stars=symbols[index], of=n_stars))
                    elif subrow == 1:
                        table.cell(fmtxt.peq(_P[index]))
                    elif subrow == 2:
                        table.cell(fmtxt.peq(_Pc[index], 'c'))
                elif mirror and corr and subrow == 0:
                    index = indexes[(col, row)]
                    table.cell(fmtxt.P(_Pc[index]))
                else:
                    table.cell()
    return table


def _pairwise(
        data,
        within,
        parametric,
        corr,
        trend,
        levels=True,
):
    """Pairwise tests

    Parameters
    ----------
    data
        list of groups/treatments
    corr : 'Hochberg' | 'Holm' | 'Bonferroni'
        MCP.

    Returns
    -------
    results : dict
        dictionary with results:
        'test': test name
        'caption': information about correction
        'statistic': abbreviation used for the staistic (e.g. 'Q')
        statistic: list of values
        'df': df
        'p': list of corresponding pa values
        'stars': list of n stars (ints)
        'pw_indexes': dict linking table index (i,j) to the list index for p etc.
    """
    # find test
    k = len(data)
    if k < 3:  # need no correction for single test
        corr = None
    if parametric:
        if within:
            test_func = scipy.stats.ttest_rel
            test_name = "T-Tests (paired samples)"
        else:
            test_func = scipy.stats.ttest_ind
            test_name = "T-Tests (independent samples)"
        statistic = "t"
    elif within:
        test_func = partial(scipy.stats.wilcoxon, alternative='two-sided')
        test_name = "Wilcoxon Signed-Rank Test"
        statistic = "z"
    else:
        test_func = partial(scipy.stats.mannwhitneyu, alternative='two-sided')
        test_name = "Mann-Whitney U Test"
        statistic = "u"

    # perform test
    _K = []  # kennwerte
    _P = []
    _df = []
    i = 0
    indexes = {}
    for x in range(k):
        for y in range(x + 1, k):
            Y1, Y2 = data[x], data[y]
            t, p = test_func(Y1, Y2)
            _K.append(t)
            if within:
                _df.append(len(Y1) - 1)
            else:
                _df.append(len(Y1) + len(Y2) - 2)

            _P.append(p)
            indexes[(x, y)] = indexes[(y, x)] = i
            i += 1
    # add stars
    if corr:
        p_adjusted = mcp_adjust(_P, corr)
    else:
        p_adjusted = _P
    # prepare output
    out = {'test': test_name,
           'caption': _get_correction_caption(corr, len(_P)),
           'statistic': statistic,
           statistic: _K,
           'df': _df,
           'p': _P,
           'stars': star(p_adjusted, int, levels, trend),
           'symbols': star(p_adjusted, str, levels, trend),
           'pw_indexes': indexes}
    return out


def pairwise_correlations(xs, sub=None, ds=None, labels={}):
    """Pairwise correlation table

    Parameters
    ----------
    xs : sequence of Var | NDVar
        Variables to correlate.
    sub : index
        Use only a subset of the data
    ds : Dataset
        If a Dataset is given, all data-objects can be specified as names of
        Dataset variables.
    labels : {str: str} dict
        Labels for ``xs`` in the table (mapping ``x.name`` to string labels).

    Returns
    -------
    pairwise_table : fmtxt.Table
        Table with pairwise correlations.
    """
    sub = assub(sub, ds)
    x_rows = [asnumeric(x, sub, ds) for x in xs]
    n_vars = len(x_rows)

    table = fmtxt.Table('l' + 'c' * n_vars)
    # header
    table.cell()
    for i in range(1, n_vars + 1):
        table.cell(i)
    table.midrule()
    # body
    for i_row, x_row in enumerate(x_rows):
        label = nice_label(x_row, labels)
        table.cell("%i  %s" % (i_row + 1, label))
        for x_col in x_rows:
            if x_col is x_row:
                table.cell()
            else:
                corr = Correlation(x_row, x_col)
                table.cell(fmtxt.stat(corr.r, drop0=True))
        table.endline()
    return table


def correlations(y, x, cat=None, sub=None, ds=None, asds=False):
    """Correlation with one or more predictors

    Parameters
    ----------
    y : Var
        First variable
    x : Var | list of Var
        second variable (or list of variables).
    cat : categorial
        Show correlations separately for different groups in the data.
    sub : index
        Use only a subset of the data
    ds : Dataset
        If a Dataset is given, all data-objects can be specified as names of
        Dataset variables.
    asds : bool
        Return correlations in Dataset instead of Table.

    Returns
    -------
    correlations : Table | Dataset
        Table or Dataset (if ``asds=True``) with correlations.
    """
    sub = assub(sub, ds)
    y = asvar(y, sub, ds)
    if isinstance(x, (Var, str)):
        x = (x,)
        print_x_name = False
    else:
        print_x_name = True
    x = [asvar(x_, sub, ds) for x_ in x]
    if cat is None:
        cat_cells = [None]
        n_cat = 1
    else:
        cat = ascategorial(cat, sub, ds)
        cat_cells = cat.cells
        n_cat = len(cat_cells)

    # correlation Dataset, nested:
    # x -> cat
    ds = Dataset()
    if print_x_name:
        ds['x'] = Factor([dataobj_repr(x_) for x_ in x], repeat=n_cat)

    if n_cat > 1:
        if isinstance(cat, Interaction):
            cat_names = [dataobj_repr(c) for c in cat.base]
            for i, name in enumerate(cat_names):
                ds[name] = Factor([cell[i] for cell in cat.cells], tile=len(x))
        elif isinstance(cat, Factor):
            cat_names = (dataobj_repr(cat),)
            ds[dataobj_repr(cat)] = Factor(cat.cells, tile=len(x))
        else:
            raise TypeError(repr(cat))
    else:
        cat_names = ()

    rs = []
    dfs = []
    ps = []
    for x_ in x:
        for cell in cat_cells:
            if cell is None:
                r, p, df = _corr(y.x, x_.x)
            else:
                sub = cat == cell
                r, p, df = _corr(y[sub].x, x_[sub].x)
            rs.append(r)
            dfs.append(df)
            ps.append(p)
    ds['r'] = Var(rs)
    ds['df'] = Var(dfs)
    p = Var(ps)
    ds['sig'] = star_factor(p)
    ds['p'] = p
    if asds:
        return ds

    table = fmtxt.Table('l' * (4 + print_x_name + len(cat_names)),
                        title="Correlations with %s" % dataobj_repr(y))
    if print_x_name:
        table.cell('x')
    table.cells(*cat_names)
    table.cells('r', 'df', '*' 'p')
    table.midrule()
    last_x = None
    for case in ds.itercases():
        if print_x_name:
            if case['x'] == last_x:
                table.cell('')
            else:
                table.cell(case['x'])
                last_x = case['x']
        for name in cat_names:
            table.cell(case[name])
        table.cell(fmtxt.stat(case['r'], '%.3f', drop0=True))
        table.cell(case['df'])
        table.cell(case['sig'])
        table.cell(fmtxt.p(case['p']))
    return table


def _corr(y, x):
    n = len(y)
    assert len(x) == n
    df = n - 2
    r = np.corrcoef(y, x)[0, 1]
    if r == 1:
        return r, 0., df
    t = r / np.sqrt((1 - r ** 2) / df)
    p = scipy.stats.t.sf(np.abs(t), df) * 2
    return r, p, df


class bootstrap_pairwise:
    def __init__(self, y, x, match=None, sub=None,
                 samples=1000, replacement=True,
                 title="Bootstrapped Pairwise Tests", ds=None):
        sub = assub(sub, ds)
        y = asvar(y, sub, ds)
        x = asfactor(x, sub, ds)
        assert len(y) == len(x), "data length mismatch"
        if match is not None:
            match = ascategorial(match, sub, ds)
            assert len(match) == len(y), "data length mismatch"

        # prepare data container
        resampled = np.empty((samples + 1, len(y)))  # sample x subject within category
        resampled[0] = y.x
        # fill resampled
        for i, y_i in enumerate(resample(y, samples, replacement, match), 1):
            resampled[i] = y_i.x
        self.resampled = resampled

        cells = x.cells
        n_groups = len(cells)

        if match is not None:
            # if there are several values per x%match cell, take the average
            # T: indexes to transform y.x to [x%match, value]-array
            match_cell_ids = match.cells
            group_size = len(match_cell_ids)
            T = None
            i = 0
            for x_cell in cells:
                for match_cell in match_cell_ids:
                    source_indexes = np.where((x == x_cell) * (match == match_cell))[0]
                    if T is None:
                        n_cells = n_groups * group_size
                        T = np.empty((n_cells, len(source_indexes)), dtype=int)
                    T[i, :] = source_indexes
                    i += 1

            if T.shape[1] == 1:
                T = T[:, 0]
                ordered = resampled[:, T]
            else:
                ordered = resampled[:, T].mean(axis=2)
            self.ordered = ordered

            # t-tests
            n_comparisons = sum(range(n_groups))
            t = np.empty((samples + 1, n_comparisons))
            comp_names = []
            one_group = np.arange(group_size)
            groups = [one_group + i * group_size for i in range(n_groups)]
            for i, (g1, g2) in enumerate(itertools.combinations(range(n_groups), 2)):
                group_1 = groups[g1]
                group_2 = groups[g2]
                diffs = ordered[:, group_1] - ordered[:, group_2]
                t[:, i] = (np.mean(diffs, axis=1) * np.sqrt(group_size) /
                           np.std(diffs, axis=1, ddof=1))
                comp_names.append(' - '.join((cells[g1], cells[g2])))

            self.diffs = diffs
            self.t_resampled = np.max(np.abs(t[1:]), axis=1)
            self.t = t = t[0]
        else:
            raise NotImplementedError

        self._Y = y
        self._X = x
        self._group_names = cells
        self._group_data = np.array([ordered[0, g] for g in groups])
        self._group_size = group_size
        self._df = group_size - 1
        self._match = match
        self._n_samples = samples
        self._replacement = replacement
        self._comp_names = comp_names
        self._p_parametric = self.test_param(t)
        self._p_boot = self.test_boot(t)
        self.title = title

    def __repr__(self):
        out = ['bootstrap_pairwise(', self._Y.name, self._X.name]
        if self._match:
            out.append('match=%s ' % self._match.name)
        out.append('saples=%i ' % self._n_samples)
        out.append('replacement=%s)' % self._replacement)
        return ''.join(out)

    def __str__(self):
        return str(self.table())

    def table(self):
        table = fmtxt.Table('lrrrr')
        table.title(self.title)
        table.caption("Results based on %i samples" % self._n_samples)
        table.cell('Comparison')
        table.cell(fmtxt.symbol('t', self._df))
        table.cell(fmtxt.symbol('p', 'param'))
        table.cell(fmtxt.symbol('p', 'corr'))
        table.cell(fmtxt.symbol('p', 'boot'))
        table.midrule()

        p_corr = mcp_adjust(self._p_parametric)
        stars_parametric = star(p_corr)
        stars_boot = star(self._p_boot)

        for name, t, p1, pc, s1, p2, s2 in zip(self._comp_names, self.t,
                                                self._p_parametric, p_corr,
                                                stars_parametric,
                                                self._p_boot, stars_boot):
            table.cell(name)
            table.cell(t, fmt='%.2f')
            table.cell(fmtxt.p(p1))
            table.cell(fmtxt.p(pc, stars=s1))
            table.cell(fmtxt.p(p2, stars=s2))
        return table

    def plot_t_dist(self):
        # http://stackoverflow.com/questions/4150171/how-to-create-a-density-plot-in-matplotlib
        from matplotlib import pyplot

        t = self.t_resampled
        density = scipy.stats.gaussian_kde(t)
#        density.covariance_factor = lambda : .25
#        density._compute_covariance()
        xs = np.linspace(0, max(t), 200)
        pyplot.plot(xs, density(xs))

    def plot_dv_dist(self):
        from matplotlib import pyplot

        xs = np.linspace(np.min(self._group_data), np.max(self._group_data), 200)
        for i, name in enumerate(self._group_names):
            density = scipy.stats.gaussian_kde(self._group_data[i])
            pyplot.plot(xs, density(xs), label=name)
        pyplot.legend()

    def test_param(self, t):
        return scipy.stats.t.sf(np.abs(t), self._group_size - 1) * 2

    def test_boot(self, t):
        "t: scalar or array; returns p for each t"
        test = self.t_resampled[:, None] > np.abs(t)
        return np.sum(test, axis=0) / self.t_resampled.shape[0]
