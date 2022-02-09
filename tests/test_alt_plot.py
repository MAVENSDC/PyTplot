import pytplot
import os
import numpy as np

current_directory = os.path.dirname(os.path.realpath(__file__))

def test_altitude_plot():

    pytplot.netcdf_to_tplot(current_directory + "/testfiles/g15_xrs_2s_20170619_20170619.nc", time='time_tag')
    pytplot.store_data('altitude', data={'x': pytplot.data_quants['A_COUNT'].coords['time'].values, 'y': np.arange(0, len(pytplot.data_quants['A_COUNT'].coords['time'].values), step=1)})
    pytplot.link('A_COUNT', 'altitude')
    pytplot.xlim('2017-06-19 02:00:00', '2017-06-19 04:00:00')
    pytplot.ylim("A_COUNT", 17000, 18000)
    pytplot.timebar('2017-06-19 03:00:00', "A_COUNT", color=(100, 255, 0), thick=3)
    pytplot.timebar('2017-06-19 03:30:00', "A_COUNT", color='g')
    pytplot.options("A_COUNT", 'alt', 1)
    pytplot.tplot(2, display=False)
    pytplot.tplot(2, testing=True, bokeh=True)