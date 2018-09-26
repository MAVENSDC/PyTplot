from pyqtgraph.Qt import QtCore,QtGui
import pytplot
import numpy as np
import pyqtgraph as pg

#Load data
vars = []
tplot_keys = pytplot.data_quants.keys()
for key in tplot_keys:
    if pytplot.data_quants[key].spec_bins is not None:
        vars.append(key)


for var in vars:

    energy_bins = list()
    for name, values in pytplot.data_quants[var].spec_bins.iteritems():
        # name = energy
        # value = value of energy
        energy_bins.append(values.values[0])

    flux_values = list()
    time_values = list()
    for r, rows in pytplot.data_quants[var].data.iterrows():
        # r = energy bin #
        # rows = the flux at each time, where each row signifies a different time
        flux_values.append(rows.values)
        time_values.append(r)

    a_dict = {}
    for i in range(len(time_values)):
        a_dict[time_values[i]] = [energy_bins, flux_values]

    # app = QtGui.QApplication([])

    win = pg.GraphicsWindow(title="Some title")
    win.resize(1000,600)
    win.setWindowTitle('Interactive Window')

    # Enable antialiasing for prettier plots
    # pg.setConfigOptions(antialias=True)

    p1 = win.addPlot(title="Energy Flux vs. Energy")
    p1.setLabel('bottom','Energy')
    p1.setLabel('left','Energy Flux')
    plot = p1.plot([],[])

    def find_nearest_time(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    #Define the update function
    def update(t):
        time_array = np.array(time_values)
        time = find_nearest_time(time_array, t)
        idx = time_values.index(time)
        plot.setData(energy_bins[:], flux_values[idx])

    # Make the above function called whenever hover_time is updated
    pytplot.hover_time.register_listener(update)

    # Start Qt event loop unless running in interactive mode.
    if __name__ == '__main__':
        import sys
        if not (hasattr(sys, 'ps1')) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()