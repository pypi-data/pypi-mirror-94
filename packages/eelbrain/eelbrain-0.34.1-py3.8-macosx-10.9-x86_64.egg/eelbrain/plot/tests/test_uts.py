# Author: Christian Brodbeck <christianbrodbeck@nyu.edu>
from eelbrain import datasets, plot, testnd, Factor, concatenate, set_tmin
from eelbrain.testing import hide_plots


@hide_plots
def test_uts_stat():
    "test plot.UTSStat plotting function"
    ds = datasets.get_uts(utsnd=True)
    p = plot.UTSStat('uts', ds=ds)
    p.close()
    p = plot.UTSStat('uts', 'A%B', ds=ds)
    p.plot_legend('lower right')
    p.plot_legend(False)
    pl = p.plot_legend('fig')
    p.plot_legend('center')
    pl.close()
    p.close()
    p = plot.UTSStat('uts', 'A', xax='B', ds=ds)
    p.close()
    p = plot.UTSStat('uts', 'A', 'B', match='rm', ds=ds)
    assert [len(pl.stat_plots) for pl in p._plots] == [2, 2]
    p.close()
    p = plot.UTSStat('uts', 'A', 'B', match='rm', ds=ds, pool_error=False)
    assert [len(pl.stat_plots) for pl in p._plots] == [2, 2]
    p.close()

    # error
    p = plot.UTSStat('uts', 'A', match='rm', ds=ds, error='none')
    p.close()
    p = plot.UTSStat('uts', 'A', match='rm', ds=ds, error='all')
    p.close()

    # clusters
    sds = ds.sub("B == 'b0'")
    res = testnd.TTestRelated('uts', 'A', 'a1', 'a0', match='rm', ds=sds, samples=0, pmin=0.05, mintime=0.02)
    p = plot.UTSStat('uts', 'A', ds=ds)
    p.set_clusters(res.clusters)
    p.close()
    p = plot.UTSStat('uts', 'A', ds=ds, clusters=res.clusters)
    p.close()
    res = testnd.TTestRelated('uts', 'A', 'a1', 'a0', match='rm', ds=sds, samples=100, pmin=0.05, mintime=0.02)
    res_sub = testnd.TTestRelated('uts', 'A', 'a1', 'a0', match='rm', ds=sds, tstart=0.100, samples=100, pmin=0.05, mintime=0.02)
    p = plot.UTSStat('uts', 'A', ds=ds, clusters=res.clusters)
    p.close()
    p = plot.UTSStat('uts', 'A', 'B', ds=ds, clusters=res_sub.clusters)
    p.set_clusters(None)
    p.set_clusters(res.clusters, ax=0)
    p.close()
    p = plot.UTSStat('uts', 'A', 'B', ds=ds)
    p.set_clusters(res.clusters)
    p.set_clusters(None, ax=1)
    p.close()

    # mask
    p = plot.UTSStat('uts', 'A', ds=ds, mask=res.p > 0.05)
    p.close()
    p = plot.UTSStat('uts', 'A', ds=ds, mask=res_sub.p > 0.05)
    p.close()

    # x-axis other than time
    p = plot.UTSStat("utsnd.sub(time=0)", 'A', ds=ds)
    assert p.figure.axes[0].get_xlim() == (0, 4)
    p.close()


@hide_plots
def test_uts():
    "test plot.UTS plotting function"
    ds = datasets.get_uts()
    x_long = set_tmin(concatenate(ds[:10, 'uts']), -1)

    p = plot.UTS('uts', ds=ds)
    p.close()
    p = plot.UTS('uts', 'A%B', ds=ds)
    p.set_ylim(1)
    p.set_ylim(0, 1)
    assert p.get_ylim() == (0, 1)
    p.set_ylim(1, -1)
    assert p.get_ylim() == (1, -1)
    p.close()

    p = plot.UTS(x_long, h=2, w=5, xlim=2)
    assert p.get_xlim() == (-1, 1)
    p.set_xlim(2, 4)
    assert p.get_xlim() == (2, 4)
    p.close()

    # color dict
    colors = plot.colors_for_oneway(['a0', 'a1', 'a2'])
    a0, a1, a2 = ds[:3, 'uts']
    a0.name = 'a0'
    a1.name = 'a1'
    a2.name = 'a2'
    p = plot.UTS([[a0, a1, a2]], colors=colors)
    p.close()

    # multiple y with xax
    y1 = ds.eval("uts[(A == 'a1') & (B == 'b1')]")
    y1.name='y'
    y2 = ds.eval("uts[(A == 'a0') & (B == 'b1')]")
    y2.name='y2'
    rm = ds.eval("rm[(A == 'a0') & (B == 'b1')]")
    p = plot.UTS(y1, rm)
    p.close()
    p = plot.UTS([y1, y2], rm)
    p.close()

    # axtitle from Factor
    ds1 = ds[:3]
    p = plot.UTS('uts', xax='.case', axtitle=ds1['rm'], ds=ds1, ncol=1, w=2)
    p.close()


@hide_plots
def test_clusters():
    "test plot.uts cluster plotting functions"
    ds = datasets.get_uts()

    A = ds['A']
    B = ds['B']
    Y = ds['uts']

    # fixed effects model
    res = testnd.ANOVA(Y, A * B)
    p = plot.UTSClusters(res, title="Fixed Effects Model")
    p.close()

    # random effects model:
    subject = Factor(range(15), tile=4, random=True, name='subject')
    res = testnd.ANOVA(Y, A * B * subject, match=subject, samples=2)
    p = plot.UTSClusters(res, title="Random Effects Model")
    p.close()

    # plot UTSStat
    p = plot.UTSStat(Y, A % B, match=subject)
    p.set_clusters(res.clusters)
    p.close()
    p = plot.UTSStat(Y, A, xax=B, match=subject)
    p.close()
