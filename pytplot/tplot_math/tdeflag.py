"""
Removes NaNs and other flags.

Notes
----
Allowed wildcards are ? for a single character, * from multiple characters.
Similar to tdeflag.pro in IDL SPEDAS, but now a wrapper for deflag.py

"""
import logging
import pytplot

def tdeflag(names, flag=None, method='linear', newname=None, new_names=None, suffix=None,
            overwrite=None, fillval=None):
    """
    Replaces FLAGs in arrays with interpolated or other values.

    Parameters
    ----------
    names: str/list of str
        List of pytplot names.
    method: str, optional
        Method to apply. Default is 'linear'
        If None,then flagged values are replaced with NaN
        Other options 'repeat' (repeat last good value), 
        'linear' (interpolate linearly over gap).
        'replace' replaces flagged value with a fill value, which can be set using the 
                  keyword 'fillval' (default is to use NaN)
        Option 'remove_nan' removes time intervals with NaN values
    new_names: str/list of str, optional (Deprecated)
        List of new_names for pytplot variables.
        If '', then pytplot variables are replaced.
        If not given, then a suffix is applied.
    newname: str/list of str, optional
        List of new names for pytplot variables.
        If '', then pytplot variables are replaced.
        If not given, then a suffix is applied.
    suffix: str, optional
        A suffix to apply. Default is '-deflag'.
    overwrite: bool, optional
        Replace the existing tplot name.

    Returns
    -------
    None.

    """
    # new_names is deprecated in favor of newname
    if new_names is not None:
        logging.info("tdeflag: The new_names parameter is deprecated. Please use newname instead.")
        newname = new_names

    old_names = pytplot.tnames(names)

    if len(old_names) < 1:
        logging.error('tdeflag error: No pytplot names were provided.')
        return

    if suffix is None:
        suffix = '-deflag'

    if overwrite is not None:
        n_names = old_names
    elif newname is None:
        n_names = [s + suffix for s in old_names]
    else:
        n_names = newname

    if isinstance(n_names, str):
        n_names = [n_names]

    if len(n_names) != len(old_names):
        n_names = [s + suffix for s in old_names]
        logging.info('input newname has incorrect number of elements')

    for i in range(len(old_names)):
        pytplot.deflag(old_names[i], flag, new_tvar=n_names[i], method=method, fillval=fillval)
        logging.info('tdeflag was applied to: ' + n_names[i])
