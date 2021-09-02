
# link> http://www.ioccg.org/groups/Software_OCA/QAA_v6_2014209.pdf
# QAA-V6


import numpy as np
import pandas as pd

from dependencies.aw_POPE_FRY_1996 import Aw


def get_bbw_lambda(lambda_nm=412, verbose=True):
    '''
    Description:
        This function returns the water back scattering (bbw)

    Returns:
        (float)
    '''

    bbw = 0.0038 * (400 / lambda_nm)**4.32

    return bbw


def get_aw_lambda(lambda_nm=412, verbose=True):
    '''
    Description:
        This function evaluates the absorption coefficient of water (aw).

    Returns aw

    '''

    aw_lambdas = Aw.set_index('nm')['aw']

    aw_lambdas.index = aw_lambdas.index.astype(float)

    lambda_nm = float(lambda_nm)

    if lambda_nm in aw_lambdas.index.values:

        return float(aw_lambdas[lambda_nm])

    else:

        nearest_aw_lambda_0 = get_nearest_column(
            list(aw_lambdas.index), lambda_nm)

        if verbose:
            print(
                'getting nearest water absortion \
                coeficient for lambda {}'.format(lambda_nm)
            )

            print('Lambda selected for aw(lambda0): \
                {0}\n'.format(
                str(nearest_aw_lambda_0)))

        return float(aw_lambdas[nearest_aw_lambda_0])


def get_rrs_lambda(Rrs_lambda):
    '''
    Description:
        This function return the remote sensing
        surface reflectance (L/E), also known as 'rrs'

    Return float

    '''

    return Rrs_lambda / (0.52 + (1.7 * Rrs_lambda))


def get_u_lambda(rrs_lambda, g0=0.089, g1=0.1245):

    return (-g0 + np.sqrt((g0**2) + 4 * g1 * rrs_lambda)) / 2 * g1


def get_Chi(rrs_lambda_443,
            rrs_lambda_490,
            rrs_lambda_55x,
            rrs_lambda_670):

    rrs_soma = (rrs_lambda_443 + rrs_lambda_490)

    denominator = (rrs_lambda_55x +
                   (5 * (rrs_lambda_670 / rrs_lambda_490)) * rrs_lambda_670

                   )

    Chi = np.log(rrs_soma / denominator)

    return Chi


def get_total_absortion_coeficient_lambda_0(Rrs_lambda_670,
                                            Rrs_lambda_443,
                                            Rrs_lambda_490,
                                            Chi,
                                            lambda_0=550,
                                            H_exponent_coefficients=None,
                                            verbose=False,
                                            ):
    '''
    Constants in H_exponent_coefficients were the average of the
    coefficients obtained by least-square fitting
    a(λ0) of the synthetic data set adopted by the IOCCG [2006]
    for SeaWiFS, MODIS, and MERIS bands. If None (default),
    Lee coefficients is applied.

    In short, one set of parameters is proposed for the
    three sensors
    (good enough for comparison of derived IOPs with in situ measurements),
    except the change of aw(λ0) values for each sensor.

    Separate sets of constants for each sensor are necessary
    if long-term and consistent IOP results from the three
    sensors are the goal.

    '''

    if H_exponent_coefficients is None:
        Lee_Coefficients = dict(h0=-1.145902928,
                                h1=-1.365828264,
                                h2=-0.469266028)
        H_exponent_coefficients = Lee_Coefficients

        del Lee_Coefficients

    h0, h1, h2 = H_exponent_coefficients.values()

    if Rrs_lambda_670 < 0.0015:  # in sr ** (-1) units

        exponent = (h0 + h1 * Chi + h2 * Chi)

        a_water_lambda_0 = 0.0005

        a_lambda_55x = a_water_lambda_0 + 10**(exponent)

        a_tot_lambda_0 = a_lambda_55x

        return a_tot_lambda_0

    else:

        a_water_lambda_0 = get_aw_lambda(lambda_nm=lambda_0, verbose=verbose)

        a_lambda_670 = a_water_lambda_0 + 0.39 * \
            (Rrs_lambda_670 / (Rrs_lambda_443 + Rrs_lambda_490))**1.14

        a_tot_lambda_0 = a_lambda_670

        return a_tot_lambda_0


