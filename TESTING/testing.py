import pytplot
import pydivide
import pandas as pd 

# # PYDIVIDE STUFF #
# # Load data with pydivide
# insitu = pydivide.read('2017-06-19')
# 
# # Store time, alt, lat, lon as variables
# t = insitu['Time']
# alt = insitu['SPACECRAFT']['ALTITUDE']
# lat = insitu['SPACECRAFT']['SUB_SC_LATITUDE']
# lon = insitu['SPACECRAFT']['SUB_SC_LONGITUDE']
# 
# # Now store in tplot
# pytplot.store_data('sc_lat', data={'x': t, 'y': lat})
# pytplot.store_data('sc_lon', data={'x': t, 'y': lon})
# pytplot.store_data('sc_alt', data={'x': t, 'y': alt})
# 
# # Link everything together
# pytplot.link('sc_alt', 'sc_lat', link_type='lat')
# pytplot.link('sc_alt', 'sc_lon', link_type='lon')
# pytplot.link('sc_lat', 'sc_alt', link_type='alt')
# pytplot.link('sc_lon', 'sc_alt', link_type='alt')
# 
# # Allow crosshairs and crosshair legend
# # pytplot.tplot_options('crosshair', False)
# 
# # Control plot range
# # pytplot.tplot_options('map_x_range', [0, 50])
# # pytplot.tplot_options('map_y_range', [0, 50])
# 
# # Create a time series plot of longitude with latitude as a seperate axis on the bottom
# pytplot.tplot('sc_lon', var_label='sc_lat')
# 
# # Turns this into a plot of latitude vs altitude
# pytplot.options('sc_lat', 'alt', 1)
# pytplot.tplot(['sc_lat'])
# 
# # Turns this into a map of altitude
# pytplot.options('sc_alt', 'map', 1)
# pytplot.tplot(['sc_alt'])

# PYTPLOT STUFF #

# Load data with pytplot
var1 = pytplot.cdf_to_tplot(r"C:\Users\Elysia\Desktop\maven_code\maven_data\maven\data\sci\swe\l2\2017\06\mvn_swe_l2_svyspec_20170619_v04_r04.cdf", prefix='swe_1_')
# var2 = pytplot.cdf_to_tplot("/Users/juba8233/Projects/maven/maven_data/maven/data/sci/swe/l2/2017/12/mvn_swe_l2_svyspec_20171208_v04_r04.cdf", prefix = 'swe_2_')
# var3 = pytplot.cdf_to_tplot("/Users/juba8233/Projects/maven/maven_data/maven/data/sci/euv/l2/2017/06/mvn_euv_l2_bands_20170619_v09_r03.cdf", prefix="mvn_euv_")
# var4 = pytplot.cdf_to_tplot("/Users/juba8233/Projects/maven/maven_data/maven/data/sci/euv/l2/2017/06/mvn_euv_l2_bands_20170619_v11_r03.cdf", prefix="mvn_euv_2_")

print(pytplot.data_quants['swe_1_diff_en_fluxes'].data)
pytplot.data_quants['swe_1_diff_en_fluxes'].data.index = pd.to_datetime(pytplot.data_quants['swe_1_diff_en_fluxes'].data.index, unit='s')
pytplot.pdresample('swe_1_diff_en_fluxes','H')
print(pytplot.data_quants['swe_1_diff_en_fluxes'].data)
print('...................')
pytplot.data_quants['swe_1_diff_en_fluxes'].data.index = pytplot.data_quants['swe_1_diff_en_fluxes'].data.index.strftime('%y-%m-%d %H:%M:%S')
pytplot.data_quants['swe_1_diff_en_fluxes'].data.index = pytplot.tplot_utilities.str_to_int(pytplot.data_quants['swe_1_diff_en_fluxes'].data.index)
print(pytplot.data_quants['swe_1_diff_en_fluxes'].data)

