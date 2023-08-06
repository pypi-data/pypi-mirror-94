""" This module contains a class Quantiles that calculates quantiles
of measured heads for hydrological years.

Author: Thomas de Meij

"""

from datetime import datetime
import datetime as dt
import warnings
import numpy as np
from pandas import Series, DataFrame
import pandas as pd
import matplotlib.pyplot as plt

import acequia as aq


class Quantiles:
    """Calculate quantiles from series of measured heads

    Parameters
    ----------
    ts : pd.Series, aq.GwSeries
        timeseries with groundwater head measurments

    ref : str, ['datum','surface']
        reference level for measurements

    nclasses : int (default 10)
        number of quantile classes 

    days : bool, default True
        label xax with days or quantiles

    """

    n14 = 18

    def __init__(self, gw, srname=None, ref='surface', nclasses=10, days=True):
        """Return quantiles object"""

        if isinstance(gw,aq.GwSeries):
            ts = gw.heads(ref=ref)
            if srname is None:
                srname = gw.name()

        if isinstance(gw,pd.Series):
            ts = gw
            if srname is None: 
                srname = gw.name

        if srname is None: 
            srname = 'series'

        self.gw = gw
        self.ref = ref
        self.ts = ts
        self.srname = srname
        self.days = days

        if self.days:
            
            self.days = [x*30 for x in range(12)] + [365]
            self.qt = [x/365 for x in self.days]
            self.qtlabels = [str(x) for x in self.days]
            """
            self.days = [x*5 for x in range(74)] #+ [365]
            self.qt = [x/365 for x in self.days]
            self.qtlabels = [str(x) for x in self.days] # if (x/30).is_integer()]
            """

        else:
            self.qt = np.linspace(0,1,nclasses+1) # list of quantiles
            self.qtlabels = ['p'+str(int(x*100)) for x in self.qt]
            self.days = [int(x*365) for x in self.qt]

        self.tbl = self._quantiles()


    def _quantiles(self):
        """Return table with quantiles for each hydrological year"""

        # empty table with hydroyears and percentiles
        hydroyear = aq.hydroyear(self.ts)
        #allyears = np.arange(hydroyear.min(),hydroyear.max()+1)
        tbl = pd.DataFrame(index=set(hydroyear),columns=self.qtlabels)


        for i,(name,val) in enumerate(zip(self.qtlabels,self.qt)):
            grp = self.ts.groupby(hydroyear)
            tbl[name] = grp.quantile(val)

        return tbl


    def table(self):
        """Return table of quantiles for each hydrological year"""
        return self.tbl


    def plot(self,years=None,figpath=None,figtitle=None,ylim=None,
        ignore=None):
        """Plot quantiles

        Parameters
        ----------
        years : list of int
            years to plot in color
        figpath : str, optional
            figure output path
        figtitle : str, optional
            figure title
        ylim : list, optional
            ymin, ymax
        ignore : list, optional
            years to ignore in calculating reference
        """

        if years is None:
            years = []

        if not isinstance(years,list):
            msg = f'years of type {type(list)} changed to empty list'
            warnings.warn(msg)
            years = []

        if figtitle is None:
            figtitle = self.srname

        csurf = '#8ec7ff'
        clines = '#2f90f1' #'#c1e0ff'
        cyears = '#b21564'

        fig,ax = plt.subplots(1,1)
        fig.set_figwidth(13)
        fig.set_figheight(7)

        tbl = self.tbl
        x = self.qt

        reftbl = tbl.copy()
        if ignore:
            idx = [x for x in reftbl.index.values if x not in ignore]
            reftbl = reftbl.loc[idx,:]

        # reference based on quantiles
        upper = reftbl.quantile(0.05)*100
        lower = reftbl.quantile(0.95)*100

        # alternative reference
        #mean = reftbl.median(axis=0,skipna=True)
        #std = reftbl.std(axis=0,skipna=True)
        #upper = (mean+std)*100
        #lower = (mean-std)*100

        # alternative reference 2
        # leave out lowest line
        #upper = [reftbl[col].sort_values()[:-1].quantile(0.05)*100 for col in reftbl.columns]
        #lower = [reftbl[col].sort_values()[:-1].quantile(0.95)*100 for col in reftbl.columns]

        ax.fill_between(x, upper, lower, color=csurf) 

        for year in self.tbl.index:

            yvals = self.tbl.loc[year,:].values * 100
            xvals = self.qt

            #if year in years:
            #    ax.plot(xvals,yvals,color=cyears)
            #else:
            ax.plot(xvals,yvals,color=clines)


        for year in self.tbl.index:
            if year in years:
                yvals = self.tbl.loc[year,:].values * 100
                xvals = self.qt
                ax.plot(xvals,yvals,color=cyears)

        ax.set_xticks(self.qt)
        ax.set_xticklabels(self.qtlabels)
        if self.days:
            ##ax.set_xticklabels(self.days)
            ax.set_xlabel('dagen/jaar', fontsize=15)
        else:
            ax.set_xlabel('percentiel', fontsize=15)

        ax.set_xlim(1,0)
        if ylim:
            ax.set_ylim(ylim[0],ylim[1])

        ax.invert_xaxis()
        if self.ref=='surface':
            ax.invert_yaxis()

        ax.set_ylabel('grondwaterstand (cm -mv)', fontsize=15)


        ax.text(0.99, 0.97, figtitle, horizontalalignment='right',
                verticalalignment='top', transform=ax.transAxes,
                fontsize = 16)

        if figpath is not None:
            plt.savefig(figpath,bbox_inches='tight')

        plt.show()
        return ax
