# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 14:54:54 2020

@author: Philipe_Leal
"""
import scipy
import numpy as np


def sensitivity_lambda(
        nm,
        interp_f,
        column='BA RSR [watts]',
        band_name='CoastalAerosol'):

    sensitivity_lm = interp_f(nm)

    return sensitivity_lm * nm


def central_wavelength_function(
        lookup_table,
        column='BA RSR [watts]',
        band_name='CoastalAerosol'):

    nm_min = lookup_table.loc[band_name].index.min()
    nm_max = lookup_table.loc[band_name].index.max()

    series = lookup_table.loc[band_name, column]

    interp_f = scipy.interpolate.interp1d(
        series.index, series.values, kind='cubic')

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
