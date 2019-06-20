Tplot Variables
================

Every piece of data read into tplot is stored into global "tplot variable" (sometimes called "tvar" in the documentation).  

Every routine that deals with these variables uses simply their names to reference them, you do not need to pass the actual variables themselves around from function to function.  

If you would like to access the variable directly, they are stored in a global OrderedDict object called "data_quants", and can be found like so::

	pytplot.data_quants['tplot_variable_name_here']

Tplot variables are kept global because it is not unheard of for >50 variables to be read in from a single file satellite data file, and naming/keeping track of each variable can become cumbersome.    


Internal Structure
------------------

Users do not necessarily need to know the internal details of the tplot variables to use the library, but if you'd like to use tplot variables in other libraries this is good information to know.  

"Tplot variable" is really just a fancy name for an Xarray DataArrray object.  Tplot variables are just a type of DataArray that have standardized attributes so that PyTplot knows how to work with them

* There is always a "time" coordinate, and that time is in seconds since 1970.  
* For spectogram data, there is always a "spec_bins" coordinate that keeps track of the bin sizes on the yaxis 
* There is a "plot_options" attribute given to each tplot variable that is a large nested dictionary that keeps track of all plotting objects for the variable. 
* The dimensions stored are always "time", "y", "v", and for more mutlidimensional data there is "v2", "v3", etc

You can also access the pure underlying numpy arrays like so::

	#Data
	pytplot.data_quants['variable_name'].values
	#Time
	pytplot.data_quants['variable_name'].coords['time'].values
	#Spec bins
	pytplot.data_quants['variable_name'].coords['spec_bins'].values

