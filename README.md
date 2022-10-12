[![build](https://github.com/MAVENSDC/PyTplot/workflows/build/badge.svg)](https://github.com/MAVENSDC/PyTplot/actions)
[![DOI](https://zenodo.org/badge/68843190.svg)](https://zenodo.org/badge/latestdoi/68843190)

Full Documentation here: [https://pytplot.readthedocs.io/en/latest/](https://pytplot.readthedocs.io/en/latest/) 


Pytplot is a python package which aims to mimic the functionality of the IDL "tplot" libraries. 

These plots have several user interaction tools built in, such as zooming and panning.  The can be exported as standalone HTML files (to retain their interactivity) or as static PNG files.    

Pytplot can be used in python scripts, or interactively through IPython and the Jupyter notebook.  


Quick Start
===========

Install Python
---------------

You will need the Anaconda distribution of Python 3 in order to run pytplot.  

`Anaconda <https://www.continuum.io/downloads/>`_ comes with a suite of packages that are useful for data science. 


Install pytplot
----------------

Open up a terminal, and type::

	pip install pytplot
	
This will install pytplot and all of it's dependencies.  

You will also need to install nodejs.  This can be done through Anaconda with the following command::

	conda install -c bokeh nodejs

Running Pytplot
---------------

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


Copyright 2019 Regents of the University of Colorado. All Rights Reserved.
Released under the MIT license.
This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
Verify current version before use at: https://github.com/MAVENSDC/PyTplot
