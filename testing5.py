import pytplot
import numpy as np

pytplot.tplot_restore("C:/Code Repos/Pytplot/pytplot/sampledata/test_data.tplot")

pytplot.tplot_names()

pytplot.store_data('swia_vel-den', data=['swia_den','swia_vel'])

pytplot.data_quants['swia_den'].data[pytplot.data_quants['swia_den'].data < 0] = np.nan
pytplot.data_quants['swia_vel'].data[pytplot.data_quants['swia_vel'].data < 0] = np.nan
#Set individual plot options
pytplot.options('swia_counts', 'colormap', 'magma')
pytplot.options('swia_counts', 'ztitle', 'FLUX')
pytplot.options('swia_counts', 'ytitle', 'Energy')
pytplot.options("swia_counts", "spec", 1)
pytplot.options("swia_counts", "crosshair_y", "banana")
pytplot.options("swia_counts", "crosshair_z", "tomato")
pytplot.options("swia_counts" , 'panel_size', 1)
pytplot.options('swia_counts', 'ylog', 1)
pytplot.options('swia_counts', 'zlog', 1)
pytplot.options('swia_counts', 'ylog_interactive', 1)
pytplot.options('swia_counts', 'xlog_interactive', 1)
pytplot.options("mag", 'legend_names', ['MSO X', 'MSO Y', 'MSO Z'])
pytplot.options('swia_vel-den', 'ylog', 1)
pytplot.ylim('swia_vel-den', 1,100)
pytplot.options('swia_vel-den', 'panel_size', .5)
#pytplot.options('swia_vel-den', 'char_size', 5)
#pytplot.options('mag', 'panel_size', .5)
pytplot.options('SEP_2_ION', 'panel_size', .5)
pytplot.zlim('SEP_2_ION', 1, 100)
pytplot.ylim('mag', 20, 40)
pytplot.options('swia_vel-den', 'legend_names', ['SWIA Density', 'SWIA Velocity'])
#pytplot.options('diff_en_fluxes', 'static', '2017-06-19 12:30:00')
#pytplot.options('diff_en_fluxes', 'static_tavg', ['2017-06-19 05:30:00','2017-06-19 12:30:00'])
#Set overall plot options
pytplot.tplot_options('wsize', [1000,1000])
pytplot.tplot_options('title', "MAVEN Orbit 3355")
pytplot.tplot_options('title_size', 8)
#pytplot.tplot_options('crosshair', False)
#Add a random time bar
pytplot.xlim('2016-06-20 00:00:00', '2016-06-20 04:00:00')
pytplot.timespan('2016-06-20 00:00:00', 4, keyword='hours')
pytplot.timebar('2016-06-20 01:15:32', thick=3, color='g')
#Plot
pytplot.tplot([6,3,8], var_label='orbit', bokeh=True)
