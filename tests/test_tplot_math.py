import pytplot
import os

current_directory = os.path.dirname(os.path.realpath(__file__))

def test_math():

    pytplot.cdf_to_tplot(os.path.dirname(os.path.realpath(__file__)) + "/testfiles/mvn_euv_l2_bands_20170619_v09_r03.cdf")
    pytplot.tplot_names()

    pytplot.tplot_math.split_vec('mvn_euv_calib_bands')

    pytplot.tplot('mvn_euv_calib_bands_x', display=False)

    pytplot.tplot_math.subtract('mvn_euv_calib_bands_x', 'mvn_euv_calib_bands_y', new_tvar='s')

    pytplot.tplot('s', display=False)

    pytplot.tplot_math.clean_spikes('mvn_euv_calib_bands_x',newname='despike')

    pytplot.tplot('despike',display=False)

    pytplot.tplot_math.add('s', 'mvn_euv_calib_bands_x', new_tvar='a')

    pytplot.tplot(['mvn_euv_calib_bands_x', 'a'], display=False)

    pytplot.tplot_math.subtract('mvn_euv_calib_bands_x', 'mvn_euv_calib_bands_z', new_tvar='m')

    pytplot.tplot('m', display=False)

    pytplot.tplot_math.divide('m', 'mvn_euv_calib_bands_z', new_tvar='d')

    pytplot.tplot('d', display=False)

    pytplot.add_across('mvn_euv_calib_bands', new_tvar='data_summed')

    pytplot.tplot('mvn_euv_calib_bands', display=False)

    pytplot.avg_res_data('data_summed', res=120)

    pytplot.tplot('data_summed', display=False)

    pytplot.deflag('mvn_euv_calib_bands', 0, newname='deflagged')

    pytplot.tplot('deflagged', display=False)

    pytplot.flatten('mvn_euv_calib_bands')

    pytplot.tplot('data_flattened', display=False)

    pytplot.join_vec(['mvn_euv_calib_bands_x', 'mvn_euv_calib_bands_y', 'mvn_euv_calib_bands_z'], newname='data2')

    pytplot.tplot('data2', display=False)

    # pytplot.pwr_spec('mvn_euv_calib_bands_x')

    pytplot.tplot('mvn_euv_calib_bands_x_pwrspec', display=False)

    pytplot.derive('mvn_euv_calib_bands_x')

    pytplot.store_data("data3", data=['mvn_euv_calib_bands_x', 'mvn_euv_calib_bands_y', 'mvn_euv_calib_bands_z'])

    pytplot.tplot('data3', display=False)

    pytplot.cdf_to_tplot(os.path.dirname(os.path.realpath(__file__))+ "/testfiles/mvn_swe_l2_svyspec_20170619_v04_r04.cdf")

    pytplot.tplot('data_3_resampled', display=False)
    pytplot.options('diff_en_fluxes', 'spec', 1)
    pytplot.spec_mult('diff_en_fluxes')

    pytplot.add_across('diff_en_fluxes_specmult', new_tvar='tot_en_flux', column_range=[[0, 10], [10, 20], [20, 30]])

    pytplot.options('diff_en_fluxes', 'ylog', 1)
    pytplot.options('diff_en_fluxes', 'zlog', 1)
    pytplot.options('tot_en_flux', 'ylog', 1)
    pytplot.ylim('tot_en_flux', 1, 100)
    pytplot.tplot(['diff_en_fluxes', 'tot_en_flux'], display=False)

    pytplot.split_vec('tot_en_flux')

    pytplot.add('tot_en_flux_x', 'mvn_euv_calib_bands_y', new_tvar='weird_data')

    pytplot.tplot('weird_data', display=False)
    