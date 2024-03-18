
from .subtract_average import subtract_average


def subtract_median(
        names,
        new_names=None,
        suffix=None,
        overwrite=None
):
    """
    Subtracts the median from data.

    Parameters
    ----------
    names: str/list of str
        List of pytplot names.
    new_names: str/list of str, optional
        List of new_names for pytplot variables.
        Default: None. If not given, then a suffix is applied.
    suffix: str, optional
        A suffix to apply.
        Default: '-d'.
    overwrite: bool, optional
        If set, then pytplot variables are replaced.
        Default: None

    Returns
    -------
    None.

    """
    subtract_average(names, new_names=new_names, suffix=suffix, overwrite=overwrite,
                     median=1)
