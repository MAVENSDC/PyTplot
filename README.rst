Pytplot
--------


SAMPLE COMMANDS:

Obtain sample data:
pytplot.tplot_restore('test_data.tplot')

Plot some data:
pytplot.py_tplot('swia_vel', var_label='orbit')

Change panel size:
pytplot.py_options(['mag','swia_den','swia_vel'] , 'panel_size', .5)

Change axis:
pytplot.py_options('swia_den', 'ylog', 1)

Change timespan:
pytplot.py_timespan('2016-06-20 00:00:00', .1875, keyword='days')

Plot all of the data:
pytplot.py_tplot(['SEP_2_ELEC','SEP_1_ION', 'SEP_2_ION', 'swia_counts','swia_den','mag','swia_vel'])