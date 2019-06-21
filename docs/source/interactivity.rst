Interactive Plots
==================

Part of the appeal of IDL tplot is that its easy to make plots that interact with the primary plotting window, primarily based on the time that the user is hovering the mouse over.  

For now, we have implemented one type of interactive plot that "slices" the spectrograms so that you can better see a single point in time.  


Spectrogram Slicing
-------------------




Adding your Own Supplementary Qt Plots
----------------------------------------

..note: 
	This only works when plotting with pyqtgraph.  Bokeh only creates static HTML files, so it cannot communicate back to python once created.  

If you using pytplot in an IPython environment (including Jupyter notebooks), you can call tplot multiple times and have multiple windows pop up without.  This is because IPython continually runs a qt "event loop" in the background, similar to IDL.

However, if you are using python in a non-interactive environment (say just running a script), pyqtgraph needs to start an event loop to run in.  Python will "freeze" and continue looking for events in the tplot window until the tplot window closes. 

This means that if you want multiple plots to appear at the same time, you need to supply a function to the tplot() command to call before it starts its event loop.  Lets say you have a custom plot you'd like to appear at the same time as the pytplot plot, you would make sure your function gets called with the following addition to the tplot command::
	
	pytplot.tplot(['variables_to_plot], extra_functions=[your_func])

Or, if you need to supply arguements to your function::

	pytplot.tplot(['variables_to_plot], extra_functions=[your_func], extra_function_args=[(arg1, arg2, arg3)])

Why would you want to ensure plots appear at the same time?  Mainly for interactivity purposes, as described in the following section. 



Adding Interactivity
--------------------

The way that the interactive plots work is that any time a mouse is moved in a pyqtgraph plotting window, pytplot will call all functions "registered" to its HoverTime class.  This class will supply the function with the new time the user is hovering over, and the tplot variable that the user is hovering over.  

If you have a function that you'd like called whenever the user hovers over a spot on the plots (say it updates your own personal plot window), you can register it like so::
	
	pytplot.hover_time.register_listener(your_update_func)


Custom Interactive Example
--------------------------

This is a very simple example that will create a qt window that displays what time the user is hovering over. ::

	import pytplot
	import pyqtgraph as pg

	window = pg.GraphicsWindow()

	def text_window():
		# Set up plotting window
		window.setWindowTitle('Interactive Window')
		plot = window.addPlot()
		# Add the text item
		textitem = pg.TextItem(html='<div style="text-align: center"><span style="color: #FFF;">This is the</span><br><span style="color: #FF0; font-size: 32pt;">PEAK</span></div>', anchor=(-0.3,0.5), border='w', fill=(0, 0, 255, 100))
		plot.addItem(textitem)
		textitem.setPos(1,1)
		# Define what the plot will do when the user
		# hovers over a new time
		def update(time, name):
			textitem.setText(str(time))

		# Register to update function above to pytplot
		pytplot.hover_time.register_listener(update)

	pytplot.store_data("test_data", data={'x':[100,200,300,400,500], 'y':[1,2,3,4,5]})

	pytplot.tplot("test_data", extra_functions=[text_window], extra_function_args=[()])

