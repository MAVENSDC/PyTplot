
import unittest
from pytplot.MPLPlotter.tplot import tplot
from pytplot import options, tplot_options, cdf_to_tplot, tlimit
import os

current_directory = os.path.dirname(os.path.realpath(__file__)) + os.path.sep

class MPLPlotter_tests(unittest.TestCase):
    def test_tlimit(self):
        cdf_to_tplot(current_directory + "/testfiles/mms1_fpi_brst_l2_dis-moms_20151016130524_v3.3.0.cdf")
        panels = ['mms1_dis_energyspectr_omni_brst', 'mms1_dis_bulkv_gse_brst', 'mms1_dis_numberdensity_brst']
        tlimit(['2015-10-16 13:06:10', '2015-10-16 13:06:20'])
        tplot_options('title', 'tlimit')
        tplot(panels, display=False, save_png=current_directory + 'tlimit')

    def test_options(self):
        """
        Creates a series of test images
        """
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
        tplot(panels, display=False, save_png=current_directory+'thick')
        options('mms1_dis_numberdensity_brst', 'thick', 1)

        tplot_options('title', 'alpha')
        options('mms1_dis_numberdensity_brst', 'alpha', 0.5)
        options('mms1_dis_energyspectr_omni_brst', 'alpha', 0.5)
        tplot(panels, display=False, save_png=current_directory+'alpha')
        options('mms1_dis_numberdensity_brst', 'alpha', 1)
        options('mms1_dis_energyspectr_omni_brst', 'alpha', 1)


if __name__ == '__main__':
    unittest.main()