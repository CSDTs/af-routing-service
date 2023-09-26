import openrouteservice as ors
import datetime
import ast
import pytest
import os

KEY = "OSRM_API_KEY"
AF_KEY = "AF_BASE_URL"

def timestamp_of(the_timestamp):
    return int(datetime.datetime.strptime('2019-03-22 08:00:00', '%Y-%m-%d %H:%M:%S').timestamp())

@pytest.fixture
def expected_mi():
    def load_dict_from_file(filepath):
        with open(filepath, 'r') as file:
            dict_string = file.read()

        dictionary = ast.literal_eval(dict_string)
        return dictionary    
    return load_dict_from_file('./tests/expected_mi.dict')

@pytest.fixture
def orms_client():
    return ors.Client(key=os.environ.get(KEY))
    

@pytest.fixture
def af_client():
    #return ors.Client(base_url=os.environ.get(AF_KEY)) # could be the local container, MI based
    return ors.Client('http://localhost:8080/')

def reverse(arr):
    return [arr[1], arr[0]]

@pytest.fixture
def mi_1j_1v_job():
    return [
        ors.optimization.Job(
            id=1,
            # longitude, latitude order
            location=[
                    -83.16220076371327,
                    42.41754281551739
                ],
            skills=[1],
            service=300,  # Assume 20 minutes at each site
            amount=[1],
            time_windows=[[32400,36000]]
        )
    ]  

@pytest.fixture
def mi_1j_1v_vehicle():
    return [
        ors.optimization.Vehicle(
            id=1,
            start=[
                -82.96820310588846,
                42.42396039614465
            ],
            skills=[1],
            capacity=[4],
            time_window=[28800,43200]
        )
    ]

def test_1j_1v_ors_optimization(orms_client, mi_1j_1v_job, mi_1j_1v_vehicle, expected_mi):
    """
    This is really a sanity check that service at minimum returns 
    what we'd expect in the simplest case; more of a check of
    argument order (lat lon vs lon lat), units of values
    """

    result = orms_client.optimization(
        jobs=mi_1j_1v_job,
        vehicles=mi_1j_1v_vehicle,
        geometry=True
    )

    for key in ['unassigned','delivery', 'service']:
        assert expected_mi['summary'][key] == result['summary'][key], f"{key} was not the same! expected_mi['summary'][{key}]={expected_mi[key]} vs result['summary'][{key}]={result[key]}"

def test_1j_1v_local_optimization(af_client, mi_1j_1v_job, mi_1j_1v_vehicle, expected_mi):
    """
    This is really a sanity check that service at minimum returns 
    what we'd expect in the simplest case; more of a check of
    argument order (lat lon vs lon lat), units of values
    """

    result = af_client.optimization(
        jobs=mi_1j_1v_job,
        vehicles=mi_1j_1v_vehicle,
        geometry=True
    )

    for key in ['unassigned','delivery', 'service']:
        assert expected_mi['summary'][key] == result['summary'][key], f"{key} was not the same! expected_mi['summary'][{key}]={expected_mi[key]} vs result['summary'][{key}]={result[key]}"

