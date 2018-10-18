import pytplot

def test_cdf_read():
    pytplot.cdf_to_tplot("/home/travis/build/MAVENSDC/PyTplot/tests/testfiles/mvn_euv_l2_bands_20170619_v09_r03.cdf")
    pytplot.cdf_to_tplot("/home/travis/build/MAVENSDC/PyTplot/tests/testfiles/mvn_swe_l2_svyspec_20170619_v04_r02.cdf")