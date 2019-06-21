Plotting
=============

tplot function
--------------


All plotting is called through the "tplot()" function.  If you'd like to customize how you plots are displayed,
it is assume that you have set them up prior to calling this function.

.. autofunction:: pytplot.tplot


Oveplotting
-----------

To combine two or more variables in the same plot, you need to create a new variable like so::

	pytplot.store_data("new_variable", data=["variable1_to_overplot", "variable2_to_overplot"])
	
Then when you plot this new variable, it will be a combination of the two variables given in "data".  

..note:
	Each variable should still retain the plot options you set for it, but I am still working out the kinks.  
	
	
Extra X axes
-------------

This is described above in the tplot function documentation, but this is such a widely used feature of tplot that it 
deserves its own subsection.  
	

	