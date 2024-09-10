# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pyqtgraph as pg
import numpy as np
from .. import tplot_utilities
from pyqtgraph.Qt import QtCore, QtGui
import pytplot
from .CustomAxis.DateAxis import DateAxis
from .CustomImage.UpdatingImage import UpdatingImage
from .CustomImage.ColorbarImage import ColorbarImage
from .CustomAxis.BlankAxis import BlankAxis
from .CustomLegend.CustomLegend import CustomLegendItem
from .CustomAxis.AxisItem import AxisItem
from .CustomViewBox.NoPaddingPlot import NoPaddingPlot
from .CustomLinearRegionItem.CustomLinearRegionItem import CustomLinearRegionItem
from math import log10, floor
import pandas as pd

class TVarFigureSpec(pg.GraphicsLayout):
    def __init__(self, tvar_name, show_xaxis=False):

        # This sets the default number of points to use when creating a spectrogram image
        self.X_PIXEL_LENGTH = 1000
        self.Y_PIXEL_HEIGHT = 100

        self.tvar_name = tvar_name
        self.show_xaxis = show_xaxis
        self.crosshair = pytplot.tplot_opt_glob['crosshair']

        # Sets up the layout of the Tplot Object
        pg.GraphicsLayout.__init__(self)
        self.layout.setHorizontalSpacing(10)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.show_xaxis = show_xaxis
        if 'show_all_axes' in pytplot.tplot_opt_glob:
            if pytplot.tplot_opt_glob['show_all_axes']:
                self.show_xaxis = True
        # Set up the x axis
        if self.show_xaxis:
            self.xaxis = DateAxis(orientation='bottom')
            self.xaxis.setHeight(35)
            self.xaxis.enableAutoSIPrefix(enable=False)
        else:
            self.xaxis = DateAxis(orientation='bottom', showValues=False)
            self.xaxis.setHeight(0)
            self.xaxis.enableAutoSIPrefix(enable=False)
        # Set up the y axis
        self.yaxis = AxisItem('left')
        self.yaxis.setStyle(textFillLimits=pytplot.tplot_opt_glob["axis_tick_num"])  # Set an absurdly high number for the first 3, ensuring that at least 3 axis labels are always present
        # Creating axes to bound the plots with lines
        self.xaxis2 = DateAxis(orientation='top', showValues=False)
        self.xaxis2.setHeight(0)
        self.yaxis2 = AxisItem("right", showValues=False)
        self.yaxis2.setWidth(0)

        vb = NoPaddingPlot()
        # Generate our plot in the graphics layout
        self.plotwindow = self.addPlot(row=0, col=0, axisItems={'bottom': self.xaxis,
                                                                'left': self.yaxis,
                                                                'right': self.yaxis2,
                                                                'top': self.xaxis2}, viewBox=vb)

        # Turn off zooming in on the y-axis, time resolution is much more important
        self.plotwindow.setMouseEnabled(y=pytplot.tplot_opt_glob['y_axis_zoom'])

        if pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['border']:
            self.plotwindow.showAxis("top")
            self.plotwindow.showAxis("right")

        # Set up the view box needed for the legends
        self.legendvb = pg.ViewBox(enableMouse=False)
        self.legendvb.setMaximumWidth(100)
        self.legendvb.setXRange(0, 1, padding=0)
        self.legendvb.setYRange(0, 1, padding=0)
        self.addItem(self.legendvb, 0, 1)

        self.curves = []
        self.colors = self._setcolors()
        self.colormap = self._setcolormap()

        if pytplot.tplot_opt_glob['black_background']:
            self.labelStyle = {'font-size':
                               str(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['char_size'])
                               + 'pt', 'color': '#FFF',
                               'white-space': 'pre-wrap'}
        else:
            self.labelStyle = {'font-size':
                               str(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['char_size'])
                               + 'pt', 'color': '#000',
                               'white-space': 'pre-wrap'}

        # Set the font size of the axes
        font = QtGui.QFont()
        font.setPixelSize(pytplot.tplot_opt_glob['axis_font_size'])
        self.xaxis.setTickFont(font)
        self.yaxis.setTickFont(font)
        self.yaxis.setStyle(textFillLimits=pytplot.tplot_opt_glob["axis_tick_num"],
                            tickFont=font)  # Set an absurdly high number for the first 3, ensuring that at least 3 axis labels are always present

        # Set legend options
        self.hoverlegend = CustomLegendItem(offset=(0, 0))
        self.hoverlegend.setItem("Date:", "0")
        # Allow the user to set x-axis(time), y-axis, and z-axis data names in crosshairs
        self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].attrs['plot_options']['xaxis_opt']['crosshair'] + ':', "0")
        self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['crosshair'] + ':', "0")
        self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']['crosshair'] + ':', "0")
        self.hoverlegend.setVisible(False)
        self.hoverlegend.setParentItem(self.plotwindow.vb)

        # Just perform this operation once, so we don't need to keep doing it
        self.data_2d = pytplot.tplot_utilities.reduce_spec_dataset(name=self.tvar_name)

    @staticmethod
    def getaxistype():
        axis_type = 'time'
        link_y_axis = False
        return axis_type, link_y_axis

    def _set_crosshairs(self):
        if pytplot.tplot_opt_glob['black_background']:
            self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('w'))
            self.hLine = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('w'))
        else:
            self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('k'))
            self.hLine = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('k'))
        self.plotwindow.addItem(self.vLine, ignoreBounds=True)
        self.plotwindow.addItem(self.hLine, ignoreBounds=True)

    def _set_roi_lines(self):
        if 'roi_lines' in pytplot.tplot_opt_glob.keys():
            # Locating the two times between which there's a roi
            roi_1 = pytplot.tplot_utilities.str_to_int(pytplot.tplot_opt_glob['roi_lines'][0])
            roi_2 = pytplot.tplot_utilities.str_to_int(pytplot.tplot_opt_glob['roi_lines'][1])
            # find closest time to user-requested time
            x = pytplot.data_quants[self.tvar_name].coords['time']
            x_sub_1 = abs(x - roi_1 * np.ones(len(x)))
            x_sub_2 = abs(x - roi_2 * np.ones(len(x)))
            x_argmin_1 = np.nanargmin(x_sub_1)
            x_argmin_2 = np.nanargmin(x_sub_2)
            x_closest_1 = x[x_argmin_1]
            x_closest_2 = x[x_argmin_2]
            # Create a roi box
            roi = CustomLinearRegionItem(orientation=pg.LinearRegionItem.Vertical, values=[x_closest_1, x_closest_2])
            roi.setBrush([211, 211, 211, 130])
            roi.lines[0].setPen('r', width=2.5)
            roi.lines[1].setPen('r', width=2.5)
            self.plotwindow.addItem(roi)

    def buildfigure(self):
        self._setxrange()
        self._setyrange()
        self._setyaxistype()
        self._setzaxistype()
        self._setzrange()
        self._visdata()
        self._setxaxislabel()
        self._setyaxislabel()
        self._addlegend()
        self._addtimebars()
        self._addmouseevents()
        self._set_crosshairs()
        self._set_roi_lines()
        self._setxrange() # Need to change the x range again one last time, visualizing the data resets it

    def _setyaxislabel(self):
        ylabel = pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['axis_label'].replace(" \ ", " <br> ")
        if "axis_subtitle" in pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']:
            sublabel = pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['axis_subtitle'].replace(" \ ", " <br> ")
            self.yaxis.setLabel(f"{ylabel} <br> {sublabel}", **self.labelStyle)
        else:
            self.yaxis.setLabel(ylabel, **self.labelStyle)

    def _setxaxislabel(self):
        if self.show_xaxis:
            self.xaxis.setLabel(pytplot.data_quants[self.tvar_name].attrs['plot_options']['xaxis_opt']['axis_label'], **self.labelStyle)
        
    def getfig(self):
        return self

    def _visdata(self):
        # Determine if the data needs to be reformatted into a standard sized image
        try:
            if len(self.data_2d.coords['spec_bins'][0]) > 1:
                x, y, data = self._format_spec_data_as_image(x_pixel_length = self.X_PIXEL_LENGTH,
                                                             y_pixel_height = self.Y_PIXEL_HEIGHT)
            else:
                x = self.data_2d.coords['time'].values
                y = self.data_2d.coords['spec_bins'].values
                data = self.data_2d.values
        except TypeError:
            x = self.data_2d.coords['time'].values
            y = self.data_2d.coords['spec_bins'].values
            data = self.data_2d.values

        # Take the log of the y values if we are using a logarithmic y axis
        if self._getyaxistype() == 'log':
            y = np.log10(y)

        # The the log of the z values if we are using a logarithmic x axis
        if self._getzaxistype() == 'log':
            data[data <= 0] = np.nan
            data = np.log10(data)
            zmin = np.log10(self.zmin)
            zmax = np.log10(self.zmax)
        else:
            zmin = self.zmin
            zmax = self.zmax

        # Pass in the data to actually create the spectrogram image
        specplot = UpdatingImage(x, y, data, self.colormap, zmin, zmax)

        self.plotwindow.addItem(specplot)


    def _format_spec_data_as_image(self, x_pixel_length=1000, y_pixel_height=100):
        '''
        This function is used to format data where the coordinates of the y axis are time varying.  For instance, data
        collected at t=0 could be collected for energy bins at 100GHz, 200Ghz, and 300Ghz, but at t=1 the data was
        collected at 1GHz, 50GHz, and 100 Ghz.  This smooths things out over the image, and creates NaNs where data
        is missing.  These NaN's are displayed completely transparently in the UpdatingImage class.
        :return: x, y, data
        '''

        x = self.data_2d.coords['time'].values

        # Get a list of 1000 x values
        xp = np.linspace(np.nanmin(x), np.nanmax(x), x_pixel_length)

        # Grab data from only those values
        resampled_data_2d = self.data_2d.sel(time=xp, method='nearest')

        # Get a list of 100 y values between the min and the max y values
        if self._getyaxistype() == 'log':
            yp = np.logspace(np.log10(self.ymin), np.log10(self.ymax), y_pixel_height)
        else:
            yp = np.linspace(self.ymin, self.ymax, y_pixel_height)


        # Determine the closest y values for which we have data at each x value
        data_reformatted = [] # This will store the 1000x100 data array, ultimately forming the picture

        y_values_at_x0 = resampled_data_2d.coords['spec_bins'][0]
        closest_y_index_to_yp = []
        for yi in yp:
            closest_y_index_to_yp.append((np.abs(y_values_at_x0 - yi)).argmin())


        # For each xp, determine the closest value of x we have available. Then, determine the closest values of y at
        # each x, and determine the value at those points
        prev_bins = y_values_at_x0
        prev_closest_ys = closest_y_index_to_yp
        for i in range(0, x_pixel_length):
            y_values_at_xi = resampled_data_2d.coords['spec_bins'][i]
            if (y_values_at_xi == prev_bins).all():
                closest_y_index_to_yp = prev_closest_ys
            else:
                closest_y_index_to_yp = []
                for yi in yp:
                    closest_y_index_to_yp.append((np.abs(y_values_at_xi - yi)).argmin())
                prev_closest_ys = closest_y_index_to_yp
                prev_bins = y_values_at_xi

            # temp_data holds the values for those closest points for a particular point in time
            temp_data = resampled_data_2d[i][closest_y_index_to_yp].values

            # Try cutting the data off that is outside the bounds
            try:
                temp_data[yp < np.nanmin(y_values_at_xi)] = np.nan
                temp_data[yp > np.nanmax(y_values_at_xi)] = np.nan
            except RuntimeWarning:
                # If the entire bin is NaN the above stuff fails, so just continue on
                pass
            data_reformatted.append(temp_data)

        return xp, yp, np.array(data_reformatted)

    def _setyaxistype(self):
        if self._getyaxistype() == 'log':
            self.plotwindow.setLogMode(y=True)
        else:
            self.plotwindow.setLogMode(y=False)
        return

    def _addlegend(self):
        zaxis = AxisItem('right')
        zlabel = pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']['axis_label'].replace(" \ ", " <br> ")
        if "axis_subtitle" in pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']:
            zsublabel = pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']['axis_subtitle'].replace(" \ ", " <br> ")
            zaxis.setLabel(f"{zlabel} <br> {zsublabel}", **self.labelStyle)
        else:
            zaxis.setLabel(zlabel, **self.labelStyle)

        if self.show_xaxis:
            emptyAxis = BlankAxis('bottom')
            emptyAxis.setHeight(35)
            p2 = self.addPlot(row=0, col=1, axisItems={'right': zaxis, 'bottom': emptyAxis}, enableMenu=False,
                              viewBox=self.legendvb)
        else:
            p2 = self.addPlot(row=0, col=1, axisItems={'right': zaxis}, enableMenu=False, viewBox=self.legendvb)
            p2.hideAxis('bottom')

        p2.buttonsHidden = True
        p2.setMaximumWidth(100)
        p2.showAxis('right')
        p2.hideAxis('left')

        colorbar = ColorbarImage()
        colorbar.setImage(np.array([np.linspace(1, 2, 200)]).T)

        p2.addItem(colorbar)
        p2.setLogMode(y=(self.zscale == 'log'))
        p2.setXRange(0, 1, padding=0)
        colorbar.setLookupTable(self.colormap)
        if self.zscale == 'log':
            colorbar.setRect(QtCore.QRectF(0, np.log10(self.zmin), 1, np.log10(self.zmax) - np.log10(self.zmin)))
            # I have literally no idea why this is true, but I need to set the range twice
            p2.setYRange(np.log10(self.zmin), np.log10(self.zmax), padding=0)
            p2.setYRange(np.log10(self.zmin), np.log10(self.zmax), padding=0)
        else:
            colorbar.setRect(QtCore.QRectF(0, self.zmin, 1, self.zmax - self.zmin))
            p2.setYRange(self.zmin, self.zmax, padding=0)
        colorbar.setLookupTable(self.colormap)

    def _addmouseevents(self):
        if self.plotwindow.scene() is not None:
            self.plotwindow.scene().sigMouseMoved.connect(self._mousemoved)

    def round_sig(self, x, sig=4):
        return round(x, sig - int(floor(log10(abs(x)))) - 1)

    def _mousemoved(self, evt):
        # get current position
        pos = evt

        # if plot window contains position
        if self.plotwindow.sceneBoundingRect().contains(pos):
            mousePoint = self.plotwindow.vb.mapSceneToView(pos)
            # grab x and y mouse locations
            index_x = int(mousePoint.x())
            # set log magnitude if log plot
            if self._getyaxistype() == 'log':
                index_y = self.round_sig(10 ** (float(mousePoint.y())), 4)
            else:
                index_y = self.round_sig(float(mousePoint.y()), 4)

            # find closest time/data to cursor location
            x = np.asarray(self.data_2d.coords['time'].values)
            x_sub = abs(x - index_x * np.ones(len(x)))
            x_argmin = np.nanargmin(x_sub)
            x_closest = x[x_argmin]
            try:
                if len(self.data_2d.coords['spec_bins'][0]) > 1:
                    y = np.asarray((self.data_2d.coords['spec_bins'][x_argmin]))
                else:
                    y = np.asarray((self.data_2d.coords['spec_bins']))
            except:
                y = np.asarray((self.data_2d.coords['spec_bins']))

            y_sub = abs(y - index_y * np.ones(y.size))
            y_argmin = np.nanargmin(y_sub)
            y_closest = y[y_argmin]

            data_point = self.data_2d[x_argmin][y_argmin].values

            # Associate mouse position with current plot you're mousing over.
            pytplot.hover_time.change_hover_time(int(mousePoint.x()), name=self.tvar_name)

            # add crosshairs
            if self.crosshair:
                self._update_crosshair_locations(mousePoint.x(), mousePoint.y(), x_closest, y_closest, data_point)

        else:
            self.hoverlegend.setVisible(False)
            self.vLine.setVisible(False)
            self.hLine.setVisible(False)

    def _update_crosshair_locations(self, mouse_x, mouse_y, x_val, y_val, data_point):
        self.vLine.setPos(mouse_x)
        self.hLine.setPos(mouse_y)
        self.vLine.setVisible(True)
        self.hLine.setVisible(True)

        date = (pytplot.tplot_utilities.int_to_str(x_val))[0:10]
        time = (pytplot.tplot_utilities.int_to_str(x_val))[11:19]

        self.hoverlegend.setVisible(True)
        self.hoverlegend.setItem("Date:", date)
        # Allow the user to set x-axis(time), y-axis, and z-axis data names in crosshairs
        self.hoverlegend.setItem(
            pytplot.data_quants[self.tvar_name].attrs['plot_options']['xaxis_opt']['crosshair'] + ':', time)
        self.hoverlegend.setItem(
            pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['crosshair'] + ':', str(y_val))
        self.hoverlegend.setItem(
            pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']['crosshair'] + ':', str(data_point))

    def _getyaxistype(self):
        if 'y_axis_type' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']:
            return pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_axis_type']
        else:
            return 'linear'

    def _setzaxistype(self):
        if self._getzaxistype() == 'log':
            self.zscale = 'log'
        else:
            self.zscale = 'linear'

    def _getzaxistype(self):
        if 'z_axis_type' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']:
            return pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']['z_axis_type']
        else:
            return 'log'

    def _setcolors(self):
        if 'line_color' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']:
            return pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['line_color']
        else:
            return pytplot.tplot_utilities.rgb_color(['k', 'r', 'seagreen', 'b', 'darkturquoise', 'm', 'goldenrod'])

    def _setcolormap(self):
        if 'colormap' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']:
            for cm in pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['colormap']:
                return tplot_utilities.return_lut(cm)
        else:
            return tplot_utilities.return_lut("spedas")

    def _setxrange(self):
        # Check if x range is set.  Otherwise, x range is automatic.
        if 'x_range' in pytplot.tplot_opt_glob:
            self.plotwindow.setXRange(pytplot.tplot_opt_glob['x_range'][0], pytplot.tplot_opt_glob['x_range'][1])

    def _setyrange(self):
        self.ymin = pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][0]
        self.ymax = pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][1]
        if self._getyaxistype() == 'log':
            if pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][0] <= 0 or \
                    pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][1] <= 0:
                self.ymin = np.nanmin(pytplot.data_quants[self.tvar_name].coords['spec_bins'].values)
                self.ymax = np.nanmax(pytplot.data_quants[self.tvar_name].coords['spec_bins'].values)
            self.plotwindow.vb.setYRange(np.log10(self.ymin),
                                         np.log10(self.ymax),
                                         padding=0)
        else:
            self.plotwindow.vb.setYRange(self.ymin,
                                         self.ymax,
                                         padding=0)

    def _setzrange(self):
        # Get Z Range
        if 'z_range' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']:
            self.zmin = pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']['z_range'][0]
            self.zmax = pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']['z_range'][1]
        else:
            dataset_temp = pytplot.data_quants[self.tvar_name].where(pytplot.data_quants[self.tvar_name] != np.inf)
            dataset_temp = dataset_temp.where(dataset_temp != -np.inf)
            # Cannot have a 0 minimum in a log scale
            if self.zscale == 'log':
                dataset_temp = dataset_temp.where(dataset_temp > 0)
            self.zmax = dataset_temp.max().max().values
            self.zmin = dataset_temp.min().min().values

    def _addtimebars(self):
        # find number of times to plot
        dict_length = len(pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar'])
        # for each time
        for i in range(dict_length):
            # pull date, color, thickness
            date_to_highlight = pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar'][i]["location"]
            color = pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar'][i]["line_color"]
            thick = pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar'][i]["line_width"]
            # make infinite line w/ parameters
            # color = pytplot.tplot_utilities.rgb_color(color)
            infline = pg.InfiniteLine(pos=date_to_highlight, pen=pg.mkPen(color, width=thick))
            # add to plot window
            self.plotwindow.addItem(infline)

        return
