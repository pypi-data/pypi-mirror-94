#!/usr/bin/env python
u"""
iers_mean_pole.py
Written by Tyler Sutterley (07/2020)
Provides the angular coordinates of the IERS Conventional Mean Pole (CMP)
Coordinates are based on the table of values from
    ftp://hpiers.obspm.fr/iers/eop/eopc01/mean-pole.tab
Based on IERS_CMP_YYYY.f located at ftp://tai.bipm.org/iers/convupdt/chapter7/
    http://iers-conventions.obspm.fr/

INPUTS:
    input_file: full path to mean-pole.tab file provided by IERS
    input_epoch: dates for which the angular coordinates of the Conventional
        Mean Pole are desired in decimal years
    version: Year of the conventional model.
        Limited to values of '2003', '2010', '2015'

OUTPUTS:
    x: Angular coordinate x of conventional mean pole [arcsec]
    y: Angular coordinate y of conventional mean pole [arcsec]
    flag: epoch is valid for version and version number is valid
        data will be set to FILL_VALUE if flag == False

OPTIONS:
    FILL_VALUE: value for invalid flags

PYTHON DEPENDENCIES:
    numpy: Scientific Computing Tools For Python
        https://numpy.org
        https://numpy.org/doc/stable/user/numpy-for-matlab-users.html

REFERENCE:
    Petit, G. and Luzum, B. (eds.), IERS Conventions (2010),
        IERS Technical Note No. 36, BKG (2010)

UPDATE HISTORY:
    Updated 07/2020: added function docstrings
    Updated 12/2018: using future division for python3 compatibility
    Written 09/2017
"""
from __future__ import division
import numpy as np

#-- read table of mean pole values, calculate angular coordinates at epoch
def iers_mean_pole(input_file,input_epoch,version,FILL_VALUE=np.nan):
    """
    Calculates the angular coordinates of the IERS Conventional Mean Pole (CMP)

    Arguments
    ---------
    input_file: full path to mean-pole.tab file provided by IERS
    input_epoch: dates for the angular coordinates of the Conventional Mean Pole
    version: Year of the conventional model.

    Keyword arguments
    -----------------
    FILL_VALUE: value for invalid flags

    Returns
    -------
    x: Angular coordinate x of conventional mean pole
    y: Angular coordinate y of conventional mean pole
    flag: epoch is valid for version and version number is valid
    """
    #-- verify IERS model version
    assert version in ('2003','2010','2015'), "Incorrect IERS model version"
    #-- read mean pole file
    table = np.loadtxt(input_file)
    #-- reduce to 1971 to end date
    ii, = np.nonzero(table[:,0] >= 1971)
    table = np.copy(table[ii,:])
    #-- reduce to yearly values
    jj, = np.nonzero((table[:,0] % 1) == 0.0)
    table = np.copy(table[jj,:])
    end_time = table[-1,0] + 0.2
    #-- final shape of the table
    nrows,ncols = np.shape(table)
    #-- allocate for output arrays
    x = np.full_like(input_epoch,FILL_VALUE)
    y = np.full_like(input_epoch,FILL_VALUE)
    flag = np.zeros_like(input_epoch,dtype=np.bool)
    for t,epoch in enumerate(input_epoch):
        #-- Conventional mean pole model in IERS Conventions 2003
        if (version == '2003') and (epoch >= 1975) and (epoch < 2004):
            x[t] = 0.054 + 0.00083*(epoch-2000.0)
            y[t] = 0.357 + 0.00395*(epoch-2000.0)
            flag[t] = True
        #-- Conventional mean pole model in IERS Conventions 2010
        elif (version == '2010') and (epoch >= 1975) and (epoch < 2011):
            dx = epoch-2000.0
            if (dx < 10.0):
                x[t] = 0.055974 + 1.8243e-3*dx + 1.8413e-4*dx**2 + 7.024e-6*dx**3
                y[t] = 0.346346 + 1.7896e-3*dx + 1.0729e-4*dx**2 + 0.908e-6*dx**3
            else:
                x[t] = 0.023513 + 0.0076141*dx
                y[t] = 0.358891 - 0.0006287*dx
            flag[t] = True
        #-- Conventional mean pole model in IERS Conventions 2015
        #-- must be below maximum valid date within file (e.g. 2015.2 for 2015)
        elif (version == '2015') and (epoch >= 1975) and (epoch < end_time):
            #-- find epoch within mean pole table
            i = 1
            j = nrows+1
            while (j > (i+1)):
                k = (i+j)//2
                if (epoch < table[k,0]):
                    j = k
                else:
                    i = k
            #-- calculate differential from point in table
            dx = epoch - table[i,0]
            if (i == (nrows-1)):
                x[t] = table[i,1] + dx*(table[nrows-1,1]-table[nrows-2,1])
                y[t] = table[i,2] + dx*(table[nrows-1,1]-table[nrows-2,2])
            else:
                x[t] = table[i,1] + dx*(table[i+1,1]-table[i,1])
                y[t] = table[i,2] + dx*(table[i+1,2]-table[i,2])
            flag[t] = True
    #-- return mean pole values
    return (x,y,flag)
