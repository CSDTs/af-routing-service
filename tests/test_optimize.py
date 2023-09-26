import openrouteservice as ors
import datetime
import ast
import pytest
import os

KEY = "OSRM_API_KEY"

def timestamp_of(the_timestamp):
    return int(datetime.datetime.strptime('2019-03-22 08:00:00', '%Y-%m-%d %H:%M:%S').timestamp())

@pytest.fixture
def expected_idai():
    def load_dict_from_file(filepath):
        with open(filepath, 'r') as file:
            dict_string = file.read()

        dictionary = ast.literal_eval(dict_string)
        return dictionary    
    return load_dict_from_file('./expected_idai.dict')

@pytest.fixture
def ors_client():
    return ors.Client(key=os.environ.get(KEY))  

@pytest.fixture
def jobs():
    """
    Hurrican Idai; https://github.com/GIScience/openrouteservice-examples/blob/master/resources/data/idai_health_sites.csv

    1	33.9852423	-19.8202962	2019-03-22 08:00:00	2019-03-22 18:00:00	24
    """
    return [
        ors.optimization.Job(
            id=1,
            location=[33.9852423, -19.8202962],
            service=1200,  # Assume 20 minutes at each site
            amount=[24],
            time_windows=[[
                timestamp_of("2019-03-22 08:00:00"),
                timestamp_of("2019-03-22 18:00:00")
            ]]
        )
    ]  

@pytest.fixture
def vehicles():
    return [
        ors.optimization.Vehicle(
            id=7,
            start=[34.835447, -19.818474],
            capacity=[300],
            time_window=[1553241600, 1553284800]
        )
    ]


def test_1j_1v_optimization(ors_client, jobs, vehicles):
    result = ors_client.optimization(
        jobs=jobs,
        vehicles=vehicles,
        geometry=True
    )

    print(result)

    5/0