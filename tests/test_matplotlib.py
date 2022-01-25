
import numpy as np
from pytplot.MPLPlotter.tplot import tplot
from pytplot import get_data, store_data, options, tplot_options, cdf_to_tplot, tlimit, timebar
import os

current_directory = os.path.dirname(os.path.realpath(__file__)) + os.path.sep

"""
Creates a series of test images
"""
def test_simple():
    store_data('simple', data={'x': [1, 2, 3, 4, 5], 'y': [1, 5, 1, 5, 1]})
    tplot_options('title', 'simple')
    tplot('simple', display=False, save_png=current_directory + 'simple')

def test_margins():
    store_data('margins', data={'x': [1, 2, 3, 4, 5], 'y': [1, 5, 1, 5, 1]})
    tplot_options('title', 'margins')
    tplot_options('xmargin', [0.2, 0.2])
    tplot_options('ymargin', [0.2, 0.2])
    tplot('margins', display=False, save_png=current_directory + 'margins')
    tplot_options('xmargin', None)
    tplot_options('ymargin', None)

def test_timebar():
    cdf_to_tplot(current_directory + "/testfiles/mms1_fpi_brst_l2_dis-moms_20151016130524_v3.3.0.cdf")
    panels = ['mms1_dis_energyspectr_omni_brst', 'mms1_dis_bulkv_gse_brst', 'mms1_dis_numberdensity_brst']
    tplot_options('title', 'timebar')
    timebar('2015-10-16 13:06:20', color='r')
    timebar('2015-10-16 13:06:40', color='b')
    tplot(panels, display=False, save_png=current_directory + 'timebar')

def test_tlimit():
    cdf_to_tplot(current_directory + "/testfiles/mms1_fpi_brst_l2_dis-moms_20151016130524_v3.3.0.cdf")
    panels = ['mms1_dis_energyspectr_omni_brst', 'mms1_dis_bulkv_gse_brst', 'mms1_dis_numberdensity_brst']
    tlimit(['2015-10-16 13:06:10', '2015-10-16 13:06:20'])
    tplot_options('title', 'tlimit')
    tplot(panels, display=False, save_png=current_directory + 'tlimit')
    tlimit(full=True)

def test_vertical_spacing():
    cdf_to_tplot(current_directory + "/testfiles/mms1_fpi_brst_l2_dis-moms_20151016130524_v3.3.0.cdf")
    panels = ['mms1_dis_energyspectr_omni_brst', 'mms1_dis_bulkv_gse_brst', 'mms1_dis_numberdensity_brst']
    tplot_options('title', 'vertical_spacing')
    tplot_options('vertical_spacing', 0.0)
    tplot(panels, display=False, save_png=current_directory + 'vertical_spacing')
    tplot_options('vertical_spacing', None)

def test_charsize():
    cdf_to_tplot(current_directory + "/testfiles/mms1_fpi_brst_l2_dis-moms_20151016130524_v3.3.0.cdf")
    panels = ['mms1_dis_energyspectr_omni_brst', 'mms1_dis_bulkv_gse_brst', 'mms1_dis_numberdensity_brst']
    tplot_options('title', 'charsize')
    options('mms1_dis_bulkv_gse_brst', 'char_size', 20)
    tplot('mms1_dis_bulkv_gse_brst', display=False, save_png=current_directory + 'charsize')
    options('mms1_dis_bulkv_gse_brst', 'char_size', None)

def test_axis_font_size():
    cdf_to_tplot(current_directory + "/testfiles/mms1_fpi_brst_l2_dis-moms_20151016130524_v3.3.0.cdf")
    panels = ['mms1_dis_energyspectr_omni_brst', 'mms1_dis_bulkv_gse_brst', 'mms1_dis_numberdensity_brst']
    tplot_options('title', 'axis_font_size')
    tplot_options('axis_font_size', 20)
    tplot('mms1_dis_bulkv_gse_brst', display=False, save_png=current_directory + 'axis_font_size')
    tplot_options('axis_font_size', None)