def get_bbp_lambda_0(u_lambda_0,
                     a_tot_lambda_0,
                     bbw_lambda_670,
                     Rrs_lambda_670,
                     Reflectance_threshold_for_670=0.0015,
                     lambda_0=550
                     ):

    if np.any(Rrs_lambda_670 < Reflectance_threshold_for_670):

        bbw_lambda_55x = get_bbw_lambda(lambda_0)

        bbp_lambda_55x = (((u_lambda_0 * a_tot_lambda_0) / (1 - u_lambda_0))
                          * bbw_lambda_55x)

        bbp_lambda_0 = bbp_lambda_55x

    else:

        bbw_lambda_670 = get_bbw_lambda(670)

        bbp_lambda_670 = (((u_lambda_0 * a_tot_lambda_0) / (1 - u_lambda_0))
                          * bbw_lambda_670)

        bbp_lambda_0 = bbp_lambda_670

    return bbp_lambda_0


def get_Ni(bbp_lambda_0, rrs_lambda_443, rrs_lambda_55x):

    rrs_ratio = (rrs_lambda_443 / rrs_lambda_55x)

    Expo = np.exp((-0.9) * rrs_ratio)

    Ni = 2 * (1 - (1.2 * Expo))

    return Ni


def get_bbp_lambda(bbp_lambda_0, lambda_0, lambda_i, Ni):

    return bbp_lambda_0 * (lambda_0 / lambda_i)**Ni


def get_a_lambda(u_lambda, bbw_lambda, bbp_lambda):

    a_lambda = (1 - u_lambda) * (bbw_lambda + bbp_lambda) / u_lambda

    return a_lambda


def get_tau(rrs_lambda_443, rrs_lambda_55x):

    return (0.74 + (0.2 / (0.8 + rrs_lambda_443 + rrs_lambda_55x)))


def get_S(rrs_lambda_443, rrs_lambda_55x):

    return (0.015 + (0.002 / (0.6 + (rrs_lambda_443 / rrs_lambda_55x))))


def get_Csi(S):
    '''
        This function returns the letter ξ (Csi)
    '''

    return np.exp(S * (442.5 - 415.5))


def get_ag_lambda_443(
        a_lambda_412,
        a_lambda_443,
        tau,
        Csi,
        aw_lambda_412,
        aw_lambda_443):

    fracao_1 = (a_lambda_412 - tau * a_lambda_443) / (Csi - tau)

    fracao_2 = (aw_lambda_412 - tau * aw_lambda_443) / (Csi - tau)

    return fracao_1 - fracao_2


def get_adg_lambda(ag_lambda, S, lambda_i, lambda_0=443):

    adg_lambda = ag_lambda * np.exp(-S * (lambda_i - lambda_0))

    return adg_lambda


def get_aph_lambda(a_lambda, adg_lambda, aw_lambda):

    aph_lambda = a_lambda - adg_lambda - aw_lambda

    return aph_lambda


def get_nearest_column(column_list, pattern):

    pattern_idx = np.argmin([abs(x - pattern) for x in column_list])

    return column_list[pattern_idx]


