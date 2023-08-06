#!/usr/bin/env python
u"""
compute_LPT_displacements.py
Written by Tyler Sutterley (12/2020)
Calculates radial pole load tide displacements for an input file
    following IERS Convention (2010) guidelines
    http://maia.usno.navy.mil/conventions/2010officialinfo.php
    http://maia.usno.navy.mil/conventions/chapter7.php

INPUTS:
    csv file with columns for spatial and temporal coordinates
    HDF5 file with variables for spatial and temporal coordinates
    netCDF4 file with variables for spatial and temporal coordinates
    geotiff file with bands in spatial coordinates

COMMAND LINE OPTIONS:
    -F X, --format X: input and output data format
        csv (default)
        netCDF4
        HDF5
        geotiff
    -v X, --variables X: variable names of data in csv, HDF5 or netCDF4 file
        for csv files: the order of the columns within the file
        for HDF5 and netCDF4 files: time, y, x and data variable names
    -H X, --header X: number of header lines for csv files
    -t X, --type X: input data type
        drift: drift buoys or satellite/airborne altimetry (time per data point)
        grid: spatial grids or images (single time for all data points)
    -e X, --epoch X: Reference epoch of input time (default Modified Julian Day)
        days since 1858-11-17T00:00:00
    -d X, --deltatime X: Input delta time for files without date information
        can be set to 0 to use exact calendar date from epoch
    -P X, --projection X: spatial projection as EPSG code or PROJ4 string
        4326: latitude and longitude coordinates on WGS84 reference ellipsoid
    -V, --verbose: Verbose output of processing run
    -M X, --mode X: Permission mode of output file

PYTHON DEPENDENCIES:
    numpy: Scientific Computing Tools For Python
        https://numpy.org
        https://numpy.org/doc/stable/user/numpy-for-matlab-users.html
    scipy: Scientific Tools for Python
        https://docs.scipy.org/doc/
    h5py: Python interface for Hierarchal Data Format 5 (HDF5)
        https://www.h5py.org/
    netCDF4: Python interface to the netCDF C library
         https://unidata.github.io/netcdf4-python/netCDF4/index.html
    gdal: Pythonic interface to the Geospatial Data Abstraction Library (GDAL)
        https://pypi.python.org/pypi/GDAL
    dateutil: powerful extensions to datetime
        https://dateutil.readthedocs.io/en/stable/
    pyproj: Python interface to PROJ library
        https://pypi.org/project/pyproj/

PROGRAM DEPENDENCIES:
    time.py: utilities for calculating time operations
    spatial.py: utilities for reading and writing spatial data
    utilities: download and management utilities for syncing files
    iers_mean_pole.py: provides the angular coordinates of IERS Mean Pole
    read_iers_EOP.py: read daily earth orientation parameters from IERS

UPDATE HISTORY:
    Updated 12/2020: merged time conversion routines into module
    Updated 11/2020: use internal mean pole and finals EOP files
        added options to read from and write to geotiff image files
    Updated 10/2020: using argparse to set command line parameters
    Updated 09/2020: can use HDF5 and netCDF4 as inputs and outputs
    Updated 10/2017: use mean pole coordinates from calc_mean_iers_pole.py
    Written 10/2017 for public release
"""
from __future__ import print_function

import sys
import os
import pyproj
import argparse
import numpy as np
import pyTMD.time
import pyTMD.spatial
import scipy.interpolate
from pyTMD.iers_mean_pole import iers_mean_pole
from pyTMD.read_iers_EOP import read_iers_EOP

#-- PURPOSE: compute the pole load tide radial displacements following
#-- IERS conventions (2010)
def compute_LPT_displacements(input_file, output_file,
    FORMAT='csv', VARIABLES=['time','lat','lon','data'], HEADER=0, TYPE='drift',
    TIME_UNITS='days since 1858-11-17T00:00:00', TIME=None, PROJECTION='4326',
    VERBOSE=False, MODE=0o775):

    #-- invalid value
    fill_value = -9999.0
    #-- output netCDF4 and HDF5 file attributes
    #-- will be added to YAML header in csv files
    attrib = {}
    #-- latitude
    attrib['lat'] = {}
    attrib['lat']['long_name'] = 'Latitude'
    attrib['lat']['units'] = 'Degrees_North'
    #-- longitude
    attrib['lon'] = {}
    attrib['lon']['long_name'] = 'Longitude'
    attrib['lon']['units'] = 'Degrees_East'
    #-- load pole tides
    attrib['tide_pole'] = {}
    attrib['tide_pole']['long_name'] = 'Solid_Earth_Pole_Tide'
    attrib['tide_pole']['description'] = ('Solid_Earth_pole_tide_radial_'
        'displacements_due_to_polar_motion')
    attrib['tide_pole']['reference'] = ('ftp://tai.bipm.org/iers/conv2010/'
        'chapter7/tn36_c7.pdf')
    attrib['tide_pole']['units'] = 'meters'
    attrib['tide_pole']['_FillValue'] = fill_value
    #-- time
    attrib['time'] = {}
    attrib['time']['long_name'] = 'Time'
    attrib['time']['units'] = 'days since 1858-11-17T00:00:00'
    attrib['time']['description'] = 'Modified Julian Days'
    attrib['time']['calendar'] = 'standard'

    #-- read input file to extract time, spatial coordinates and data
    if (FORMAT == 'csv'):
        dinput = pyTMD.spatial.from_ascii(input_file, columns=VARIABLES,
            header=HEADER, verbose=VERBOSE)
    elif (FORMAT == 'netCDF4'):
        dinput = pyTMD.spatial.from_netCDF4(input_file, timename=VARIABLES[0],
            xname=VARIABLES[2], yname=VARIABLES[1], varname=VARIABLES[3],
            verbose=VERBOSE)
    elif (FORMAT == 'HDF5'):
        dinput = pyTMD.spatial.from_HDF5(input_file, timename=VARIABLES[0],
            xname=VARIABLES[2], yname=VARIABLES[1], varname=VARIABLES[3],
            verbose=VERBOSE)
    elif (FORMAT == 'geotiff'):
        dinput = pyTMD.spatial.from_geotiff(input_file, verbose=VERBOSE)
        #-- copy global geotiff attributes for projection and grid parameters
        for att_name in ['projection','wkt','spacing','extent']:
            attrib[att_name] = dinput['attributes'][att_name]
    #-- update time variable if entered as argument
    if TIME is not None:
        dinput['time'] = np.copy(TIME)

    #-- converting x,y from projection to latitude/longitude
    #-- could try to extract projection attributes from netCDF4 and HDF5 files
    try:
        crs1 = pyproj.CRS.from_string("epsg:{0:d}".format(int(PROJECTION)))
    except (ValueError,pyproj.exceptions.CRSError):
        crs1 = pyproj.CRS.from_string(PROJECTION)
    crs2 = pyproj.CRS.from_string("epsg:{0:d}".format(4326))
    transformer = pyproj.Transformer.from_crs(crs1, crs2, always_xy=True)
    if (TYPE == 'grid'):
        ny,nx = (len(dinput['y']),len(dinput['x']))
        gridx,gridy = np.meshgrid(dinput['x'],dinput['y'])
        longitude,lat = transformer.transform(gridx.flatten(),gridy.flatten())
    elif (TYPE == 'drift'):
        longitude,lat = transformer.transform(dinput['x'].flatten(),
            dinput['y'].flatten())

    #-- extract time units from netCDF4 and HDF5 attributes or from TIME_UNITS
    try:
        time_string = dinput['attributes']['time']['units']
    except (TypeError, KeyError):
        epoch1,to_secs = pyTMD.time.parse_date_string(TIME_UNITS)
    else:
        epoch1,to_secs = pyTMD.time.parse_date_string(time_string)
    #-- convert dates to Modified Julian days (days since 1858-11-17T00:00:00)
    MJD = pyTMD.time.convert_delta_time(to_secs*dinput['time'].flatten(),
        epoch1=epoch1, epoch2=(1858,11,17,0,0,0), scale=1.0/86400.0)
    #-- add offset to convert to Julian days and then convert to calendar dates
    Y,M,D,h,m,s = pyTMD.time.convert_julian(2400000.5 + MJD, FORMAT='tuple')
    #-- calculate time in year-decimal format
    time_decimal = pyTMD.time.convert_calendar_decimal(Y,M,day=D,
        hour=h,minute=m,second=s)
    #-- number of time points
    nt = len(time_decimal)

    #-- degrees to radians
    dtr = np.pi/180.0
    atr = np.pi/648000.0
    #-- earth and physical parameters (IERS and WGS84)
    GM = 3.986004418e14#-- geocentric gravitational constant [m^3/s^2]
    a_axis = 6378136.6#-- semimajor axis of the WGS84 ellipsoid [m]
    flat = 1.0/298.257223563#-- flattening of the WGS84 ellipsoid
    b_axis = (1.0 - flat)*a_axis#-- semiminor axis of the WGS84 ellipsoid [m]
    omega = 7.292115e-5#-- mean rotation rate of the Earth [radians/s]
    #-- tidal love number appropriate for the load tide
    hb2 = 0.6207
    #-- Linear eccentricity, first and second numerical eccentricity
    lin_ecc = np.sqrt((2.0*flat - flat**2)*a_axis**2)
    ecc1 = lin_ecc/a_axis
    ecc2 = lin_ecc/b_axis
    #-- m parameter [omega^2*a^2*b/(GM)]. p. 70, Eqn.(2-137)
    m = omega**2*((1 -flat)*a_axis**3)/GM
    #-- flattening components
    f_2 = -flat + (5.0/2.0)*m + (1.0/2.0)*flat**2.0 - (26.0/7.0)*flat*m + \
        (15.0/4.0)*m**2.0
    f_4 = -(1.0/2.0)*flat**2.0 + (5.0/2.0)*flat*m

    #-- flatten heights
    h = dinput['data'].flatten() if ('data' in dinput.keys()) else 0.0
    #-- convert from geodetic latitude to geocentric latitude
    #-- geodetic latitude in radians
    latitude_geodetic_rad = lat*dtr
    #-- prime vertical radius of curvature
    N = a_axis/np.sqrt(1.0 - ecc1**2.0*np.sin(latitude_geodetic_rad)**2.0)
    #-- calculate X, Y and Z from geodetic latitude and longitude
    X = (N+h)*np.cos(latitude_geodetic_rad)*np.cos(longitude*dtr)
    Y = (N+h)*np.cos(latitude_geodetic_rad)*np.sin(longitude*dtr)
    Z = (N * (1.0 - ecc1**2.0) + h) * np.sin(latitude_geodetic_rad)
    rr = np.sqrt(X**2.0 + Y**2.0 + Z**2.0)
    #-- calculate geocentric latitude and convert to degrees
    latitude_geocentric = np.arctan(Z / np.sqrt(X**2.0 + Y**2.0))/dtr
    #-- geocentric colatitude and longitude in radians
    theta = dtr*(90.0 - latitude_geocentric)
    phi = longitude*dtr

    #-- compute normal gravity at spatial location and elevation of points.
    #-- normal gravity at the equator. p. 79, Eqn.(2-186)
    gamma_a = (GM/(a_axis*b_axis)) * (1.0-(3.0/2.0)*m - (3.0/14.0)*ecc2**2.0*m)
    #-- Normal gravity. p. 80, Eqn.(2-199)
    gamma_0 = gamma_a*(1.0 + f_2*np.cos(theta)**2.0 +
        f_4*np.sin(np.pi*latitude_geocentric/180.0)**4.0)
    #-- Normal gravity at height h. p. 82, Eqn.(2-215)
    gamma_h = gamma_0*(1.0 - \
        (2.0/a_axis)*(1.0+flat+m-2.0*flat*np.cos(theta)**2.0)*h + \
        (3.0/a_axis**2.0)*h**2.0)

    #-- pole tide files (mean and daily)
    mean_pole_file = pyTMD.utilities.get_data_path(['data','mean-pole.tab'])
    pole_tide_file = pyTMD.utilities.get_data_path(['data','finals.all'])
    #-- calculate angular coordinates of mean pole at time
    mpx,mpy,fl = iers_mean_pole(mean_pole_file,time_decimal,'2015')
    #-- read IERS daily polar motion values
    EOP = read_iers_EOP(pole_tide_file)
    #-- interpolate daily polar motion values to MJD using cubic splines
    xSPL = scipy.interpolate.UnivariateSpline(EOP['MJD'],EOP['x'],k=3,s=0)
    ySPL = scipy.interpolate.UnivariateSpline(EOP['MJD'],EOP['y'],k=3,s=0)
    px = xSPL(MJD)
    py = ySPL(MJD)
    #-- calculate differentials from mean pole positions
    mx = px - mpx
    my = -(py - mpy)

    #-- calculate radial displacement at time
    dfactor = -hb2*atr*(omega**2*rr**2)/(2.0*gamma_h)
    Srad = np.ma.zeros((len(latitude_geocentric)),fill_value=fill_value)
    Srad.data[:] = dfactor*np.sin(2.0*theta)*(mx*np.cos(phi) + my*np.sin(phi))
    #-- replace fill values
    Srad.mask = np.isnan(Srad.data)
    Srad.data[Srad.mask] = Srad.fill_value

    #-- calculate radial displacement at time
    if (TYPE == 'grid'):
        Srad = np.ma.zeros((ny,nx,nt),fill_value=fill_value)
        Srad.mask = np.zeros((ny,nx,nt),dtype=np.bool)
        for i in range(nt):
            SRAD=dfactor*np.sin(2.0*theta)*(mx[i]*np.cos(phi)+my[i]*np.sin(phi))
            #-- reform grid
            Srad.data[:,:,i]=np.reshape(SRAD, (ny,nx))
            Srad.mask[:,:,i]=np.isnan(SRAD)
    elif (TYPE == 'drift'):
        Srad = np.ma.zeros((nt),fill_value=fill_value)
        Srad.data[:] = dfactor*np.sin(2.0*theta)*(mx*np.cos(phi)+my*np.sin(phi))
        Srad.mask = np.isnan(Srad.data)
    #-- replace invalid data with fill values
    Srad.data[Srad.mask] = Srad.fill_value

    #-- output to file
    output = dict(time=MJD,lon=longitude,lat=lat,tide_pole=Srad)
    if (FORMAT == 'csv'):
        pyTMD.spatial.to_ascii(output, attrib, output_file, delimiter=',',
            columns=['time','lat','lon','tide_pole'], verbose=VERBOSE)
    elif (FORMAT == 'netCDF4'):
        pyTMD.spatial.to_netCDF4(output, attrib, output_file, verbose=VERBOSE)
    elif (FORMAT == 'HDF5'):
        pyTMD.spatial.to_HDF5(output, attrib, output_file, verbose=VERBOSE)
    elif (FORMAT == 'geotiff'):
        pyTMD.spatial.to_geotiff(output, attrib, output_file, verbose=VERBOSE,
            varname='tide_pole')
    #-- change the permissions level to MODE
    os.chmod(output_file, MODE)

