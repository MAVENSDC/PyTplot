# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from _collections import OrderedDict

import os
import sys
import xarray as xr

# xarray options
xr.set_options(keep_attrs=True)

using_graphics = False

# runs without Qt
# if not 'PYTPLOT_NO_GRAPHICS' in os.environ:
#     using_graphics = True
# else:
#     print("Turning off qt graphics.  Bokeh plotting is still enabled.")
#     using_graphics = False

try:
    import google.colab
    using_graphics = False
except:
    pass

# This variable will be constantly changed depending on what x value the user is hovering over
class HoverTime(object):
    hover_time = 0
    functions_to_call = []

    def register_listener(self, fn):
        self.functions_to_call.append(fn)
        return

    # New time is time we're hovering over, grabbed from TVarFigure(1D/Spec/Alt/Map)
    # name is whatever tplot we're currently hovering over (relevant for 2D interactive
    # plots that appear when plotting a spectrogram).
    def change_hover_time(self, new_time, name=None):
        self.hover_time = new_time
        for f in self.functions_to_call:
            try:
                f(self.hover_time, name)
            except Exception as e:
                print(e)
        return

if using_graphics:
    try:
        import pyqtgraph as pg
        from pyqtgraph.Qt import QtWidgets

        #Note: This is absolutely required for windows systems to work currently
        #But presumably it will be fixed at some point in the future
        if sys.platform.startswith('win'):
            pg.ptime.time = lambda: 0

        pg.setConfigOptions(imageAxisOrder='row-major')
        pg.setConfigOptions(background='w')


        class PlotWindow(QtWidgets.QMainWindow):
            def __init__(self):
                super().__init__()

            def init_savepng(self, exporter):
                if exporter is None:
                    return
                # Set up the save PNG button/call exportpng function that activates when user presses button
                exportdatapngaction = QtWidgets.QAction("Save PNG", self)
                exportdatapngaction.triggered.connect(lambda: self.exportpng(exporter))

                # Set up menu bar to display and call creation of save PNG button
                menubar = self.menuBar()
                menubar.setNativeMenuBar(False)
                menubar.addAction(exportdatapngaction)
                self.setWindowTitle('PyTplot Window')

            def exportpng(self, exporter):
                if exporter is None:
                    print("Cannot save the image.  Try installing h5py to get around this issue.")
                    return
                # Function called by save PNG button to grab the image from the plot window and save it
                fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Open file', 'pytplot.png', filter="png (*.png *.)")
                exporter.parameters()['width'] = tplot_opt_glob['window_size'][0]
                exporter.parameters()['height'] = tplot_opt_glob['window_size'][1]
                exporter.export(fname[0])

            def newlayout(self, layout):
                # Needed for displaying plots
                self.setCentralWidget(layout)

    except Exception as e:
        print("Qt graphics import failed with error " + str(e))
        print("Turning off qt graphics.  Bokeh plotting is still enabled.")
        using_graphics = False

# Global Variables
hover_time = HoverTime()
data_quants = OrderedDict()
interactive_window = None  # 2D interactive window that appears whenever plotting spectrograms w/ tplot.
# If option 't_average' is set by user, then x and y values on this plot are the average of the user-specified
# number of seconds for which the cursor location should be averaged.
static_window = None  # 2D window showing data at certain point in time from a spectrogram plot.
static_tavg_window = None  # 2D window showing averaged y and z data for a specified time range from a spectrogram plot.
tplot_opt_glob = dict(tools="xpan,crosshair,reset",
                      min_border_top=12, min_border_bottom=12,
                      title_align='center', window_size=[800, 800],
                      title_size='12pt', title_text='', crosshair=True,
                      data_gap=0, black_background=False, axis_font_size=12, axis_tick_num=[(0, 1000000000), (3, 1),],
                      y_axis_zoom=False)
lim_info = {}
extra_layouts = {}

if using_graphics:
    pytplotWindow_names = []
    pytplotWindows = []  # This is a list that will hold future qt windows
    from . import QtPlotter

    qt_plotters = {'qtTVarFigure1D': QtPlotter.TVarFigure1D,
                   'qtTVarFigureSpec': QtPlotter.TVarFigureSpec,
                   'qtTVarFigureAlt': QtPlotter.TVarFigureAlt,
                   'qtTVarFigureMap': QtPlotter.TVarFigureMap}

