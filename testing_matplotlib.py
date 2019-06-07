
#Requires pip install pyopengl

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pytplot
import pydivide

#Read in the data
#pydivide.download_files(start_date='2014-12-27', end_date='2014-12-28')
insitu = pydivide.read('2014-12-27')

#Set up the silly little widget
app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('pyqtgraph example: GL Shaders')
w.setCameraPosition(distance=5000, azimuth=-90)
md = gl.MeshData.sphere(rows=10, cols=20)
mars = gl.GLMeshItem(meshdata=md, smooth=True, color=(1, 0, 0, 1), glOptions='additive')
mars.translate(0, 0, 0)
mars.scale(3390, 3390, 3390)
w.addItem(mars)
maven = gl.GLMeshItem(meshdata=md, smooth=True, color=(1, 1, 0, 1), glOptions='additive')
maven.translate(0, 0, 0)
maven.scale(300, 300, 300)
w.addItem(maven)

#Define the update function
def update(t, name):
    maven.translate(-update.pos[0], -update.pos[1], -update.pos[2])
    i = insitu['Time'].searchsorted(t)
    update.pos = [insitu['SPACECRAFT']['MSO_X'][i-1], insitu['SPACECRAFT']['MSO_Y'][i-1], insitu['SPACECRAFT']['MSO_Z'][i-1]]
    maven.translate(update.pos[0], update.pos[1], update.pos[2])
update.pos = [0,0,0]

#Make the above function called whenever hover_time is updated
pytplot.hover_time.register_listener(update)

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if not (hasattr(sys, 'ps1')) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()


t_tot = []
d_tot=[]
with open("C:/temp/asdf.txt") as f:
    num=0
    for line in f:
        time, data = line.split()
        if num > 675000 and num < 750000:
            t_tot.append(float(time))
            d_tot.append(float(data))
        num+=1


import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(nrows=2)
ax1.plot(t_tot, d_tot)
Pxx, freqs, bins, im = ax2.specgram(d_tot, NFFT=256, Fs=30, detrend='linear')

ax2.set_yscale("log")
ax2.set_ylim(.1,10)

def onclick(event):
    pytplot.hover_time.change_hover_time(event.xdata)

fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()