#-- Main program that calls compute_LPT_displacements()
def main():
    #-- Read the system arguments listed after the program
    parser = argparse.ArgumentParser(
        description="""Calculates radial pole load tide displacements for
            an input file following IERS Convention (2010) guidelines
            """
    )
    #-- command line options
    #-- input and output file
    parser.add_argument('infile',
        type=lambda p: os.path.abspath(os.path.expanduser(p)), nargs='?',
        help='Input file')
    parser.add_argument('outfile',
        type=lambda p: os.path.abspath(os.path.expanduser(p)), nargs='?',
        help='Output file')
    #-- input and output data format
    parser.add_argument('--format','-F',
        type=str, default='csv', choices=('csv','netCDF4','HDF5','geotiff'),
        help='Input and output data format')
    #-- variable names (for csv names of columns)
    parser.add_argument('--variables','-v',
        type=str, nargs='+', default=['time','lat','lon','data'],
        help='Variable names of data in input file')
    #-- number of header lines for csv files
    parser.add_argument('--header','-H',
        type=int, default=0,
        help='Number of header lines for csv files')
    #-- input data type
    #-- drift: drift buoys or satellite/airborne altimetry (time per data point)
    #-- grid: spatial grids or images (single time for all data points)
    parser.add_argument('--type','-t',
        type=str, default='drift',
        choices=('drift','grid'),
        help='Input data type')
    #-- time epoch (default Modified Julian Days)
    #-- in form "time-units since yyyy-mm-dd hh:mm:ss"
    parser.add_argument('--epoch','-e',
        type=str, default='days since 1858-11-17T00:00:00',
        help='Reference epoch of input time')
    #-- input delta time for files without date information
    parser.add_argument('--deltatime','-d',
        type=float, nargs='+',
        help='Input delta time for files without date variables')
    #-- spatial projection (EPSG code or PROJ4 string)
    parser.add_argument('--projection','-P',
        type=str, default='4326',
        help='Spatial projection as EPSG code or PROJ4 string')
    #-- verbose output of processing run
    #-- print information about each input and output file
    parser.add_argument('--verbose','-V',
        default=False, action='store_true',
        help='Verbose output of run')
    #-- permissions mode of the local files (number in octal)
    parser.add_argument('--mode','-M',
        type=lambda x: int(x,base=8), default=0o775,
        help='Permission mode of output file')
    args = parser.parse_args()

    #-- set output file from input filename if not entered
    if not args.outfile:
        fileBasename,fileExtension = os.path.splitext(args.infile)
        vars = (fileBasename,'pole_tide',fileExtension)
        args.outfile = '{0}_{1}{2}'.format(*vars)

    #-- run load pole tide program for input file
    compute_LPT_displacements(args.infile, args.outfile, FORMAT=args.format,
        VARIABLES=args.variables, HEADER=args.header, TYPE=args.type,
        TIME_UNITS=args.epoch, TIME=args.deltatime, PROJECTION=args.projection,
        VERBOSE=args.verbose, MODE=args.mode)

#-- run main program
if __name__ == '__main__':
    main()
