import pytplot
#import pydivide

#insitu = pydivide.download_files(start_date='2017-06-19', end_date='2017-06-20')
#insitu = pydivide.read(['2017-06-19','2017-06-20'])
#t = insitu['Time']
#data = insitu['MAG']['MSO_Y']
#pytplot.store_data('sgx',data={'x': t, 'y': data.values})

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

pytplot.store_data('power',data={'x': t_tot, 'y': d_tot})

pytplot.tplot_math.pwr_spec('power', nbp=512)
pytplot.zlim('power_pwrspec', .01 / 30, 100 / 30)
#pytplot.zlim('power_pwrspec', .01, 100)
pytplot.options('power_pwrspec', 'ylog', 1)
pytplot.options('power_pwrspec', 'zlog', 1)
pytplot.options('power_pwrspec', 'xlog_interactive', 'log')
pytplot.options('power_pwrspec', 'ylog_interactive', 'log')
pytplot.tplot_options('roi', ['2014-12-27 07:05:00', '2014-12-27 07:16:00'])
pytplot.options('power_pwrspec', 'static_tavg', ['2014-12-27 07:05:00', '2014-12-27 07:16:00'])
pytplot.options('power_pwrspec', 'static', '2014-12-27 07:10:00')
pytplot.tplot(['power', 'power_pwrspec'], interactive=True)

