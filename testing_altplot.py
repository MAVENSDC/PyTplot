import pydivide
import pytplot

#Read in the data
insitu = pydivide.read('2017-06-19')

#Store time, alt, lat, lon as variables
t = insitu['Time']
alt = insitu['SPACECRAFT']['ALTITUDE']
lat = insitu['SPACECRAFT']['SUB_SC_LATITUDE']
lon = insitu['SPACECRAFT']['SUB_SC_LONGITUDE']

#Now store in tplot
pytplot.store_data('sc_lat', data={'x':t, 'y':lat})
pytplot.store_data('sc_lon', data={'x':t, 'y':lon})
pytplot.store_data('sc_alt', data={'x':t, 'y':alt})

#Link everything together
pytplot.link('sc_alt', 'sc_lat', link_type='lat')
pytplot.link('sc_alt', 'sc_lon', link_type='lon')
pytplot.link('sc_lat', 'sc_alt', link_type='alt')
pytplot.link('sc_lon', 'sc_alt', link_type='alt')

#Create a time series plot of longitude with latitude as a seperate axis on the bottom
pytplot.tplot('sc_lon', var_label='sc_lat')

#Turns this into a plot of latitude vs altitude
pytplot.options('sc_lat','alt', 1)
pytplot.tplot(['sc_lat'])

#Turns this into a map of altitude
pytplot.options('sc_alt', 'map', 1)
pytplot.tplot(['sc_alt'])


