import pytplot
import os
import numpy as np

current_directory = os.path.dirname(os.path.realpath(__file__))

def test_map_plot():
    pytplot.netcdf_to_tplot(current_directory + "/testfiles/g15_xrs_2s_20170619_20170619.nc", time='time_tag')

    pytplot.store_data('lat', data={'x': pytplot.data_quants['A_COUNT'].coords['time'].values, 'y': np.arange(0, 90, step=(90 / len(pytplot.data_quants['A_COUNT'].coords['time'].values)))})
    pytplot.link('A_COUNT', 'lat', link_type='lat')
    pytplot.store_data('lon', data={'x': pytplot.data_quants['A_COUNT'].coords['time'].values, 'y': np.arange(0, 360,step=(360 / len(pytplot.data_quants['A_COUNT'].coords['time'].values)))})
    pytplot.link('A_COUNT', 'lon', link_type='lon')
    pytplot.xlim('2017-06-19 02:00:00', '2017-06-19 04:00:00')
    pytplot.ylim("A_COUNT", 17000, 18000)
    pytplot.timebar('2017-06-19 03:00:00', "A_COUNT", color=(100, 255, 0), thick=3)
    pytplot.timebar('2017-06-19 03:30:00', "A_COUNT", color='g')
    pytplot.options("A_COUNT", 'map', 1)
    pytplot.tplot(2, testing=True)
    pytplot.tplot(2, testing=True, bokeh=True)