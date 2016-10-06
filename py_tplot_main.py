from __future__ import division
import os
import datetime
from bokeh.io import output_file, show, gridplot
from options import options, tplot_options
from timestamp import TimeStamp
import pickle
import math
import pandas as pd
import numpy as np
import pytz
from bokeh.plotting import output_server
from bokeh.models import CustomJS, ColumnDataSource, Label, LogColorMapper, LogTicker, ColorBar, LinearColorMapper, BasicTicker, Legend
from bokeh.plotting.figure import Figure
from bokeh.models import (ColumnDataSource, CustomJS, DatetimeAxis,
                          HoverTool, LinearAxis, LogAxis, PanTool, Plot, Range1d, 
                          SaveTool, Span, Title, WheelZoomTool)
from bokeh.models.formatters import DatetimeTickFormatter, FuncTickFormatter,\
    NumeralTickFormatter
from bokeh.models.glyphs import Line
from bokeh.models.tools import RedoTool, UndoTool, CrosshairTool, LassoSelectTool, BoxZoomTool, ResetTool
from bokeh.driving import cosine
from bokeh.layouts import gridplot, widgetbox, layout
from openpyxl.worksheet import datavalidation
from _collections import OrderedDict
from bokeh.models.widgets.inputs import TextInput
#Global variable is data_quants
data_quants = OrderedDict()
tplot_num = 1

#Global variable for tplot options
tplot_opt_glob = dict(tools = "xpan,xwheel_zoom,crosshair,reset", 
                 min_border_top = 15, min_border_bottom = 0)
dttf = DatetimeTickFormatter(formats=dict(
            microseconds=["%H:%M:%S"],                        
            milliseconds=["%H:%M:%S"],
            seconds=["%H:%M:%S"],
            minsec=["%H:%M:%S"],
            minutes=["%H:%M:%S"],
            hourmin=["%H:%M:%S"],
            hours=["%H:%M"],
            days=["%F"],
            months=["%F"],
            years=["%F"]))
xaxis_opt_glob = dict(formatter = dttf)
title_opt = dict(align = 'center')
window_size = [800, 200]
lim_info = {}
extra_renderers = []
extra_layouts = {}
time_range_adjusted = False


def py_store_data(name, data=None, delete=False):
    global data_quants
    global title_opt
    global tplot_num
    create_time = datetime.datetime.now()
    
    if delete is True:
        py_del(name)
        return

    if data is None:
        print('Please provide data.')
        return
            
    df = pd.DataFrame(data['y'])
    if 'v' in data:
        spec_bins = data['v']
        df.columns = spec_bins.copy()
        spec_bins.sort()
        df = df.sort_index(axis=1)
    else:
        spec_bins = None
        
    times = data['x']
    df['Index'] = times
    df = df.set_index('Index', drop=True)
    
    trange = [np.nanmin(times), np.nanmax(times)]
    yaxis_opt = dict(axis_label = name)
    zaxis_opt = {}
    line_opt = {}
    dtype=''
    time_bar = []
    # Dictionary to keep track of extra details needed for plotting
    #     that aren't actual attributes in Bokeh
    extras = dict(panel_size = 1)
    tag_names = ['name', 'data', 'spec_bins', 'yaxis_opt', 'zaxis_opt', 'line_opt',
                 'trange','dtype','create_time', 'time_bar', 'extras', 'number']
    data_tags = [name, df, spec_bins, yaxis_opt, zaxis_opt, line_opt,
                 trange, dtype, create_time, time_bar, extras, tplot_num]
    # return a dictionary made from tag_names and data_tags
    temp = ( dict( zip( tag_names, data_tags ) ) )
    
    data_quants[name] = temp
    data_quants[tplot_num] = temp
        
    tplot_num += 1
    
    return

def py_del(name):
    global data_quants
    
    if not isinstance(name, list):
        name = [name]
    
    for i in name:
        if i not in data_quants.keys():
            print(str(i) + " is currently not in pytplot.")
            return
        
        temp_data_quants = data_quants[i]
        str_name = temp_data_quants['name']
        int_name = temp_data_quants['number']
        
        del data_quants[str_name]
        del data_quants[int_name]
    
    return
'''
def py_overplot(names):
    
    Combine the data from all of the names.
    Re-color lines so that none are the same color and can be distinguished.
    Introduce 'names' to the line making so they can be distinguished.
    In this case the legend would be automatic and use these names?
    Look at IDL to see what exactly I'm doing.
    
    return
'''
def str_to_int(time_str):
    epoch_t = "1970-1-1 00:00:00"
    pattern = "%Y-%m-%d %H:%M:%S"
    epoch_t1 = datetime.datetime.strptime(epoch_t, pattern)
    time_str1 = datetime.datetime.strptime(time_str, pattern)
    time_int = int((time_str1-epoch_t1).total_seconds())
    return time_int

