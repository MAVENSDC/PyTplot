import pytplot

def test_pyspedas():

    from pyspedas.mms import mms_load_fpi

    probe = '1'
    trange = ['2015-12-01/12:05:00', '2015-12-01/12:07:00']

    mms_load_fpi(probe=probe, datatype=['des-moms', 'dis-moms'], trange=trange)  # center_measurements?

    DenIN = 'mms' + probe + '_dis_numberdensity_fast'

    SpecIN = 'mms' + probe + '_dis_energyspectr_omni_fast'

    pytplot.tplot([SpecIN, DenIN], testing=True)
    pytplot.tplot([SpecIN, DenIN], testing=True, bokeh=True, save_file='testing.png')