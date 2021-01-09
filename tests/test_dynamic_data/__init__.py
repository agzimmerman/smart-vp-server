import pickle

from viz_platform.dynamic_datasets.adapter.model_to_subsurface import \
    data_to_subsurface
from viz_platform.dynamic_datasets.read_from_sql import read_from_mysql_database


def test_data_to_subsurface():
    scenario = read_from_mysql_database()
    data = pickle.loads(scenario.simulations[0].fields[0].data)
    data_to_subsurface(data)

