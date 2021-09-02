# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 14:54:54 2020

@author: Philipe_Leal
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, sys
import geopandas as gpd
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
import glob
import seaborn as sns
import scipy

filepath = glob.glob(r'C:\Users\Philipe Leal\Downloads\Response_Functions_OLI\OLI\*xlsx')[0]

all_dfs = pd.read_excel(filepath, sheet_name=None)

General = pd.read_excel(filepath, sheet_name='GENERAL', header=[0,1], 
                       
                        )

sheets = all_dfs.keys()

print(sheets)

# concat all sheets at once:
    
    # df = pd.concat(pd.read_excel(workbook_url, sheet_name=None), ignore_index=True)
    
    
df = pd.concat([all_dfs[key] for key in sheets if key not in ['GENERAL', 'Pan']],
               names=['Band_name', 'id'],
               keys = [key for key in sheets if key not in ['GENERAL', 'Pan']]).set_index('Wavelength', append=True)



df = df.reset_index(level=1, drop=True)


# Plotting the sensitivity of each Band

palette = sns.color_palette("rocket_r")

sns.relplot(
    data=df.reset_index(),
    x="Wavelength", 
    y='BA RSR [watts]',
    col="Band_name",
    col_wrap=3,
    kind="line",  palette=palette,
    height=5, aspect=.75, facet_kws=dict(sharex=True),
)



######## Central wavelength


def sensitivity_lambda(nm, interp_f, column='BA RSR [watts]', band_name= 'CoastalAerosol'):
    
    
    sensitivity_lm = interp_f(nm) 
    
    return sensitivity_lm * nm


def central_wavelength_function(lookup_table, column='BA RSR [watts]', band_name= 'CoastalAerosol'):
    
    
    
    nm_min = lookup_table.loc[band_name].index.min()
    nm_max = lookup_table.loc[band_name].index.max()
    
    
    
    series = lookup_table.loc[band_name, column]
    
    interp_f = scipy.interpolate.interp1d(series.index, series.values, kind='cubic')
    
    
    
    central_wavelength = scipy.integrate.quadrature(sensitivity_lambda, 
                                          nm_min,
                                          nm_max, 
                                          maxiter=2000,
                                          args=(interp_f,
                                                column, 
                                                band_name)    
                                          )
    
    
    series = lookup_table.loc[band_name, column]
    
    
    return central_wavelength[0] / np.trapz(series)


RFB = {}

for band in df.index.get_level_values('Band_name').unique():
    
    
    RFB_i = central_wavelength_function(df, band_name=band)
    
    print('central_wavelength: ', RFB_i)
    
    RFB[band] = RFB_i

RFB = pd.Series(RFB, name='Center Wavelength [nm] - estimated')
RFB.index.name = 'Bandname'

Comparison = General.loc[:, 'Band'].merge(RFB, on='Bandname')

print(Comparison)
                
                