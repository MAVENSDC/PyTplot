"""
Removes NaNs and other flags.

Notes
----
Allowed wildcards are ? for a single character, * from multiple characters.
Similar to tdeflag.pro in IDL SPEDAS, but now a wrapper for deflag.py

"""
import logging
import pytplot

def tdeflag(names,
            flag=None,
            method='remove_nan',
            newname=None,
            new_names=None,
            suffix=None,
            overwrite=None,
            fillval=None
):
    """
    Replaces FLAGs in arrays with interpolated or other values.

    Parameters
    ----------
    names: str/list of str
        List of pytplot names.
    flag: float, int, or list
        Value or values to be treated as flags
    method: str, optional
        Method to apply.
        If None,then flagged values are replaced with NaN
        Other options 'repeat' (repeat last good value), 
        'linear' (interpolate linearly over gap).
        'replace' replaces flagged value with a fill value, which can be set using the 
                  keyword 'fillval' (default is to use NaN)
        Option 'remove_nan' removes time intervals with NaN values
        Default: 'remove_nan'
    newname: str/list of str, optional
        List of new names for pytplot variables.
        If '', then pytplot variables are replaced.
        Default: None. If not specified then a suffix is applied.
    new_names: str/list of str, optional (Deprecated)
        List of new names for pytplot variables.
        If '', then pytplot variables are replaced.
        Default: None.
    suffix: str, optional
        A suffix to apply.
        Default: '-deflag'.
    overwrite: bool, optional
        Replace the existing tplot name.
        Default: None
    fillval: int, float (optional)
        Value to use as replacement if method='replace'

    Returns
    -------
    list of str
        List of pytplot variables created or altered by tdeflag

    Examples
    --------

    >>> pytplot.store_data('d', data={'x':[2,5,8,11,14,17,21], 'y':[[1,1],[2,2],[100,4],[4,90],[5,5],[6,6],[7,7]]})
    >>> # Remove any instances of [100,90,7,2,57] from 'd', store in 'e'.
    >>> pytplot.deflag('d',[100,90,7,2,57],newname='e')
    >>> d_deflagged = pytplot.get_data('e')
    >>> print(d_deflagged)
    """
    # new_names is deprecated in favor of newname
    if new_names is not None:
        logging.info("tdeflag: The new_names parameter is deprecated. Please use newname instead.")
        newname = new_names

    old_names = pytplot.tnames(names)

    if len(old_names) < 1:
        logging.error('tdeflag error: No pytplot names were provided.')
        return None

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
        pytplot.deflag(old_names[i], flag, newname=n_names[i], method=method, fillval=fillval)
        logging.info('tdeflag was applied to: ' + n_names[i])

    return n_names
