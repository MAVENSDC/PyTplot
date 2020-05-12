import pytplot
import os

current_directory = os.path.dirname(os.path.realpath(__file__))

def test_math():

    pytplot.cdf_to_tplot(os.path.dirname(os.path.realpath(__file__)) + "/testfiles/mvn_euv_l2_bands_20170619_v09_r03.cdf")
    pytplot.tplot_names()

    pytplot.tplot_math.split_vec('mvn_euv_calib_bands')

    pytplot.tplot('mvn_euv_calib_bands_x', testing=True)

    pytplot.tplot_math.subtract('mvn_euv_calib_bands_x', 'mvn_euv_calib_bands_y', new_tvar='s')

    pytplot.tplot('s', testing=True)

    pytplot.tplot_math.add('s', 'mvn_euv_calib_bands_x', new_tvar='a')

    pytplot.tplot(['mvn_euv_calib_bands_x', 'a'], testing=True)

    pytplot.tplot_math.subtract('mvn_euv_calib_bands_x', 'mvn_euv_calib_bands_z', new_tvar='m')

    pytplot.tplot('m', testing=True)

    pytplot.tplot_math.divide('m', 'mvn_euv_calib_bands_z', new_tvar='d')

    pytplot.tplot('d', testing=True)

    pytplot.add_across('mvn_euv_calib_bands', new_tvar='data_summed')

    pytplot.tplot('mvn_euv_calib_bands', testing=True)

    pytplot.avg_res_data('data_summed', res=120)

    pytplot.tplot('data_summed', testing=True)

    pytplot.deflag('mvn_euv_calib_bands', 0, new_tvar='deflagged')

    pytplot.tplot('deflagged', testing=True)

    pytplot.flatten('mvn_euv_calib_bands')

    pytplot.tplot('data_flattened', testing=True)

    pytplot.join_vec(['mvn_euv_calib_bands_x', 'mvn_euv_calib_bands_y', 'mvn_euv_calib_bands_z'], new_tvar='data2')

    pytplot.tplot('data2', testing=True)

    pytplot.pwr_spec('mvn_euv_calib_bands_x')

    pytplot.tplot('mvn_euv_calib_bands_x_pwrspec', testing=True)

    pytplot.derive('mvn_euv_calib_bands_x')

    pytplot.store_data("data3", data=['mvn_euv_calib_bands_x', 'mvn_euv_calib_bands_y', 'mvn_euv_calib_bands_z'])

    pytplot.tplot('data3', testing=True)

    pytplot.cdf_to_tplot(os.path.dirname(os.path.realpath(__file__))+ "/testfiles/mvn_swe_l2_svyspec_20170619_v04_r04.cdf")

    pytplot.resample('mvn_euv_calib_bands_y', pytplot.data_quants['diff_en_fluxes'].coords['time'].values, new_tvar='data_3_resampled')

    pytplot.tplot('data_3_resampled', testing=True)
    pytplot.options('diff_en_fluxes', 'spec', 1)
    pytplot.spec_mult('diff_en_fluxes')

    pytplot.add_across('diff_en_fluxes_specmult', new_tvar='tot_en_flux', column_range=[[0, 10], [10, 20], [20, 30]])

    pytplot.options('diff_en_fluxes', 'ylog', 1)
    pytplot.options('diff_en_fluxes', 'zlog', 1)
    pytplot.options('tot_en_flux', 'ylog', 1)
    pytplot.ylim('tot_en_flux', 1, 100)
    pytplot.tplot(['diff_en_fluxes', 'tot_en_flux'], testing=True)

    pytplot.split_vec('tot_en_flux')

    pytplot.add('tot_en_flux_x', 'mvn_euv_calib_bands_y', new_tvar='weird_data')

    pytplot.tplot('weird_data', testing=True)
    