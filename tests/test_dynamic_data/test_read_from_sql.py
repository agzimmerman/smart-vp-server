import pickle

import numpy

from viz_platform.dynamic_datasets.adapter.model_to_subsurface import data_to_subsurface
from viz_platform.dynamic_datasets.read_from_sql import read_from_mysql_database


def test_read_from_sql_1(save=False):
    scenario = read_from_mysql_database()
    print(scenario)
    data = pickle.loads(scenario.simulations[0].fields[0].data)
    if save:
        numpy.save('../data/pressure', data)
    data_to_subsurface(data)
