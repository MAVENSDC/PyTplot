Non-Time Series Plots
=====================

Sometimes plots other than time series may be desired.  Typically, this is either altitude or latitude/longitude plots.

Because tplot variables always have time on their x-axis, in order to get these types of plots you need to tell pytplot that two variables
are related to one another.  

In other words, if you have a tplot variable for altitude named "spacecraft_alt" and while the data is stored in the variable "spacecraft_data", you can tell pytplot that the two are related with the following command::
	
	pytplot.link("spacecraft_data", "spacecraft_alt", link_type = 'alt')

If the data are not on the same time cadence, the linked variable will be interpolated to match that of the data variable.  


Why Linking?
--------------
One may ask, why not just allow altitude/latitude/longitude to be the xaxis of the tplot variables?  
The answer, aside from the fact that this is a time-series manipulation library, is that time is still retained in the "backend" of the plots.  
For instance, the time value will display when you hover over the data, 
and if you mark specific times with either a vertical Time Bar or Region of Interest, then that point/area will be highlighted on the plot.    


Altitude Plot Example
---------------------

The following uses data taken from the MAVEN mission::
	
	# Store Data from a dictionary variable named "insitu" taken from elsewhere
	pytplot.store_data('sc_alt', data={'x':insitu['Time'] , 'y':insitu['SPACECRAFT']['ALTITUDE']})
	pytplot.store_data('euv_low', data={'x':insitu['Time'] , 'y':insitu['EUV']['IRRADIANCE_LOW']})
	pytplot.store_data('euv_lyman', data={'x':insitu['Time'] , 'y':insitu['EUV']['IRRADIANCE_LYMAN']})
	pytplot.store_data('euv_mid', data={'x':insitu['Time'] , 'y':insitu['EUV']['IRRADIANCE_MID']})
	# Link the EUV variables to "sc_alt"
	pytplot.link(["euv_mid"], "sc_alt", link_type='alt')
	pytplot.link(["euv_low"], "sc_alt", link_type='alt')
	pytplot.link(["euv_lyman"], "sc_alt", link_type='alt')
	#Specify that you'd like to overplot
	pytplot.store_data('euv', data=["euv_low","euv_mid","euv_lyman"])
	#Set Plot options
	pytplot.options("euv", 'alt', 1)
	pytplot.options("euv", 'ylog', 1)
	pytplot.ylim("euv", .000001, .02)
	pytplot.options("euv", "legend_names", ["Low", "Mid", "Lyman"])
	#Add a big blue marker at 3:23:00
	pytplot.timebar('2015-12-25 03:23:00', varname='euv', color='blue', thick=10)
	#Plot!
	pytplot.tplot("euv")




.. raw:: html
   :file: _images/altitude.html





Map Plot Example
----------------






.. raw:: html
   :file: _images/map.html