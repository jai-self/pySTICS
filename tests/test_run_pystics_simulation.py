from pystics.params import parametrization_from_stics_example_files
from pystics.simulation import run_pystics_simulation
import numpy as np
import pandas as pd
import os

def test_run_wheat():

    species = 'common_wheat'
    variety = 'Talent'

    mocked_dir = os.path.dirname(os.path.abspath(__file__)) + "/mocked_data"
    
    weather_pystics, crop, manage, soil, station, constants, initial = parametrization_from_stics_example_files(species=species, variety=variety, xml_folder_path = mocked_dir + '/mocked_param_files')
    pystics_wheat_test, _ = run_pystics_simulation(weather_pystics, crop, soil, constants, manage, station, initial)

    pystics_wheat_mocked = pd.read_pickle(mocked_dir + '/pystics_wheat_results.pkl')

    assert np.allclose(pystics_wheat_test.mafruit.values, pystics_wheat_mocked.mafruit.values, atol=1e-3)
    assert  np.allclose(pystics_wheat_test.resrac.values, pystics_wheat_mocked.resrac.values, atol=1e-3)
    assert np.allclose(pystics_wheat_test.swfac.values, pystics_wheat_mocked.swfac.values, atol=1e-3)
    assert np.allclose(pystics_wheat_test.dltams.values, pystics_wheat_mocked.dltams.values, atol=1e-3)
    assert np.allclose(pystics_wheat_test.ftemp.values, pystics_wheat_mocked.ftemp.values, atol=1e-3)
    assert np.allclose(pystics_wheat_test.udevcult.values, pystics_wheat_mocked.udevcult.values, atol=1e-3)

def test_run_barley():

    species = 'barley'
    variety = 'cork'

    mocked_dir = os.path.dirname(os.path.abspath(__file__)) + "/mocked_data"
    
    weather_pystics, crop, manage, soil, station, constants, initial = parametrization_from_stics_example_files(species=species, variety=variety, xml_folder_path = mocked_dir + '/mocked_param_files')
    pystics_barley_test, _ = run_pystics_simulation(weather_pystics, crop, soil, constants, manage, station, initial)

    pystics_barley_mocked = pd.read_pickle(mocked_dir + '/pystics_barley_results.pkl')

    assert np.allclose(pystics_barley_test.mafruit.values, pystics_barley_mocked.mafruit.values, atol=1e-3)
    assert  np.allclose(pystics_barley_test.resrac.values, pystics_barley_mocked.resrac.values, atol=1e-3)
    assert np.allclose(pystics_barley_test.swfac.values, pystics_barley_mocked.swfac.values, atol=1e-3)
    assert np.allclose(pystics_barley_test.dltams.values, pystics_barley_mocked.dltams.values, atol=1e-3)
    assert np.allclose(pystics_barley_test.ftemp.values, pystics_barley_mocked.ftemp.values, atol=1e-3)
    assert np.allclose(pystics_barley_test.udevcult.values, pystics_barley_mocked.udevcult.values, atol=1e-3)