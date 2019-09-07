# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

import os
import numpy as np

import pytplot


def read_kp_insitu_crustal_file(crustal_file=None, read_only=False, prefix='', suffix=''):
    """
    Read in a given insitu crustal file into a dictionary object
    Optional keywords maybe used to downselect instruments returned
     and the time windows.

    Input:
        crustal_file: str/list of str
            The file names and full paths of KP insitu crustal files to be read and parsed.
        read_only: boolean
            If True, just reads data into dict and returns the dict.
            If False, loads data into dict and loads data in the dict into tplot variables.
        prefix: str
            The tplot variable names will be given this prefix.  By default,
            no prefix is added.
        suffix: str
            The tplot variable names will be given this suffix.  By default,
            no suffix is added.
    Output:
        Either a dictionary (data structure) containing up to all of the columns included
        in an insitu crustal data file, or tplot variable names.
    """

    # List of headers present in KP insitu crustal file
    headers = ['TIME', 'MSO_X_LOC', 'MSO_Y_LOC', 'MSO_Z_LOC', 'MSO_X_B', 'MSO_Y_B', 'MSO_Z_B', 'GEO_X_LOC', 'GEO_Y_LOC',
               'GEO_Z_LOC', 'GEO_X_B', 'GEO_Y_B', 'GEO_Z_B']

    # Create a dictionary and list in which we'll store KP insitu crustal variable data and variable names, respectively
    crustal_dict = {}
    stored_variables = []

    # Code assumes a list of KP insitu crustal files
    if isinstance(crustal_file, str):
        crustal_file = [crustal_file]
    elif isinstance(crustal_file, list):
        crustal_file = crustal_file
    else:
        print("Invalid filenames input.")
        return stored_variables

    for c_file in crustal_file:
        with open(c_file, 'r') as f:
                lines = f.readlines()

        # Find the first occurrence where we don't have comments (i.e., where the data begins)
        data_start = next((i for i, x in enumerate(lines) if x[0] != '#'), None)

        # Populate the data dictionary with values!
        for l in lines[data_start:]:
            data_split = l.strip().split()  # Remove extra spaces, then split on whitespaces
            for v, var in enumerate(headers):
                if var in crustal_dict.keys():
                    crustal_dict[var].append(data_split[v])
                else:
                    crustal_dict[var] = [data_split[v]]

    # Don't create tplot vars if that's not what's desired
    if read_only:
        return crustal_dict

    for key in crustal_dict.keys():
        # Quicky check, did we get datetimes for time? If so, turn into seconds since the epoch.
        if key == 'TIME' and isinstance(crustal_dict[key][0], str):
            crustal_dict[key] = [pytplot.tplot_utilities.str_to_int(t) for t in crustal_dict[key]]
        # create variable name
        obs_specific = prefix + key + suffix
        # if all values are NaN, continue
        if all(v is None for v in crustal_dict[key]):
            continue
        # store data in tplot variable
        try:
            pytplot.store_data(obs_specific, data={'x': crustal_dict['TIME'],
                                                   'y': [np.float(val) for val in crustal_dict[key]]})
        except ValueError:
            continue
        if obs_specific not in stored_variables:
            stored_variables.append(obs_specific)

    return stored_variables
