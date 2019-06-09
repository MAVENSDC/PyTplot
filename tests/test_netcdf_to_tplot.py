import pytplot
import os

current_directory = os.path.dirname(os.path.realpath(__file__))

def test_goes_read():

    pytplot.netcdf_to_tplot(current_directory + "/testfiles/g15_xrs_2s_20170619_20170619.nc", time='time_tag')
    pytplot.xlim('2017-06-19 02:00:00', '2017-06-19 04:00:00')
    pytplot.ylim("B_COUNT", 17000, 18000)
    pytplot.timebar('2017-06-19 03:00:00', "B_COUNT", color=(100, 255, 0), thick=3)
    pytplot.timebar('2017-06-19 03:30:00', "B_COUNT", color='g')
    pytplot.options("B_COUNT", 'ylog', 1)
    pytplot.store_data("BCOUNTFLUX", data=["B_COUNT", "B_FLUX"])
    pytplot.tplot([1, 2, 3, 4, 5, 7], var_label=6, testing=True)