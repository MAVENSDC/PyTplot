from hapiclient.hapi import hapi

server     = 'http://hapi-server.org/servers/TestData/hapi'
dataset    = 'dataset1'
parameters = 'scalar,vector'
start      = '2010-01-01T00:00:00'
stop       = '2010-01-01T00:00:10'
opts       = {'use_cache': True}

data,meta = hapi(server,dataset,parameters,start,stop,**opts)


from hapiclient.hapi import hapitime2datetime

import pytplot
import datetime
from datetime import timezone

dateTimes = hapitime2datetime(data['Time'])
from datetime import timezone


pytplot.store_data("variable1", data={'x':dateTimes,'y': data['scalar']})
pytplot.tplot(0)
