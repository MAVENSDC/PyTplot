import os
from pytplot import tplot_restore, tplot, get

current_directory = os.path.dirname(os.path.realpath(__file__))


def test_basic_line():
    tplot_restore(os.path.join(current_directory, 'testfiles', 'mms1_dis_numberdensity_fast.tplot'))
    tplot('mms1_dis_numberdensity_fast', display=False, save_png='restore_basic_line')


def test_spec():
    tplot_restore(os.path.join(current_directory, 'testfiles', 'mms1_dis_energyspectr_omni_fast.tplot'))
    tplot('mms1_dis_energyspectr_omni_fast', display=False, save_png='restore_spec')


def test_vec():
    tplot_restore(os.path.join(current_directory, 'testfiles', 'mms1_dis_bulkv_gse_fast.tplot'))
    tplot('mms1_dis_bulkv_gse_fast', display=False, save_png='restore_vec')


def test_tensor():
    tplot_restore(os.path.join(current_directory, 'testfiles', 'mms1_dis_prestensor_gse_fast.tplot'))


# Disabled because the test file was too large
# def test_dist():
#     tplot_restore(os.path.join(current_directory, 'testfiles', 'mms1_dis_dist_fast.tplot'))


def test_data_att():
    tplot_restore(os.path.join(current_directory, 'testfiles', 'data_att_test.tplot'))
    m = get('tha_state_pos', metadata=True)
    assert 'data_att' in m
    assert 'coord_sys' in m['data_att']
    assert 'units' in m['data_att']
