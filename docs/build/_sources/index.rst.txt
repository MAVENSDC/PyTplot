.. PyTplot documentation master file, created by
   sphinx-quickstart on Wed Jul 12 12:31:41 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyTplot's documentation!
===================================

.. toctree::
   :maxdepth: 2

Introduction
------------

Pytplot is a python package which aims to mimic the functionality of the IDL "tplot" libraries. The primary routine (tplot) generates HTML files for the specified plots, and automatically opens the files in a Qt interface.

These plots have several user interaction tools built in, such as zooming and panning. The can be exported as standalone HTML files (to retain their interactivity) or as static PNG files.

Pytplot can be used in python scripts, or interactively through IPython and the Jupyter notebook.

How It Works
~~~~~~~~~~~~

Data is read into pytplot by using the "store_data" command.  Each dataset is assigned a unique name by the user.  

The data is stored in a "tplot variable" class.  The tplot variables contain all the information required to create a plot of the dataset.  The details of the plot, such as axis titles, types, line colors, etc, can be changed through other functions in pytplot.  

When you are ready to create a graph of your dataset(s), supply the dataset names you wish to plot to the "tplot" function, and a graph will be generated.   

Install Python
~~~~~~~~~~~~~~

You will need the Anaconda distribution of Python 3 in order to run pytplot.

`Anaconda <https://www.continuum.io/downloads/>`_ comes with a suite of packages that are useful for data science.

Running PyTplot
~~~~~~~~~~~~~~~

To start using pytplot in a similar manner to IDL tplot, start up an interactive environment through the terminal command::

	ipython 
	
or, if you prefer the jupyter interactive notebook::

	jupyter notebook
	
then, just import the package by typing the command::

	import pytplot

Storing Data in Memory
----------------------

store_data
~~~~~~~~~~~~~~~
.. automodule:: pytplot.store_data
   :members: store_data

tplot_rename
~~~~~~~~~~~~~~~
.. automodule:: pytplot.tplot_rename
	:members: tplot_rename
	
del_data
~~~~~~~~~~~~~~~
.. automodule:: pytplot.del_data
	:members: del_data

Retrieveing Data
----------------

get_data
~~~~~~~~~~~~~~~
.. automodule:: pytplot.get_data
   :members: get_data
   
get_timespan
~~~~~~~~~~~~~~~
.. automodule:: pytplot.get_timespan
	:members: get_timespan
	
get_ylimits
~~~~~~~~~~~~~~~
.. automodule:: pytplot.get_ylimits
	:members: get_ylimits

tplot_names
~~~~~~~~~~~~~~~
.. automodule:: pytplot.tplot_names
	:members: tplot_names
	
Setting Plot Options
--------------------

options
~~~~~~~~~~~~~~~
.. automodule:: pytplot.options
	:members: options
	
tplot_options
~~~~~~~~~~~~~~~
.. automodule:: pytplot.tplot_options
	:members: tplot_options

timebar
~~~~~~~~~~~~~~~
.. automodule:: pytplot.timebar
	:members: timebar
	
timespan
~~~~~~~~~~~~~~~
.. automodule:: pytplot.timespan
	:members: timespan
	
timestamp
~~~~~~~~~~~~~~~
.. automodule:: pytplot.timestamp
	:members: timestamp
	
xlim
~~~~~~~~~~~~~~~
.. automodule:: pytplot.xlim
	:members: xlim
	
ylim
~~~~~~~~~~~~~~~
.. automodule:: pytplot.ylim
	:members: ylim
	
zlim
~~~~~~~~~~~~~~~
.. automodule:: pytplot.zlim
	:members: zlim
	
Plotting Data
-------------

tplot
~~~~~~~~~~~~~~~
.. automodule:: pytplot.tplot
	:members: tplot
	
Saving and Restoring Sessions
-----------------------------

tplot_save
~~~~~~~~~~~~~~~
.. automodule:: pytplot.tplot_save
	:members: tplot_save
	
tplot_restore
~~~~~~~~~~~~~~~
.. automodule:: pytplot.tplot_restore
	:members: tplot_restore
	
.. only:: html

    Indices and tables
    ==================
    * :ref:`modindex`