def test_overplot():
    cdf_to_tplot(current_directory + "/testfiles/mms1_fpi_brst_l2_dis-moms_20151016130524_v3.3.0.cdf")
    store_data('combined', data='mms1_dis_energyspectr_omni_brst mms1_dis_numberdensity_brst')
    options('mms1_dis_numberdensity_brst', 'Color', 'w')
    tplot_options('title', 'overplot')
    options('combined', 'right_axis', True)
    tplot('combined', display=False, save_png=current_directory + 'overplot')

def test_pseudo_vars():
    store_data('var1', data={'x': [1, 2, 3, 4, 5], 'y': [3, 3, 3, 3, 3]})
    store_data('var2', data={'x': [1, 2, 3, 4, 5], 'y': [7, 7, 7, 7, 7]})
    store_data('var_combined', data=['var1', 'var2'])
    options('var_combined', 'yrange', [1, 10])
    tplot_options('title', 'pseudo_vars')
    tplot('var_combined', display=False, save_png=current_directory + 'pseudo_vars')

def test_errorbars():
    cdf_to_tplot(current_directory + "/testfiles/mms1_fpi_brst_l2_dis-moms_20151016130524_v3.3.0.cdf", get_support_data=True)
    d = get_data('mms1_dis_numberdensity_brst')
    e = get_data('mms1_dis_numberdensity_err_brst')
    store_data('n_with_err', data={'x': d.times, 'y': d.y, 'dy': e.y*5})
    tplot_options('title', 'error bars')
    tlimit(['2015-10-16 13:06:10', '2015-10-16 13:06:20'])
    tplot('n_with_err', display=False, save_png=current_directory + 'errorbars')
    tlimit(full=True)

def test_spec_interp():
    data = np.array([[0,       1,       2,       3,       4],
           [5,       6,       7,       8,       9],
          [10,      11,      12,      13,      14],
          [15,      16,      17,      18,      19],
          [20,      21,      22,      23,      24]])

    store_data('bins_1', data={'x': [1, 2, 3, 4, 5], 'y': data.transpose(), 'v': [10, 20, 30, 40, 50]})

    options('bins_1', 'spec', 1)
    options('bins_1', 'yrange', [0, 60.0])
    options('bins_1', 'Colormap', 'spedas')
    options('bins_1', 'y_interp', False)
    options('bins_1', 'x_interp', False)
    options('bins_1', 'y_interp_points', 10000.0)
    options('bins_1', 'x_interp_points', 10000.0)

    tplot_options('title', 'no interp')
    tplot('bins_1', display=False, save_png=current_directory + 'nointerp')

    tplot_options('title', 'X interp')
    options('bins_1', 'x_interp', True)
    tplot('bins_1', display=False, save_png=current_directory + 'xinterp')
    options('bins_1', 'x_interp', False)

    tplot_options('title', 'Y interp')
    options('bins_1', 'y_interp', True)
    tplot('bins_1', display=False, save_png=current_directory + 'yinterp')

    tplot_options('title', 'X and Y interp')
    options('bins_1', 'x_interp', True)
    tplot('bins_1', display=False, save_png=current_directory + 'xyinterp')

def test_options():
    cdf_to_tplot(current_directory + "/testfiles/mms1_fpi_brst_l2_dis-moms_20151016130524_v3.3.0.cdf")

    panels = ['mms1_dis_energyspectr_omni_brst', 'mms1_dis_bulkv_gse_brst', 'mms1_dis_numberdensity_brst']

    tplot_options('title', 'Basic')
    tplot(panels, display=False, save_png=current_directory + 'basic')

    tplot_options('title', 'ylog')
    options('mms1_dis_energyspectr_omni_brst', 'ylog', False)
    options('mms1_dis_bulkv_gse_brst', 'ylog', True)
    options('mms1_dis_numberdensity_brst', 'ylog', True)
    tplot(panels, display=False, save_png=current_directory+'ylog')
    options('mms1_dis_energyspectr_omni_brst', 'ylog', True)
    options('mms1_dis_bulkv_gse_brst', 'ylog', False)
    options('mms1_dis_numberdensity_brst', 'ylog', False)

    tplot_options('title', 'zlog')
    options('mms1_dis_energyspectr_omni_brst', 'zlog', False)
    tplot(panels, display=False, save_png=current_directory+'zlog')
    options('mms1_dis_energyspectr_omni_brst', 'zlog', True)

    tplot_options('title', 'yrange')
    options('mms1_dis_energyspectr_omni_brst', 'yrange', [1e2, 1e3])
    options('mms1_dis_bulkv_gse_brst', 'yrange', [-200, 200])
    options('mms1_dis_numberdensity_brst', 'yrange', [1, 15])
    tplot(panels, display=False, save_png=current_directory+'yrange')

    tplot_options('title', 'zrange')
    options('mms1_dis_energyspectr_omni_brst', 'zrange', [1e2, 1e7])
    tplot(panels, display=False, save_png=current_directory+'zrange')
    options('mms1_dis_energyspectr_omni_brst', 'zrange', [1e2, 1e8])

    tplot_options('title', 'ytitle')
    options('mms1_dis_energyspectr_omni_brst', 'ytitle', 'Set by test suite')
    tplot(panels, display=False, save_png=current_directory+'ytitle')
    options('mms1_dis_energyspectr_omni_brst', 'ytitle', 'DES energy')

    tplot_options('title', 'xtitle')
    options('mms1_dis_energyspectr_omni_brst', 'xtitle', 'Set by test suite')
    tplot(panels, display=False, save_png=current_directory+'xtitle')
    options('mms1_dis_energyspectr_omni_brst', 'xtitle', '')

    tplot_options('title', 'ztitle')
    options('mms1_dis_energyspectr_omni_brst', 'ztitle', 'Set by test suite')
    tplot(panels, display=False, save_png=current_directory+'ztitle')
    options('mms1_dis_energyspectr_omni_brst', 'ztitle', 'eflux')

    tplot_options('title', 'ysubtitle')
    options('mms1_dis_energyspectr_omni_brst', 'ysubtitle', 'Set by test suite')
    tplot(panels, display=False, save_png=current_directory+'ysubtitle')
    options('mms1_dis_energyspectr_omni_brst', 'ysubtitle', '')

    tplot_options('title', 'zsubtitle')
    options('mms1_dis_energyspectr_omni_brst', 'zsubtitle', 'Set by test suite')
    tplot(panels, display=False, save_png=current_directory+'zsubtitle')
    options('mms1_dis_energyspectr_omni_brst', 'zsubtitle', '')

    tplot_options('title', 'legend_names')
    options('mms1_dis_bulkv_gse_brst', 'legend_names', ['Vx data', 'Vy data', 'Vz data'])
    options('mms1_dis_numberdensity_brst', 'legend_names', 'density')
    tplot(panels, display=False, save_png=current_directory+'legend_names')
    options('mms1_dis_bulkv_gse_brst', 'legend_names', None)
    options('mms1_dis_numberdensity_brst', 'legend_names', None)

    tplot_options('title', 'line_style')
    options('mms1_dis_numberdensity_brst', 'line_style', 'dashed')
    tplot(panels, display=False, save_png=current_directory+'line_style')
    options('mms1_dis_numberdensity_brst', 'line_style', 'solid')

    tplot_options('title', 'thickness')
    options('mms1_dis_numberdensity_brst', 'thick', 4)
    options('mms1_dis_bulkv_gse_brst', 'thick', 4)
    tplot(panels, display=False, save_png=current_directory+'thick')
    options('mms1_dis_numberdensity_brst', 'thick', 0.5)
    options('mms1_dis_bulkv_gse_brst', 'thick', 0.5)

    tplot_options('title', 'alpha')
    options('mms1_dis_numberdensity_brst', 'alpha', 0.5)
    options('mms1_dis_energyspectr_omni_brst', 'alpha', 0.5)
    tplot(panels, display=False, save_png=current_directory+'alpha')
    options('mms1_dis_numberdensity_brst', 'alpha', 1)
    options('mms1_dis_energyspectr_omni_brst', 'alpha', 1)