from .store_data import store_data, store
from .tplot import tplot
from .get_data import get_data, get
from .xlim import xlim
from .ylim import ylim
from .zlim import zlim
from .tlimit import tlimit
from pytplot.exporters.tplot_save import tplot_save
from .tplot_names import tplot_names
from .tnames import tnames
from pytplot.importers.tplot_restore import tplot_restore
from .get_timespan import get_timespan
from .tplot_options import tplot_options
from .tplot_rename import tplot_rename
from .tplot_copy import tplot_copy
from .replace_data import replace_data
from .replace_metadata import replace_metadata
from .get_ylimits import get_ylimits
from .timebar import timebar
from .del_data import del_data
from .timespan import timespan
from .options import options
from .timestamp import timestamp
from .time_double import time_float,time_double, time_float_one
from .time_string import time_string, time_datetime, time_string_one
from pytplot.importers.cdf_to_tplot import cdf_to_tplot
from pytplot.importers.netcdf_to_tplot import netcdf_to_tplot
from pytplot.importers.sts_to_tplot import sts_to_tplot
from .tplot_utilities import compare_versions
from .tplot_utilities import highlight
from .tplot_utilities import annotate
from .data_att_getters_setters import set_coords, get_coords, set_units, get_units
from .data_exists import data_exists
from .link import link
from .tres import tres
# Importing tdeflag here will cause a problem while the wrapper still exists in pyspedas.
# So rather than import *, we will import everything except tdeflag from tplot_math.
#from pytplot.tplot_math import *
from .tplot_math import add_across, add, avg_res_data, clip, crop, deflag, degap, derive, divide, flatten
from .tplot_math import interp_nan, tinterp, join_vec, multiply, resample, spec_mult, split_vec, subtract, pwr_spec
from .tplot_math import clean_spikes, tsmooth, smooth, tdotp, tcrossp, pwrspc, tpwrspc, dpwrspc, tdpwrspc
#from .tplot_math import tdeflag
from .tplot_math import tnormalize, subtract_median, subtract_average, time_clip, tkm2re, makegap


# set up logging/console output
import logging
from os import environ

logging_level = environ.get('PYTPLOT_LOGGING_LEVEL')
logging_format = environ.get('PYTPLOT_LOGGING_FORMAT')
logging_date_fmt = environ.get('PYTPLOT_LOGGING_DATE_FORMAT')

if logging_format is None:
    logging_format = '%(asctime)s: %(message)s'

if logging_date_fmt is None:
    logging_date_fmt = '%d-%b-%y %H:%M:%S'

if logging_level is None:
    logging_level = logging.INFO
else:
    logging_level = logging_level.lower()
    if logging_level == 'debug':
        logging_level = logging.DEBUG
    elif logging_level == 'info':
        logging_level = logging.INFO
    elif logging_level == 'warn' or logging_level == 'warning':
        logging_level = logging.WARNING
    elif logging_level == 'error':
        logging_level = logging.ERROR
    elif logging_level == 'critical':
        logging_level = logging.CRITICAL

logging.captureWarnings(True)

# basicConfig here doesn't work if it has previously been called
logging.basicConfig(format=logging_format, datefmt=logging_date_fmt, level=logging_level)

# manually set the logger options from the defaults/environment variables
logger = logging.getLogger()
logger_handler = logger.handlers[0]  # should exist since basicConfig has been called
logger_fmt = logging.Formatter(logging_format, logging_date_fmt)
logger_handler.setFormatter(logger_fmt)
logger.setLevel(logging_level)

# Start the App
if using_graphics:
    try:
        pg.mkQApp()
    except Exception as e:
        print("Qt graphics import failed with error " + str(e))
        print("Turning off qt graphics.  Bokeh plotting is still enabled.")
        using_graphics = False

    # Ok.  In possibly the weirdest turn of events, I get a warning that interrupts Qt specplots
    # if I DO NOT import this library.  There is an error about collections.abc in the ImageItem.render()
    # function in pyqtgraph that completely works FINE as long as I've imported this library somewhere before
    # that render function being called.  Why??
    # update 23 March 2022: egrimes bumped the indentation for this import to be under the using_graphics if statement
    # since this is only required for Qt
    import requests
