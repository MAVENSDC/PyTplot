import pytplot

pytplot.store_data("variable1", data={'x':[100000,200000,300000,400000,500000], 'y':[1,2,3,4,5]})
#pytplot.tplot(0)

pytplot.options('variable1', 'ylog', 1)
pytplot.options('variable1' , 'legend_names', ['Variability'])
pytplot.options('variable1' , 'color', 'r')
pytplot.tplot_options('title', "My Line")
#pytplot.tplot(0)

pytplot.tplot_restore('C:/tplot_files/asdf.tplot.tplot')
pytplot.tplot_names()

pytplot.options('SEP_2_ION', 'ylog', 1)
pytplot.options('SEP_1_ION', 'ylog', 1)
pytplot.options('swia_counts', 'ylog', 1)
pytplot.options('SEP_2_ION', 'zlog', 1)
pytplot.options('SEP_1_ION', 'zlog', 1)
pytplot.options('swia_counts', 'zlog', 1)
pytplot.tplot([4,3,2,6], bokeh=True)

pytplot.tplot(['swia_counts'], bokeh=True, interactive=True)

import pydivide
insitu = pydivide.read('2016-06-20')
t = insitu['Time']
alt = insitu['SPACECRAFT']['ALTITUDE']
lat = insitu['SPACECRAFT']['SUB_SC_LATITUDE']
lon = insitu['SPACECRAFT']['SUB_SC_LONGITUDE']
pytplot.store_data('sc_lat', data={'x':t, 'y':lat})
pytplot.store_data('sc_lon', data={'x':t, 'y':lon})
pytplot.store_data('sc_alt', data={'x':t, 'y':alt})


pytplot.link('swia_vel', 'sc_alt', link_type='alt')
pytplot.options('swia_vel', 'alt', 1)
pytplot.tplot('swia_vel', bokeh=True)


pytplot.link('swia_vel', 'sc_lat', link_type='lat')
pytplot.link('swia_vel', 'sc_lon', link_type='lon')
pytplot.options('swia_vel', 'alt', 0)
pytplot.options('swia_vel', 'map', 1)
pytplot.options('swia_vel', 'basemap', 'C:/Code Repos/pythontoolkit/pydivide/basemaps/MarsElevation_2500x1250.jpg')
pytplot.tplot('swia_vel', bokeh=True)


pytplot.tplot(['swia_vel', 'swia_counts'])

pytplot.timebar('2016-06-20 01:15:32', thick=10, color='g')
pytplot.tplot(['swia_vel', 'swia_counts'], bokeh=True)

pytplot.tplot(['swia_counts'], var_label='sc_lat')

pytplot.tplot('swia_den', bokeh=True)

#pytplot.tplot_save(['swia_counts', 'swia_den', 'swia_vel'], "C:/temp/tplot_save.pytplot")

import pyqtgraph.opengl as gl
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

x = insitu['SPACECRAFT']['MSO_X']
y = insitu['SPACECRAFT']['MSO_Y']
z = insitu['SPACECRAFT']['MSO_Z']
pytplot.store_data('MSO_X', data={'x':t, 'y':x})
pytplot.store_data('MSO_Y', data={'x':t, 'y':y})
pytplot.store_data('MSO_Z', data={'x':t, 'y':z})


#Define the update function
def update(t, name):
    maven.translate(-update.pos[0], -update.pos[1], -update.pos[2])
    i = pytplot.data_quants['MSO_X'].data.index.values.searchsorted(t)
    update.pos = [pytplot.data_quants['MSO_X'].data.values[i-1],
                  pytplot.data_quants['MSO_Y'].data.values[i-1],
                  pytplot.data_quants['MSO_Z'].data.values[i-1]]
    maven.translate(update.pos[0], update.pos[1], update.pos[2])
update.pos = [0,0,0]

#Make the above function called whenever hover_time is updated
pytplot.hover_time.register_listener(update)
pytplot.tplot(['swia_counts'])