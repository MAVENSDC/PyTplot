[![build](https://github.com/MAVENSDC/PyTplot/workflows/build/badge.svg)](https://github.com/MAVENSDC/PyTplot/actions)
[![DOI](https://zenodo.org/badge/68843190.svg)](https://zenodo.org/badge/latestdoi/68843190)

# pytplot - matplotlib version

Pytplot is a python package which aims to mimic the functionality of the IDL "tplot" libraries for analysis and visualization of heliophysics time series data.

This is the modified (matplotlib) version of the pytplot package. This version is used in the pyspedas project, which is a python rewrite of the IDL SPEDAS software.

Pytplot can be used in python scripts, or interactively through IPython and the Jupyter notebook.


## How It Works

Data is read into pytplot by using the "store_data" command.  Each dataset is assigned a unique name by the user.

The data is stored in a "tplot variable" class.  The tplot variables contain all the information required to create a plot of the dataset.  The details of the plot, such as axis titles, types, line colors, etc, can be changed through other functions in pytplot.


## Install Python

You need to install Python 3.8 or later.


## Install pytplot

Open up a terminal, and type::

	pip install pytplot-mpl-temp

This will install pytplot and all of it's dependencies.

Since this version is designed to be used with pyspedas, you can also install it by installing pyspedas:

	pip install pyspedas

To update the package to the latest released version, use:

	pip install pytplot-mpl-temp --upgrade
	pip install pyspedas --upgrade


## Running pytplot

To start using pytplot in a similar manner to IDL tplot, start up an interactive environment through the terminal command:

	ipython

or, if you prefer the jupyter interactive notebook:

	jupyter notebook

then, just import the package by typing the command:

	import pytplot


## Contact

If you have any suggestions or notice any problems, don't hesitate to contact Jim Lewis: jwl@ssl.berkeley.edu

The original version of pytplot was developed by Bryan Harter: harter@lasp.colorado.edu


## License

Released under the MIT license.


## Additional Information

PySPEDAS: https://github.com/spedas/pyspedas