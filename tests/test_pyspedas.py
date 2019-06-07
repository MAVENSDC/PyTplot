import pytplot

def test_pyspedas():
    from pyspedas.mms import mms_load_fgm, mms_load_mec, mms_load_edp, mms_load_dsp, mms_load_fpi, mms_load_hpca, \
        mms_load_feeps

    from pyspedas import time_string, time_double, tnames
    import numpy as np

    probe = '1'
    trange = ['2015-12-01/12:05:00', '2015-12-01/12:07:00']

    mms_load_fpi(probe=probe, datatype=['des-moms', 'dis-moms'], trange=trange)  # center_measurements?
    # mms_load_fgm(trange=trange)
    tnames = pytplot.tplot_names()

    DenIN = 'mms' + probe + '_dis_numberdensity_fast'
    DenEN = 'mms' + probe + '_des_numberdensity_fast'
    VIgseN = 'mms' + probe + '_dis_bulkv_gse_brst'
    VEgseN = 'mms' + probe + '_des_bulkv_gse_brst'
    SpecIN = 'mms' + probe + '_dis_energyspectr_omni_fast'
    SpecEN = 'mms' + probe + '_des_energyspectr_omni_fast'
    PADE_lowN = 'mms' + probe + '_des_pitchangdist_lowen_brst'
    PADE_midN = 'mms' + probe + '_des_pitchangdist_miden_brst'
    PADE_highN = 'mms' + probe + '_des_pitchangdist_highen_brst'
    TIperpN = 'mms' + probe + '_dis_tempperp_brst'
    TIparaN = 'mms' + probe + '_dis_temppara_brst'
    TEperpN = 'mms' + probe + '_des_tempperp_brst'
    TEparaN = 'mms' + probe + '_des_temppara_brst'

    pytplot.tplot([SpecIN, SpecEN, DenIN], testing=True)
    pytplot.tplot([SpecIN, SpecEN, DenIN], testing=True, bokeh=True, save_file='testing.png')