
import pytplot as pt
import os

from pyspedas.mms import mms_load_fgm, mms_load_mec, mms_load_edp, mms_load_dsp, mms_load_fpi, mms_load_hpca, mms_load_feeps

from pyspedas import time_string, time_double, tnames
import numpy as np

probe = '1'
trange = ['2015-12-01/12:05:00', '2015-12-01/12:07:00']

mms_load_fpi(probe=probe, datatype=['des-moms', 'dis-moms'], trange=trange)  # center_measurements?
#mms_load_fgm(trange=trange)
tnames = pt.tplot_names()


DenIN = 'mms'+probe+'_dis_numberdensity_fast'
DenEN = 'mms'+probe+'_des_numberdensity_fast'
VIgseN = 'mms'+probe+'_dis_bulkv_gse_brst'
VEgseN = 'mms'+probe+'_des_bulkv_gse_brst'
SpecIN = 'mms'+probe+'_dis_energyspectr_omni_fast'
SpecEN = 'mms'+probe+'_des_energyspectr_omni_fast'
PADE_lowN = 'mms'+probe+'_des_pitchangdist_lowen_brst'
PADE_midN = 'mms'+probe+'_des_pitchangdist_miden_brst'
PADE_highN = 'mms'+probe+'_des_pitchangdist_highen_brst'
TIperpN = 'mms'+probe+'_dis_tempperp_brst'
TIparaN = 'mms'+probe+'_dis_temppara_brst'
TEperpN = 'mms'+probe+'_des_tempperp_brst'
TEparaN = 'mms'+probe+'_des_temppara_brst'

pt.tplot([SpecIN, SpecEN, DenIN], bokeh=True)

#files = []
#for f in os.listdir(r"C:\Code Repos\PyTplot\pydata\mms2\fpi\brst\l2\des-moms\2017\07\26"):
#    files.append(os.path.join(r"C:\Code Repos\PyTplot\pydata\mms2\fpi\brst\l2\des-moms\2017\07\26",f))
#pt.cdf_to_tplot(files[0], varformat='mms2_des_energyspectr_omni_brst')
#pt.tplot(['mms2_des_energyspectr_omni_brst'])