# Set individual plot options
pytplot.options('swe_1_diff_en_fluxes', 'colormap', 'magma')
pytplot.options('swe_1_diff_en_fluxes', 'ztitle', 'FLUX')
pytplot.options('swe_1_diff_en_fluxes', 'ytitle', 'Energy')
pytplot.options("swe_1_diff_en_fluxes", "spec", 1)
pytplot.options("swe_1_diff_en_fluxes", 'panel_size', 1)
pytplot.options('swe_1_diff_en_fluxes', 'ylog', 1)
pytplot.options('swe_1_diff_en_fluxes', 'zlog', 1)
pytplot.options('swe_1_diff_en_fluxes', 'xlog_interactive', 1)
pytplot.options('swe_1_diff_en_fluxes', 'ylog_interactive', 1)
# pytplot.options('swe_1_diff_en_fluxes', 'xrange_interactive', [3.0, 4627.5])
# pytplot.options('swe_1_diff_en_fluxes', 'yrange_interactive', [19503.521, 4264502300.0])
pytplot.options('swe_1_diff_en_fluxes', 'crosshair_y', 'Energy')
pytplot.options('swe_1_diff_en_fluxes', 'crosshair_z', 'Flux')
pytplot.options('swe_1_diff_en_fluxes', 'xtitle', 'HI JULIE')
pytplot.options('swe_1_diff_en_fluxes', 't_average', 1200)
pytplot.options('swe_1_diff_en_fluxes', 'static', '2017-06-19 01:00:57')  # pattern = "%Y-%m-%d %H:%M:%S"
pytplot.options('swe_1_diff_en_fluxes', 'static_tavg', ['2017-06-19 12:00:00', '2017-06-19 13:00:00'])

# pytplot.options('swe_2_diff_en_fluxes', 'colormap', 'magma')
# pytplot.options('swe_2_diff_en_fluxes', 'ztitle', 'FLUX')
# pytplot.options('swe_2_diff_en_fluxes', 'ytitle', 'Energy')
# pytplot.options("swe_2_diff_en_fluxes", "spec", 1)
# pytplot.options("swe_2_diff_en_fluxes" , 'panel_size', 1)
# pytplot.options('swe_2_diff_en_fluxes', 'ylog', 1)
# pytplot.options('swe_2_diff_en_fluxes', 'zlog', 1)

# pytplot.options('swe_3_spectra_diff_en_fluxes', 'colormap', 'magma')
# # pytplot.options('swe_3_spectra_diff_en_fluxes', 'ztitle', 'FLUX')
# # pytplot.options('swe_3_spectra_diff_en_fluxes', 'ytitle', 'Energy')
# pytplot.options('swe_3_spectra_diff_en_fluxes', "spec", 1)
# pytplot.options('swe_3_spectra_diff_en_fluxes', 'panel_size', 1)
# pytplot.options('swe_3_spectra_diff_en_fluxes', 'ylog', 1)
# pytplot.options('swe_3_spectra_diff_en_fluxes', 'zlog', 1)
# pytplot.options('swe_3_spectra_diff_en_fluxes', 'xlog_interactive', 1)
# pytplot.options('swe_3_spectra_diff_en_fluxes', 'ylog_interactive', 1)
# # # pytplot.options('swe_3_diff_en_fluxes', 'xrange_interactive', [3.0, 4627.5])
# # # pytplot.options('swe_3_diff_en_fluxes', 'yrange_interactive', [19503.521, 4264502300.0])
# pytplot.options('swe_3_spectra_diff_en_fluxes', 'crosshair_y', 'Energy')
# pytplot.options('swe_3_spectra_diff_en_fluxes', 'crosshair_z', 'Flux')
# # pytplot.options('swe_3_spectra_diff_en_fluxes', 't_average', 1200)
# # pytplot.options('swe_3_spectra_diff_en_fluxes', 'static', '2017-07-26 00:00:04')  # pattern = "%Y-%m-%d %H:%M:%S"
# # pytplot.options('swe_3_spectra_diff_en_fluxes', 'static_tavg', ['2017-07-25 00:00:09', '2017-07-26 00:00:04'])
#
# # pytplot.options('mvn_euv_data', 'crosshair_x', 'TIMMMMEEE')
# # pytplot.options('mvn_euv_data', 'crosshair_y', 'DATAAA')
# #
# # pytplot.options("mvn_euv_data", 'legend_names', ['Low', 'Medium', 'High'])
#
# Set overall plot options
pytplot.tplot_options('wsize', [1000, 1000])
pytplot.tplot_options('title', "MAVEN Orbit 3355")
pytplot.tplot_options('title_size', 14)
# # pytplot.tplot_options('crosshair', False)
#
# Add a random time bar
pytplot.timebar('2017-06-19 01:15:32', thick=3, color='g')

# Plot
pytplot.tplot(['swe_1_diff_en_fluxes'])
# pytplot.tplot(['swe_3_spectra_diff_en_fluxes'], interactive=True)
