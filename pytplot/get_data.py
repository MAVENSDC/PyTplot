from . import tplot_common

def get_data(name):
    global data_quants
    if name not in tplot_common.data_quants.keys():
        print("That name is currently not in pytplot")
        return
    
    temp_data_quant = tplot_common.data_quants[name]
    data_temp = temp_data_quant.data.values
    data_val = [i for [i] in data_temp]
    
    time_val = temp_data_quant.data.index.tolist()
    
    return(time_val, data_val)