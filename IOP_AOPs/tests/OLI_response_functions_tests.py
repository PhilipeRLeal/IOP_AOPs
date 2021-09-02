import pandas as pd
import seaborn as sns

from IOP_AOPs import spectral_response_functions as SRF

from SRF.OLI_response_function_analysis import central_wavelength_function
del SRF


def get_OLI_response_data():

    filepath = r'IOP_AOPs/Spectral Response Functions/data/Ball_BA_RSR.v1.xlsx'

    all_dfs = pd.read_excel(filepath, sheet_name=None)

    General = pd.read_excel(filepath, sheet_name='GENERAL', header=[0, 1],

                            )

    sheets = all_dfs.keys()

    print(sheets)

    # concat all sheets at once:

    # df = pd.concat(pd.read_excel(workbook_url,
    #                sheet_name=None), ]
    #                ignore_index=True
    #               )

    df = pd.concat(
        [
            all_dfs[key] for key in sheets if key not in [
                'GENERAL', 'Pan']], names=[
                    'Band_name', 'id'], keys=[
                        key for key in sheets if key not in [
                            'GENERAL', 'Pan']]).set_index(
                                'Wavelength', append=True)

    df = df.reset_index(level=1, drop=True)

    return df, General


def test_OLI_response_functions():

    try:

        df, General = get_OLI_response_data()

        # Plotting the sensitivity of each Band

        palette = sns.color_palette("rocket_r")

        sns.relplot(
            data=df.reset_index(),
            x="Wavelength",
            y='BA RSR [watts]',
            col="Band_name",
            col_wrap=3,
            kind="line", palette=palette,
            height=5, aspect=.75,
            facet_kws=dict(sharex=True),
        )

        # Central wavelength

        RFB = {}

        for band in df.index.get_level_values('Band_name').unique():

            RFB_i = central_wavelength_function(df, band_name=band)
            print('central_wavelength: ', RFB_i)

            RFB[band] = RFB_i

        RFB = pd.Series(RFB, name='Center Wavelength [nm] - estimated')
        RFB.index.name = 'Bandname'

        Comparison = General.loc[:, 'Band'].merge(RFB, on='Bandname')

        assert isinstance(Comparison, pd.DataFrame)

    except BaseException:
        assert False
