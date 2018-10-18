
##########
pytplot
##########

Pytplot is a python package which aims to mimic the functionality of the IDL "tplot" libraries.  The primary routine (tplot) generates HTML files for the specified plots, and automatically opens the files in a Qt interface.   

These plots have several user interaction tools built in, such as zooming and panning.  The can be exported as standalone HTML files (to retain their interactivity) or as static PNG files.    

Pytplot can be used in python scripts, or interactively through IPython and the Jupyter notebook.  

How It Works
=============

Data is read into pytplot by using the "store_data" command.  Each dataset is assigned a unique name by the user.  

The data is stored in a "tplot variable" class.  The tplot variables contain all the information required to create a plot of the dataset.  The details of the plot, such as axis titles, types, line colors, etc, can be changed through other functions in pytplot.  

When you are ready to create a graph of your dataset(s), supply the dataset names you wish to plot to the "tplot" function, and a graph will be generated.   



Install Python
=============

You will need the Anaconda distribution of Python 3 in order to run pytplot.  

`Anaconda <https://www.continuum.io/downloads/>`_ comes with a suite of packages that are useful for data science. 


Install pytplot
=============

Open up a terminal, and type::

	pip install pytplot
	
This will install pytplot and all of it's dependencies.  

You will also need to install nodejs.  This can be done through Anaconda with the following command::

	conda install -c bokeh nodejs

Running Pytplot
=============

To start using pytplot in a similar manner to IDL tplot, start up an interactive environment through the terminal command::

	ipython 
	
or, if you prefer the jupyter interactive notebook::

	jupyter notebook
	
then, just import the package by typing the command::

	import pytplot

A demo/tutorial can be found here: `docs/pytplot_tutorial.html <http://htmlpreview.github.com/?https://github.com/MAVENSDC/PyTplot/blob/master/docs/pytplot_tutorial.html>`_.
	
A full description of each function can be found in `docs/build/index.html <http://htmlpreview.github.com/?https://github.com/MAVENSDC/PyTplot/blob/master/docs/build/index.html>`_.

Alternatively, the PDF version is located in `docs/build/PyTplot.pdf <https://github.com/MAVENSDC/PyTplot/blob/master/docs/build/PyTplot.pdf>`_.

Contact
=============

If you have any suggestions or notice any problems, don't hesitate to contact Bryan Harter: harter@lasp.colorado.edu 


# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot