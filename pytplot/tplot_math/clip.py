# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import numpy as np
import copy
import logging

def clip(tvar,ymin,ymax,newname=None,new_tvar=None):
    """
    Change out-of-bounds data to NaN.

    Parameters:
        tvar1 : str
            Name of tvar to use for data clipping.
        ymin : int/float
            Minimum value to keep (inclusive)
        ymax : int/float
            Maximum value to keep (inclusive)
        new_tvar : str (Deprecated)
            Name of new tvar for clipped data storage.  If not specified, tvar will be replaced
            THIS is not an option for multiple variable input, for multiple or pseudo variables, the data is overwritten. 
        newname : str
            Name of new tvar for clipped data storage.  If not specified, tvar will be replaced
            THIS is not an option for multiple variable input, for multiple or pseudo variables, the data is overwritten.

    Returns:
        None

    Examples:
        >>> Make any values below 2 and above 6 equal to NaN.
        >>> pytplot.store_data('d', data={'x':[2,5,8,11,14,17,21], 'y':[[1,1],[2,2],[100,100],[4,4],[5,5],[6,6],[7,7]]})
        >>> pytplot.clip('d',2,6,'e')
    """

    # new_tvar is deprecated in favor of newname
    if new_tvar is not None:
        logging.info("clip: The new_tvar parameter is deprecated. Please use newname instead.")
        newname = new_tvar

    #check for globbed or array input, and call recursively
    tn = pytplot.tnames(tvar)
    if len(tn) > 1:
        for j in range(len(tn)):
            pytplot.clip(tn[j],ymin,ymax)
        return


    a = copy.deepcopy(pytplot.data_quants[tvar].where(pytplot.data_quants[tvar] >= ymin))
    a = copy.deepcopy(a.where(a <= ymax))

    if newname is None:
        a.name = tvar
        pytplot.data_quants[tvar] = a
    else:
        if 'spec_bins' in a.coords:
            pytplot.store_data(newname, data={'x': a.coords['time'], 'y': a.values, 'v': a.coords['spec_bins']})
            pytplot.data_quants[newname].attrs = copy.deepcopy(pytplot.data_quants[tvar].attrs)
        else:
            pytplot.store_data(newname, data={'x': a.coords['time'], 'y': a.values})
            pytplot.data_quants[newname].attrs = copy.deepcopy(pytplot.data_quants[tvar].attrs)

    return