def apply_QAA(Rrs_Data,
              lambda_sensor_step=1,
              lambda_0=550, verbose=True
              ):
    '''
    Description:
        This function evaluates the QAA algorithm
        over a pandas dataframe of reflectances.

    Input:
        Rrs_Data (pd.DataFrame):
            columns are spectral bands; rows are samples.
            Column names are the spectral bands applied

        lambda_sensor_step:
            it is the distance between the spectral
            bands applied in the dataframe.

           standard == 1.


        lambda_0 (float or int): reference spectral band.

        verbose: whether or not to show analysis texts.


    Returns
        dictionary with keys for:
            aph_lambda: spectral absorption coefficient of chlorophill-A
            adg_lambda: spectral absorption coefficient of particles and CDOM
            ag_443: spectral total absorption
            bbp_lambda: spectral back-scattering

        Each key contains all values of that given QAA
        coefficient per spectral band.

    '''

    lambda_range = np.arange(
        Rrs_Data.columns.min(),
        Rrs_Data.columns.max() + 1,
        lambda_sensor_step).astype(int)

    aw_lambda = pd.Series([get_aw_lambda(x)
                          for x in lambda_range], index=lambda_range)

    rrs_data = Rrs_Data.apply(get_rrs_lambda, axis=1)

    u_lambda = rrs_data.apply(get_u_lambda, axis=1)

    nearest_412_lambda = get_nearest_column(rrs_data.columns, 412)
    nearest_443_lambda = get_nearest_column(rrs_data.columns, 443)
    nearest_440_lambda = get_nearest_column(rrs_data.columns, 444)
    nearest_489_lambda = get_nearest_column(rrs_data.columns, 489)
    nearest_490_lambda = get_nearest_column(rrs_data.columns, 490)
    nearest_550_lambda = get_nearest_column(rrs_data.columns, 550)
    nearest_670_lambda = get_nearest_column(rrs_data.columns, 670)

    Chi = rrs_data.apply(lambda x: get_Chi(x[nearest_440_lambda],
                                           x[nearest_489_lambda],
                                           x[nearest_550_lambda],
                                           x[nearest_670_lambda]
                                           ),
                         axis=1)

    a_tot_lambda_0 = Rrs_Data.apply(
        lambda x: get_total_absortion_coeficient_lambda_0(
            Rrs_lambda_670=x[nearest_670_lambda],
            Rrs_lambda_443=x[nearest_443_lambda],
            Rrs_lambda_490=x[nearest_490_lambda],
            lambda_0=lambda_0,
            Chi=Chi,
            verbose=verbose),
        axis=1)

    u_lambda_0 = u_lambda[nearest_550_lambda]

    bbw_lambda_670 = get_bbw_lambda(670)

    Rrs_lambda_670 = Rrs_Data[nearest_670_lambda]

    bbp_lambda_0 = pd.Series(
        get_bbp_lambda_0(
            u_lambda_0,
            a_tot_lambda_0,
            bbw_lambda_670,
            Rrs_lambda_670,
            Reflectance_threshold_for_670=0.0015,
            lambda_0=lambda_0))

    Ni = get_Ni(
        bbp_lambda_0,
        rrs_data[nearest_443_lambda],
        rrs_data[nearest_550_lambda])

    lambdas_to_bbp = lambda_range

    bbp_lambda = pd.concat([pd.Series(get_bbp_lambda(
        bbp_lambda_0, lambda_0,
        x, Ni),
        name=x
    )
        for x in lambdas_to_bbp], axis=1
    )

    lambdas_to_bbw = lambda_range

    bbw_lambda = pd.Series(get_bbw_lambda(
        lambdas_to_bbw), index=lambdas_to_bbw)

    a_lambda = get_a_lambda(
        u_lambda, bbw_lambda[Rrs_Data.columns], bbp_lambda[Rrs_Data.columns])

    Tau = get_tau(rrs_data[nearest_443_lambda], rrs_data[nearest_550_lambda])

    S = get_S(rrs_data[nearest_443_lambda], rrs_data[nearest_550_lambda])

    Csi = get_Csi(S)

    ag_lambda = get_ag_lambda_443(a_lambda_412=a_lambda[nearest_412_lambda],
                                  a_lambda_443=a_lambda[nearest_443_lambda],
                                  tau=Tau,
                                  Csi=Csi,
                                  aw_lambda_412=aw_lambda[nearest_412_lambda],
                                  aw_lambda_443=aw_lambda[nearest_443_lambda])

    ag_lambda.name = 'ag_443'

    adg_lambda = pd.concat([get_adg_lambda(
        ag_lambda, S, C, lambda_0=443) for C in Rrs_Data.columns], axis=1)

    adg_lambda.columns = Rrs_Data.columns

    aph_lambda = get_aph_lambda(a_lambda, adg_lambda, aw_lambda)[
        Rrs_Data.columns]

    return {'aph_lambda': aph_lambda,
            'adg_lambda': adg_lambda,
            'ag_lambda': ag_lambda,
            'bbp_lambda': bbp_lambda}


if '__main__' == __name__:

    N_samples = 10

    Bandas = [412, 443, 489, 510, 555, 670]

    Random_data = np.random.randint(
        low=0, high=800, size=(N_samples, len(Bandas))) / 1000

    Rrs_Data = pd.DataFrame(Random_data, columns=Bandas)

    Rrs_Data.head()

    QAA_Results = apply_QAA(Rrs_Data)

    for k, v in QAA_Results.items():
        print(str(k), '\n' * 3, '-' * 50, '\n', v, '\n' * 3)
