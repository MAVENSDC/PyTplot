'''
Read in a given variable name and option name.
Modifies options for lines of the plot.

Input:
    var_name: Tplot variable name (string)
    plot_option: Option name (string)
    val: Value to change option to.
         Type is different for each option.

Output: None
'''
from bokeh.models import Range1d
from bokeh.models.glyphs import Line

def option_usage():
    print("options 'tplot variable name' 'plot option' value[s]")
    return

def options(option, value, old_yaxis_opt, old_zaxis_opt, old_line_opt, old_extras):
    new_yaxis_opt = old_yaxis_opt
    new_zaxis_opt = old_zaxis_opt
    new_line_opt = old_line_opt
    new_extras = old_extras
    
    #if(option == 'axis_style'):
    
    if option == 'color':
        if isinstance(value, list):
            new_extras['line_color'] = value
        else:
            new_extras['line_color'] = [value]
    
    if option == 'colormap':
        new_extras['colormap'] = value
    
    if option == 'spec':
        new_extras['spec'] = value
    #elif option is 'colors':
    
    # don't know what the values are meant to mean
    # elif(option == 'ygridstyle'):
    
    elif option == 'ylog':
        if value == 1:
            new_yaxis_opt['y_axis_type'] = 'log'
        if value == 0:
            new_yaxis_opt['y_axis_type'] = 'linear'
    
    elif option == 'legend_names':
        new_yaxis_opt['legend_names'] = value
    
    elif option == 'zlog':
        if value == 1:
            new_zaxis_opt['z_axis_type'] = 'log'
        if value == 0:
            new_zaxis_opt['z_axis_type'] = 'linear'
    
    # elif(option == 'ymajor'):  
    
    elif option == 'nodata':
        new_line_opt['visible'] = value
    
    elif option == 'line_style':
        to_be = []
        if value == 0 or value == 'solid_line':
            to_be = []
        elif value == 1 or value == 'dot':
            to_be = [2, 4]
        elif value == 2 or value == 'dash':
            to_be = [6]
        elif value == 3 or value == 'dash_dot':
            to_be = [6, 4, 2, 4]
        elif value == 4 or value == 'dash_dot_dot_dot':
            to_be = [6, 4, 2, 4, 2, 4, 2, 4]
        elif value == 5 or value == 'long_dash':
            to_be = [10]
            
        new_line_opt['line_dash'] = to_be
        
        if(value == 6 or value == 'none'):
            new_line_opt['visible'] = False
            
    elif option == 'name':
        new_line_opt['name'] = value
    
    elif option == "panel_size":
        if value > 1 or value <= 0:
            print("Invalid value. Should be (0, 1]")
            return
        new_extras['panel_size'] = value
            
    elif option == 'thick':
        new_line_opt['line_width'] = value
    
    elif option == 'transparency':
        alpha_val = value/100
        new_line_opt['line_alpha'] = alpha_val
    
    elif option == ('yrange' or 'y_range'):
        new_yaxis_opt['y_range'] = [value[0], value[1]]
        
    elif option == ('zrange' or 'z_range'):
        new_zaxis_opt['z_range'] = [value[0], value[1]]
    
    elif option == 'ytitle':
        new_yaxis_opt['axis_label'] = value
    
    elif option == 'ztitle':
        new_zaxis_opt['axis_label'] = value
        
    '''       
    # value: NumberSpec(String, Dict(String, Either(String, Float)), Float)
    if(option == 'alpha'):
        line_list = fig.select(type=Line)
        line_len = len(line_list)
        i = 0
        while(i < line_len):
            line_list[i].line_alpha = value
            i += 1
    # value: Enum('butt', 'round', 'square')
    elif(option == 'cap'):
        line_list = fig.select(type=Line)
        line_len = len(line_list)
        i = 0
        while(i < line_len):
            line_list[i].line_cap = value
            i += 1
    # value: color value: string
    elif(option == 'color'):
        line_list = fig.select(type=Line)
        line_len = len(line_list)
        i = 0
        while(i < line_len):
            line_list[i].line_color = value
            i += 1
    # value: DashPattern
    elif(option == 'dash'):
        line_list = fig.select(type=Line)
        line_len = len(line_list)
        i = 0
        while(i < line_len):
            line_list[i].line_dash = value
            i += 1
    # value: Int
    elif(option == 'dash_offset'):
        line_list = fig.select(type=Line)
        line_len = len(line_list)
        i = 0
        while(i < line_len):
            line_list[i].line_dash_offset = value
            i += 1
    # value: Enum('miter', 'round', 'bevel')
    elif(option == 'join'):
        line_list = fig.select(type=Line)
        line_len = len(line_list)
        i = 0
        while(i < line_len):
            line_list[i].line_join = value
            i += 1
    # value: integer
    elif(option == 'thick'):
        line_list = fig.select(type=Line)
        line_len = len(line_list)
        i = 0
        while(i < line_len):
            line_list[i].line_width = value
            i += 1
    # value: Bool
    elif(option == 'visible'):
        line_list = fig.select(type=Line)
        line_len = len(line_list)
        i = 0
        while(i < line_len):
            line_list[i].visible = value
            i += 1
    # value: [integer, integer]
    elif(option == 'yrange'):
        fig.y_range = Range1d(value[0], value[1])
    # value: string
    elif(option == 'ytitle'):
        fig.yaxis.axis_label = value
    '''
    
    return (new_yaxis_opt, new_zaxis_opt, new_line_opt, new_extras)


def tplot_options(option, value, old_tplot_opt_glob, old_title_opt, window_size):
    new_tplot_opt_glob = old_tplot_opt_glob
    new_title_opt = old_title_opt
    
    if option == 'title':
        new_title_opt['text'] = value
    
    elif option == 'title_size':
        str_size = str(value) + 'pt'
        new_title_opt['text_font_size'] = str_size
        
    elif option == 'wsize':
        window_size = value
    
    return (new_tplot_opt_glob, new_title_opt, window_size)

        
    