def int_to_str(time_int):
    if math.isnan(time_int):
        return "NaN"
    else:
        return datetime.datetime.fromtimestamp(int(round(time_int)), tz=pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")

def py_xlim(min, max):
    global data_quants
    global lim_info
    global time_range_adjusted
    if not isinstance(min, (int, float, complex)):
        min = str_to_int(min)
    if not isinstance(max, (int, float, complex)):
        max = str_to_int(max)
    if 'x_range' in tplot_opt_glob:
        lim_info['xlast'] = tplot_opt_glob['x_range']
    # Allows the user to customize the limits before the variable
    #     has been plotted.
    else:
        lim_info['xfull'] = Range1d(min, max)
        lim_info['xlast'] = Range1d(min, max)
    tplot_opt_glob['x_range'] = Range1d(min, max)
    time_range_adjusted = False
    return

def py_ylim(name, min, max, log_opt=False):
    global data_quants
    
    if name not in data_quants.keys():
        print("That name is currently not in pytplot.")
        return
    
    temp_data_quant = data_quants[name]
    temp_data_quant['yaxis_opt']['y_range'] = [min, max]
    
    return

def py_zlim(name, min, max, log_opt=False):
    global data_quants
    
    if name not in data_quants.keys():
        print("That name is currently not in pytplot.")
        return
    
    temp_data_quant = data_quants[name]
    temp_data_quant['zaxis_opt']['z_range'] = [min, max]
    
    return

'''
ToDo: Add conversion from string to useable data in case of passing
          in time. e.g.: tlimit('12:30', '14:30') == tlimit(12.5, 14.5)
      Make it so when no arguments are passed in, the BoxZoomTool
          is selected. But is this actually necessary? If you're going
          to use the mouse anyway, why not just click the tool on the
          toolbar.
      When the BoxZoomTool is used to zoom in, the last should be
          updated so that it can go back even when the mouse is used.
          Right now just goes to full.
'''
# arg: can be a list of the min and max times to be taken
#      can be a string of 'full' or 'last'
#      can be a variable, and a variable plus a certain amount of time
def py_tlimit(arg):
    global lim_info
    
    if arg is 'last':
        xlast = lim_info['xlast']
        lim_info['xlast'] = tplot_opt_glob['x_range']
        tplot_opt_glob['x_range'] = xlast
    elif arg is 'full':
        tplot_opt_glob['x_range'] = lim_info['xfull']
    elif isinstance(arg, list):
        min = arg[0]
        max = arg[1]
        py_xlim(min, max)
        
    return

def py_options(name, option, value):
    global data_quants
    
    if not isinstance(name, list):
        name = [name]
    
    option = option.lower()
    
    for i in name:
        if i not in data_quants.keys():
            print(str(i) + " is currently not in pytplot.")
            return
        (new_yaxis_opt, new_zaxis_opt, new_line_opt, new_extras) = options(option, value, data_quants[i]['yaxis_opt'], data_quants[i]['zaxis_opt'], data_quants[i]['line_opt'], data_quants[i]['extras'])

        data_quants[i]['yaxis_opt'] = new_yaxis_opt
        data_quants[i]['zaxis_opt'] = new_zaxis_opt
        data_quants[i]['line_opt'] = new_line_opt
        data_quants[i]['extras'] = new_extras
    
    return

def py_tplot_options(option, value):
    global tplot_opt_glob
    global title_opt
    global window_size

    option = option.lower()
    
    (tplot_opt_glob, title_opt, window_size) = tplot_options(option, value, tplot_opt_glob, title_opt, window_size)
    
    return

def py_tplot(name, var_label = None, auto_color=False, interactive=False):
    global data_quants
    global time_range_adjusted
    
    # Name for .html file containing plots
    out_name = ""
    
    if(not isinstance(name, list)):
        name=[name]
        num_plots = 1
    else:
        num_plots = len(name)
    
    for i in range(num_plots):
        if name[i] not in data_quants.keys():
            print(str(i) + " is currently not in pytplot")
            return
    
    # Vertical Box layout to store plots
    all_plots = []
    #all_plots.append([dim_width, dim_height])
    #all_plots.append([dim_height])
    i = 0
    
    # Configure plot sizes
    total_psize = 0
    j = 0
    while(j < num_plots):
        total_psize += data_quants[name[j]]['extras']['panel_size']
        j += 1
    p_to_use = window_size[1]/total_psize
    
    # Create all plots  
    while(i < num_plots):
        interactive_plot=None
        temp_data_quant = data_quants[name[i]]
        yaxis_opt = temp_data_quant['yaxis_opt']
        zaxis_opt = temp_data_quant['zaxis_opt']
        line_opt = temp_data_quant['line_opt']
        
        p_height = int(temp_data_quant['extras']['panel_size'] * p_to_use)
        p_width = window_size[0]
        
        if temp_data_quant['spec_bins'] is not None:
            new_plot, interactive_plot = specplot(name[i], num_plots, last_plot = (i == num_plots-1), height=p_height, width=p_width, var_label=var_label, interactive=interactive)       
        else:
            # Make plot
            if 'x_range' not in tplot_opt_glob:
                tplot_opt_glob['x_range'] = Range1d(np.nanmin(temp_data_quant['data'].index.tolist()), np.nanmax(temp_data_quant['data'].index.tolist()))
                if i == num_plots-1:
                    lim_info['xfull'] = tplot_opt_glob['x_range']
                    lim_info['xlast'] = tplot_opt_glob['x_range']
            if 'y_range' not in yaxis_opt:
                ymin = min(temp_data_quant['data'].min(skipna=True).tolist())
                ymax = max(temp_data_quant['data'].max(skipna=True).tolist())
                yaxis_opt['y_range'] = [ymin - 1, ymax + 1]
            
            all_tplot_opt = {}
            all_tplot_opt.update(tplot_opt_glob)
            all_tplot_opt['y_range'] = Range1d(yaxis_opt['y_range'][0], yaxis_opt['y_range'][1])
            if 'y_axis_type' in yaxis_opt:
                all_tplot_opt['y_axis_type'] = yaxis_opt['y_axis_type']

            new_plot = Figure(x_axis_type='datetime', plot_height = p_height, plot_width = p_width, **all_tplot_opt)
            if not time_range_adjusted:
                new_plot.x_range.start = new_plot.x_range.start * 1000
                new_plot.x_range.end = new_plot.x_range.end * 1000
                time_range_adjusted = True
                
            if num_plots > 1 and i == num_plots-1:
                new_plot.plot_height += 22
            
            #Formatting stuff
            new_plot.grid.grid_line_color = None
            new_plot.axis.major_tick_line_color = None
            new_plot.axis.major_label_standoff = 0
            new_plot.xaxis.formatter = dttf
            new_plot.title = None
            
            #Check for time bars
            if temp_data_quant['time_bar']:
                time_bars = temp_data_quant['time_bar']
                for time_bar in time_bars:
                    time_bar_line = Span(location = time_bar['location'], dimension = time_bar['dimension'], line_color = time_bar['line_color'], line_width = time_bar['line_width'])
                    new_plot.renderers.extend([time_bar_line])
            new_plot.renderers.extend(extra_renderers)
            new_plot.toolbar.active_drag='auto'
            
            xaxis1 = DatetimeAxis(major_label_text_font_size = '0pt', **xaxis_opt_glob)
            new_plot.add_layout(xaxis1, 'above')
                
            #Turn off the axes for all but last plot    
            if num_plots > 1 and i != num_plots-1:
                new_plot.xaxis.major_label_text_font_size = '0pt'

            # Add lines
            if 'line_color' in temp_data_quant['extras']:
                multi_line_colors = temp_data_quant['extras']['line_color']
            else:
                multi_line_colors = ['black', 'red', 'green', 'navy', 'orange', 'firebrick', 'pink', 'blue', 'olive']
            
            yother = temp_data_quant['data']
            line_glyphs = []
            line_num = 0
            line_style = None
            if 'linestyle' in temp_data_quant['extras']:
                line_style = temp_data_quant['extras']['linestyle']
            for column_name in yother.columns:
                corrected_time = []
                for x in temp_data_quant['data'].index:
                    corrected_time.append(int_to_str(x))
                x = temp_data_quant['data'].index * 1000
                y = yother[column_name]
                line_opt = temp_data_quant['line_opt']
                line_source = ColumnDataSource(data=dict(x=x, y=y, corrected_time=corrected_time))
                if auto_color:
                    line = Line(x='x', y='y', line_color = multi_line_colors[line_num % len(multi_line_colors)], **line_opt)
                else:
                    line = Line(x='x', y='y', **line_opt)
                if 'line_style' not in line_opt:
                    if line_style is not None:
                        line.line_dash = line_style[line_num % len(line_style)]
                else:
                    line.line_dash = line_opt['line_style']
                line_glyphs.append(new_plot.add_glyph(line_source, line))
                line_num += 1
            
            #Set y/z labels
            new_plot.yaxis.axis_label = yaxis_opt['axis_label']
            #Add tools
            hover = HoverTool()
            hover.tooltips = [("Time","@corrected_time"), ("Value","@y")]
            new_plot.add_tools(hover)
            new_plot.add_tools(BoxZoomTool(dimensions=['width']))
            
            #Add the Legend is applicable
            if line_num>1 and ('legend_names' in yaxis_opt):
                if len(yaxis_opt['legend_names']) != line_num:
                    print("Number of lines do not match length of legend names")
                legend = Legend()
                legend.location = (0,0)
                legend_items =[]
                j=0
                for legend_name in yaxis_opt['legend_names']:
                    legend_items.append((legend_name, [line_glyphs[j]]))
                    j = j+1
                legend.legends = legend_items
                legend.label_text_font_size = "6pt"
                legend.border_line_color = None
                legend.glyph_height = int(p_height / (len(legend_items) + 1))
                new_plot.add_layout(legend, 'right')
            
        # Add name of variable to output file name
        if i == num_plots-1:    
            out_name += temp_data_quant['name']
        else:
            out_name += temp_data_quant['name'] + '+'
            
        # Add plot to GridPlot layout
        if interactive_plot is None:
            all_plots.append([new_plot])
        else:
            all_plots.append([new_plot, interactive_plot])
        i += 1 
           
    # Add date of data to the bottom left corner and timestamp to lower right
    # if py_timestamp('on') was previously called
    total_string = ""
    if 'time_stamp' in extra_layouts:
        total_string = extra_layouts['time_stamp']
    
    ts = TimeStamp(text = total_string)
    extra_layouts['data_time'] = ts
    all_plots.append([extra_layouts['data_time']])
        
    # Set all plots' x_range and plot_width to that of the bottom plot
    #     so all plots will pan and be resized together.
    k = 0
    while(k < num_plots - 1):
        all_plots[k][0].x_range = all_plots[num_plots - 1][0].x_range
        k += 1
    
    #
    #Add extra x axes if applicable 
    #
    if var_label is not None:
        if not isinstance(var_label, list):
            var_label = [var_label]
        
        x_axes = []
        x_axes_index = 0
        for new_x_axis in var_label:
            
            axis_data_quant = data_quants[new_x_axis]
            axis_start = min(axis_data_quant['data'].min(skipna=True).tolist())
            axis_end = max(axis_data_quant['data'].max(skipna=True).tolist())
            x_axes.append(Range1d(start = axis_start, end = axis_end))
            
            k = 0
            while(k < num_plots ):
                all_plots[k][0].extra_x_ranges['extra_'+str(new_x_axis)] = x_axes[x_axes_index]
                k += 1
            
            all_plots[k-1][0].add_layout(LinearAxis(x_range_name = 'extra_'+str(new_x_axis)), 'below')
            all_plots[k-1][0].plot_height += 22
            x_axes_index += 1
    
    # Add toolbar and title (if applicable) to top plot.
    #all_plots[0][0].toolbar_location = "above"  
    if 'text' in title_opt:
        title1 = Title(**title_opt)  
        all_plots[0][0].title = title1
        all_plots[0][0].plot_height += 22
    #final.children[0].add_tools(HoverTool())
    final = gridplot(all_plots)
    
    
    out_name += '.html'
    output_file(out_name)
    show(final)
    
    
    
    return

def py_get_data(name):
    '''
    ToDo: Figure out what the 'values' attribute in the
          IDL version means.
    '''
    global data_quants
    if name not in data_quants.keys():
        print("That name is currently not in pytplot")
        return
    
    temp_data_quant = data_quants[name]
    data_val = temp_data_quant['data'].values
    '''yother = temp_data_quant['data']
    for column_name in yother.columns:
        y = yother[column_name].values.tolist()
        print(y)
        data_val.append(y)'''
    time_val = temp_data_quant['data'].index
    
    return(time_val, data_val)

def py_get_names():
    global data_quants
    print(iter(data_quants))
    for key, value in data_quants.items():
        if isinstance(key, int):
            print(key, ":", data_quants[key]['name'])
        
    return

def py_overplot(new_name, names, auto_format = False):
    for i in names:
        if i not in data_quants.keys():
            print(str(i) + " is currently not in pytplot.")
            return
    new_time = None
    new_data = []
    if auto_format:
        linestyle_guide = ['solid', 'dashed', 'dotted', 'dashdot']
        linestyle_list = []
        linestyle_added = 0
    
    # obtain time
    (new_time, _) = py_get_data(names[0])
    time_len = len(new_time)
    # create internal lists in new_data based off new_time
    for time in new_time:
        new_data.append([])
    for temp_name in names:
        (_, temp_data) = py_get_data(temp_name)
        data_len = None
        i = 0
        data_len = len(temp_data[0])
        while(i < time_len):
            j = 0
            while(j < data_len):
                new_data[i].append(temp_data[i][j])
                j += 1
            i += 1

        # add linestyle to linestyle_list based on how many
        # lines there were and which # plot this is
        if auto_format:
            temp_linestyle = linestyle_guide[linestyle_added]
            i = 0
            while(i < data_len):
                linestyle_list.append(temp_linestyle)
                i += 1
            linestyle_added += 1

    py_store_data(new_name, data={'x':new_time, 'y':new_data})
    if auto_format:
        data_quants[new_name]['extras']['linestyle'] = linestyle_list

    return

def py_tplot_save(name, filename=None):
    global data_quants
    if name not in data_quants.keys():
        print("That name is currently not in pytplot") 
        return
    
    temp_data_quant = data_quants[name]
    if filename==None:
        filename="var_"+name+".pytplot"
    pickle.dump(temp_data_quant, open(filename, "wb"))
    
    return

def py_tplot_rename(old_name, new_name):
    global data_quants
    if old_name not in data_quants.keys():
        print("That name is currently not in pytplot")
        return
    if isinstance(old_name, int):
        old_name = data_quants[old_name]['name']
    
    data_quants[new_name] = data_quants.pop(old_name)
    
    return

def py_tplot_restore(file_name):
    global data_quants
    global tplot_num
    #Error check
    if not (os.path.isfile(file_name)):
        print("Not a valid file name")
        return
    
    #Check if the restored file was an IDL file
    
    if file_name.endswith('.tplot'):
        from scipy.io import readsav
        temp_tplot = readsav(file_name)
        for i in range(len(temp_tplot['dq'])):
            data_name = temp_tplot['dq'][i][0].decode("utf-8")
            temp_x_data = temp_tplot['dq'][i][1][0][0]
            #Pandas reads in data the other way I guess
            if len(temp_tplot['dq'][i][1][0][2].shape) == 2:
                temp_y_data = np.transpose(temp_tplot['dq'][i][1][0][2])
            else:
                temp_y_data = temp_tplot['dq'][i][1][0][2]
            
            
            #If there are more than 4 fields, that means it is a spectrogram 
            if len(temp_tplot['dq'][i][1][0]) > 4:
                temp_v_data = temp_tplot['dq'][i][1][0][4]
                
                #Change from little endian to big endian, since pandas apparently hates little endian
                #We might want to move this into the py_store_data procedure eventually
                if (temp_x_data.dtype.byteorder == '>'):
                    temp_x_data = temp_x_data.byteswap().newbyteorder()
                if (temp_y_data.dtype.byteorder == '>'):
                    temp_y_data = temp_y_data.byteswap().newbyteorder()
                if (temp_v_data.dtype.byteorder == '>'):
                    temp_v_data = temp_v_data.byteswap().newbyteorder()
                
                py_store_data(data_name, data={'x':temp_x_data, 'y':temp_y_data, 'v':temp_v_data})
            else:
                #Change from little endian to big endian, since pandas apparently hates little endian
                #We might want to move this into the py_store_data procedure eventually
                if (temp_x_data.dtype.byteorder == '>'):
                    temp_x_data = temp_x_data.byteswap().newbyteorder()
                if (temp_y_data.dtype.byteorder == '>'):
                    temp_y_data = temp_y_data.byteswap().newbyteorder()
                py_store_data(data_name, data={'x':temp_x_data, 'y':temp_y_data})
            
            #Still have no idea what "lh" is
            #data_quants[data_name]['lh'] = temp_tplot['dq'][i][2]
            
            #Need to loop through the options and determine what goes where
            if temp_tplot['dq'][i][3].dtype.names is not None:
                for option_name in temp_tplot['dq'][i][3].dtype.names:
                    py_options(data_name, option_name, temp_tplot['dq'][i][3][option_name][0])
            
            data_quants[data_name]['trange'] =  temp_tplot['dq'][i][4].tolist()
            data_quants[data_name]['dtype'] =  temp_tplot['dq'][i][5]
            data_quants[data_name]['create_time'] =  temp_tplot['dq'][i][6]
        
        ###################################################################    
        #TODO: temp_tplot['tv']
        
        #if temp_tplot['tv'][0][0].dtype.names is not None:
        #    for option_name in temp_tplot['tv'][0][0].dtype.names:
        #        py_tplot_options(option_name, temp_tplot['tv'][0][0][option_name][0])
        #'tv' stands for "tplot variables"
        #temp_tplot['tv'][0][0] is all of the "options" variables
            #For example, TRANGE_FULL, TRANGE, REFDATE, DATA_NAMES
        #temp_tplot['tv'][0][1] is all of the "settings" variables
            #temp_tplot['tv'][0][1]['D'][0] is "device" options
            #temp_tplot['tv'][0][1]['P'][0] is "plot" options
            #temp_tplot['tv'][0][1]['X'][0] is x axis options
            #temp_tplot['tv'][0][1]['Y'][0] is y axis options
        ####################################################################
    else:
        temp_data_quant = pickle.load(open(file_name,"rb"))
        data_quants[temp_data_quant['name']] = temp_data_quant
        data_quants[temp_data_quant['number']] = temp_data_quant
        tplot_num += 1
    
    return

def py_get_timespan(name):
    global data_quants
    if name not in data_quants.keys():
        print("That name is currently not in pytplot") 
        return
    print("Start Time: " + int_to_str(data_quants[name]['trange'][0]))
    print("End Time:   " + int_to_str(data_quants[name]['trange'][1]))
    
    return(data_quants[name]['trange'][0], data_quants[name]['trange'][1])
    
def py_get_ylimits(name, trg = None):
    global data_quants
    if not isinstance(name, list):
        name = [name]
    name_num = len(name)
    ymin = None
    ymax = None
    for i in range(name_num):
        if name[i] not in data_quants.keys():
            print(str(name[i]) + " is currently not in pytplot.")
            return
        temp_data_quant = data_quants[name[i]]
        yother = temp_data_quant['data']
        if trg is not None:
            for column_name in yother.columns:
                y = yother[column_name]
                trunc_tempt_data_quant = y.truncate(before = trg[0], after = trg[1])
                loc_min = trunc_tempt_data_quant.min(skipna=True)
                loc_max = trunc_tempt_data_quant.max(skipna=True)
                if (ymin is None) or (loc_min < ymin):
                    ymin = loc_min
                if (ymax is None) or (loc_max > ymax):
                    ymax = loc_max
        else:
            for column_name in yother.columns:
                y = yother[column_name]
                loc_min = y.min(skipna=True)
                loc_max = y.max(skipna=False)
                if (ymin is None) or (loc_min < ymin):
                    ymin = loc_min
                if (ymax is None) or (loc_max > ymax):
                    ymax = loc_max
    print("Y Minimum: " + str(ymin))
    print("Y Maximum: " + str(ymax))
    
    return(ymin, ymax)

def specplot(name, num_plots, last_plot=False, height=200, width=800, var_label=None, interactive=False):
    global data_quants
    global time_range_adjusted

    temp_data_quant = data_quants[name]

    if 'colormap' in temp_data_quant['extras']:
        rainbow_colormap = return_bokeh_colormap(temp_data_quant['extras']['colormap'])
    else:
        rainbow_colormap = return_bokeh_colormap('spectral')
    
    yaxis_opt = temp_data_quant['yaxis_opt']
    zaxis_opt = temp_data_quant['zaxis_opt']
    line_opt = temp_data_quant['line_opt']
    
    if 'x_range' not in tplot_opt_glob:
        tplot_opt_glob['x_range'] = Range1d(np.nanmin(temp_data_quant['data'].index.tolist()), np.nanmax(temp_data_quant['data'].index.tolist()))
        if last_plot:
            lim_info['xfull'] = tplot_opt_glob['x_range']
            lim_info['xlast'] = tplot_opt_glob['x_range']
    if 'y_range' not in yaxis_opt:
        ymin = np.nanmin(temp_data_quant['spec_bins'])
        ymax = np.nanmax(temp_data_quant['spec_bins'])
        yaxis_opt['y_range'] = [ymin, ymax]
            
    all_tplot_opt = {}
    all_tplot_opt.update(tplot_opt_glob)
    all_tplot_opt['y_range'] = Range1d(yaxis_opt['y_range'][0], yaxis_opt['y_range'][1])
    if 'y_axis_type' in yaxis_opt:
        all_tplot_opt['y_axis_type'] = yaxis_opt['y_axis_type']
    #Retrieve y and z logs
    if 'z_axis_type' in zaxis_opt:
        zscale = zaxis_opt['z_axis_type']
    else:
        zscale = 'log'
    
            
    #Get Z Range
    if 'z_range' in temp_data_quant['zaxis_opt']:
        zmin = temp_data_quant['zaxis_opt']['z_range'][0]
        zmax = temp_data_quant['zaxis_opt']['z_range'][1]
    else:
        zmax = temp_data_quant['data'].max().max()
        zmin = temp_data_quant['data'].min().min()
        if zscale=='log':
            zmin_list = []
            for column in temp_data_quant['data'].columns:
                series = temp_data_quant['data'][column]
                zmin_list.append(series.iloc[series.nonzero()[0]].min())
            zmin = min(zmin_list)
    
    
    new_plot=Figure(x_axis_type='datetime', plot_height = height, plot_width = width, **all_tplot_opt)
    new_plot.lod_factor = 100
    new_plot.lod_interval = 30
    new_plot.lod_threshold = 100
    new_plot.yaxis.axis_label_text_font_size = "10pt"
    if not time_range_adjusted:
        new_plot.x_range.start = new_plot.x_range.start * 1000
        new_plot.x_range.end = new_plot.x_range.end * 1000
        time_range_adjusted = True
    
    #APPARENTLY NEEDED
    if num_plots > 1 and last_plot==True:
        new_plot.plot_height += 22
    #if num_plots > 1:
    #    p.toolbar_location = None
    
    #GET CORRECT X DATA
    x = temp_data_quant['data'].index.tolist()
    x[:] = [a*1000 for a in x]
    temp = [a for a in x if (a <= tplot_opt_glob['x_range'].end and a >= tplot_opt_glob['x_range'].start)]
    x= temp

    #Sometimes X will be huge, we'll need to cut down so that each x will stay about 1 pixel in size
    step_size=1
    num_rect_displayed = len(x)
    if (width*2) < num_rect_displayed:
        step_size=int(math.floor(num_rect_displayed/(width*2)))
        x[:] = x[0::step_size]

    #Get length of arrays
    size_x = len(x)
    size_y = len(temp_data_quant['spec_bins'])
    
    #These arrays will be populated with data for the rectangle glyphs
    color = []
    bottom = []
    top = []
    left=[]
    right=[]
    value=[]
    corrected_time=[]
    for i in range(size_y-1):
        for j in range(size_x-1):
            temp = temp_data_quant['data'][temp_data_quant['spec_bins'][i]].iloc[j*step_size]
            value.append(temp)
            if np.isfinite(temp):
                color.append(get_heatmap_color(color_map=rainbow_colormap, min=zmin, max=zmax, value=temp, zscale=zscale))
            else:
                color.append("#%02x%02x%02x" % (255, 255, 255))
            bottom.append(temp_data_quant['spec_bins'][i])
            left.append(x[j])
            right.append(x[j+1])
            top.append(temp_data_quant['spec_bins'][i+1])
            corrected_time.append(int_to_str(x[j]/1000))
             
    #Here is where we add all of the rectangles to the plot
    cds = ColumnDataSource(data=dict(x=left,y=bottom,z=color,value=value, corrected_time=corrected_time))
    new_plot.quad(bottom = 'y', left='x', right=right, top=top, color='z', source=cds)
        
    if interactive:
        if 'y_axis_type' in yaxis_opt:
            y_interactive_log = 'log'
        else:
            y_interactive_log = 'linear'
        interactive_plot = Figure(plot_height = height, plot_width = width, y_range = (zmin, zmax), y_axis_type=y_interactive_log)
        interactive_plot.min_border_left = 100
        spec_bins = temp_data_quant['spec_bins']
        flux = [0]*len(spec_bins)
        interactive_line_source = ColumnDataSource(data=dict(x=spec_bins, y=flux))
        interactive_line = Line(x='x', y='y')
        interactive_plot.add_glyph(interactive_line_source, interactive_line)
        callback = CustomJS(args=dict(cds=cds, interactive_line_source=interactive_line_source), code="""
                var geometry = cb_data['geometry'];
                var x_data = geometry.x; // current mouse x position in plot coordinates
                var y_data = geometry.y; // current mouse y position in plot coordinates
                var d2 = interactive_line_source.get('data');
                var asdf = cds.get('data');
                var j = 0;
                x=d2['x']
                y=d2['y']
                time=asdf['x']
                energies=asdf['y']
                flux=asdf['value']
                for (i = 0; i < time.length-1; i++) {
                    if(x_data >= time[i] && x_data <= time[i+1] ) {
                        x[j] = energies[i]
                        y[j] = flux[i]
                        j=j+1
                    }
                }
                j=0
                interactive_line_source.trigger('change');
            """)
    else:
        interactive_plot = None
        callback=None
    
    #Formatting stuff
    new_plot.grid.grid_line_color = None
    new_plot.axis.major_tick_line_color = None
    new_plot.axis.major_label_standoff = 0
    new_plot.xaxis.formatter = dttf
    new_plot.title = None
    #Check for time bars
    if temp_data_quant['time_bar']:
        time_bars = temp_data_quant['time_bar']
        for time_bar in time_bars:
            time_bar_line = Span(location = time_bar['location'], dimension = time_bar['dimension'], line_color = time_bar['line_color'], line_width = time_bar['line_width'])
            new_plot.renderers.extend([time_bar_line])
            
    new_plot.renderers.extend(extra_renderers)
    new_plot.toolbar.active_drag='auto'
    
    #Add axes
    xaxis1 = DatetimeAxis(major_label_text_font_size = '0pt', **xaxis_opt_glob)
    new_plot.add_layout(xaxis1, 'above')
    if num_plots > 1 and not last_plot:
        new_plot.xaxis.major_label_text_font_size = '0pt'
    
    #Add the color bar
    if 'z_axis_type' in zaxis_opt:
        if zaxis_opt['z_axis_type'] == 'log':
            color_mapper=LogColorMapper(palette=rainbow_colormap, low=zmin, high=zmax)
            color_bar=ColorBar(color_mapper=color_mapper, ticker=LogTicker(), border_line_color=None, location=(0,0))
        else:
            color_mapper=LinearColorMapper(palette=rainbow_colormap, low=zmin, high=zmax)
            color_bar=ColorBar(color_mapper=color_mapper, ticker=BasicTicker(), border_line_color=None, location=(0,0))
    else:
        color_mapper=LogColorMapper(palette=rainbow_colormap, low=zmin, high=zmax)
        color_bar=ColorBar(color_mapper=color_mapper, ticker=LogTicker(), border_line_color=None, location=(0,0))
    color_bar.width=10
    color_bar.formatter = NumeralTickFormatter(format="0,0")
    color_bar.major_label_text_align = 'left'
    color_bar.label_standoff = 5
    color_bar.major_label_text_baseline = 'middle'
    #color_bar.title='hello'
    #color_bar.title_text_align = 'left'
    
    
    #Set y/z labels
    new_plot.yaxis.axis_label = yaxis_opt['axis_label']
    if 'axis_label' in zaxis_opt:
        color_bar.title = zaxis_opt['axis_label']
        color_bar.title_text_font_size = '8pt'
        color_bar.title_text_font_style = 'bold'
        color_bar.title_standoff = 20
    
    new_plot.add_layout(color_bar, 'right')
    
    #Create a custom hover tool
    hover = HoverTool(callback=callback)
    hover.tooltips = [("Time","@corrected_time"), ("Energy", "@y"), ("Value","@value")]
    new_plot.add_tools(hover)
    new_plot.add_tools(BoxZoomTool(dimensions=['width']))
    return new_plot, interactive_plot

def return_bokeh_colormap(name):
    import matplotlib as mpl
    from matplotlib import cm
    cm = mpl.cm.get_cmap(name)
    colormap = [rgb_to_hex(tuple((np.array(cm(x))*255).astype(np.int))) for x in range(0,cm.N)]
    return colormap

def rgb_to_hex(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    return '#%02x%02x%02x' % (red, green, blue)

def get_heatmap_color(color_map, min, max, value, zscale = 'log'):
    if value > max:
        value = max
    if value < min:
        return ("#%02x%02x%02x" % (255, 255, 255))
    if zscale=='log':
        log_min=np.log10(min)
        log_max=np.log10(max)
        log_val=np.log10(value)
        if np.isfinite(np.log10(value)):
            cm_index = int((((log_val-log_min) / (log_max-log_min)) * (len(color_map)-1)))
            return color_map[cm_index]
        else:
            return ("#%02x%02x%02x" % (255, 255, 255))
    else:
        cm_index = int((((value-min) / (max-min)) * len(color_map)))
        return color_map[cm_index]

def py_timebar_delete(t, varname = None, dim = 'height'):
    print(dim)
    if varname is None:
        for name in data_quants:
            list_timebars = data_quants[name]['time_bar']
            elem_to_delete = []
            for elem in list_timebars:
                if (elem.location is t) and (elem.dimension is dim):
                    elem_to_delete.append(elem)
            for i in elem_to_delete:
                list_timebars.remove(i)
            data_quants[name]['time_bar'] = list_timebars
    else:
        if not isinstance(varname, list):
            varname = [varname]
        for i in varname:
            if i not in data_quants.keys():
                print(str(i) + " is currently not in pytplot.")
                return
            list_timebars = data_quants[i]['time_bar']
            elem_to_delete = []
            for elem in list_timebars:
                if (elem.location is t) and (elem.dimension is dim):
                    elem_to_delete.append(elem)
            for j in elem_to_delete:
                list_timebars.remove(j)
            data_quants[i]['time_bar'] = list_timebars 
    
    return

def timebar_delete(t, varname=None, dim='height'):
    if varname is None:
        for name in data_quants:
            list_timebars = data_quants[name]['time_bar']
            elem_to_delete = []
            for elem in list_timebars:
                for num in t:
                    if (elem.location == num) and (elem.dimension == dim):
                        elem_to_delete.append(elem)
            for i in elem_to_delete:
                list_timebars.remove(i)
            data_quants[name]['time_bar'] = list_timebars
    else:
        if not isinstance(varname, list):
            varname = [varname]
        for i in varname:
            if i not in data_quants.keys():
                print(str(i) + " is currently not in pytplot.")
                return
            list_timebars = data_quants[i]['time_bar']
            elem_to_delete = []
            for elem in list_timebars:
                for num in t:
                    if (elem.location == num) and (elem.dimension == dim):
                        elem_to_delete.append(elem)
            for j in elem_to_delete:
                list_timebars.remove(j)
            data_quants[i]['time_bar'] = list_timebars
    return    
    
def py_timebar(t, varname = None, databar = False, delete = False, color = 'black', thick = 1, dash = False):
    global data_quants
    global extra_renderers
    
    if not isinstance(t, (int, float, complex)):
        t = str_to_int(t)
    
    dim = 'height'
    if databar is True:
        dim = 'width'
    
    dash_pattern = 'solid'
    if dash is True:
        dash_pattern = 'dashed'
        
    # Convert single value to a list so we don't have to write code to deal with
    # both single values and lists.
    if not isinstance(t, list):
        t = [t]
    # Convert values to seconds by multiplying by 1000
    if databar is False:
        num_bars = len(t)
        for j in range(num_bars):
            t[j] *= 1000
            
    if delete is True:
        timebar_delete(t, varname, dim)
        return
    # If no varname specified, add timebars to every plot
    if varname is None:
        num_bars = len(t)
        for i in range(num_bars):
            tbar = {}
            tbar['location'] = t[i]
            tbar['dimension'] = dim
            tbar['line_color'] = color
            tbar['line_width'] = thick
            tbar['line_dash'] = dash_pattern
            for name in data_quants:
                temp_data_quants = data_quants[name]
                temp_data_quants['time_bar'].append(tbar)
    else:
        if not isinstance(varname, list):
            varname = [varname]
        for j in varname:
            if j not in data_quants.keys():
                print(str(j) + "is currently not in pytplot")
            else:
                num_bars = len(t)
                for i in range(num_bars):
                    tbar = Span(location = t[i], dimension = dim, line_color = color, line_width = thick, line_dash = dash_pattern)
                    temp_data_quants = data_quants[j]
                    temp_data_quants['time_bar'].append(tbar)
    return

def py_timespan(t1, dt, keyword = None):
    if keyword is None or keyword is 'days':
        # days is the duration
        dt *= 86400
    elif keyword is 'hours':
        dt *= 3600
    elif keyword is 'minutes':
        dt *= 60
    elif keyword is 'seconds':
        dt *= 1
    else:
        print("Invalid 'keyword' option.\nEnum(None, 'hours', 'minutes', 'seconds', 'days')")
        
    if not isinstance(t1, (int, float, complex)):
        t1 = str_to_int(t1)
    t2 = t1+dt
    py_xlim(t1, t2)
    
    return

def timestamp_help(in_date):
    
    form_datetime = datetime.datetime.utcfromtimestamp(in_date)
    form_string = form_datetime.strftime("%m/%d/%Y")
    
    return form_string

def py_timestamp(val):
    global extra_layouts
    
    if val is 'on':
        todaystring = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        extra_layouts['time_stamp'] = todaystring
    else:
        if 'time_stamp' in extra_layouts:
            del extra_layouts['time_stamp']
    
    return
