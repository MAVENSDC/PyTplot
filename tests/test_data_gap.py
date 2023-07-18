import pytplot
import os

current_directory = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
def test_data_gap():
    """
    Tests the data_gap option for individual variables and
    overall. Uses THEMIS SCM wave mode data because this has both
    short and long gaps.
    """
    pytplot.cdf_to_tplot(current_directory + "/testfiles/tha_l1_scw_20111211_v01.cdf")
    pytplot.tplot_copy('tha_scw', 'tha_scw2')

    #Global data_gap setup, removes big gaps
    pytplot.tplot_options('data_gap', 600.0)
    #Individual data_gap setup, for small gaps
    pytplot.options('tha_scw2', 'data_gap', 60.0)
    pytplot.tplot(['tha_scw','tha_scw2'], display=False, save_png=current_directory + 'datagap_test_global')
    #Check to see if the short gaps are NaN'd for 'tha_scw2'
    pytplot.tlimit(['2011-12-11 17:00:00', '2011-12-11 18:00:00'])
    pytplot.tplot(['tha_scw','tha_scw2'], display=False, save_png=current_directory + 'datagap_test_individual')
    #Turn off
    pytplot.tplot_options('data_gap', None)
    pytplot.options('tha_scw2', 'data_gap', None)
    pytplot.tlimit(full=True)
    pytplot.tplot(['tha_scw','tha_scw2'], display=False, save_png=current_directory + 'datagap_test_none')
    
