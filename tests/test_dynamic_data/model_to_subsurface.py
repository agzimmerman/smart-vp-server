import pickle

from subsurface.visualization import update_grid_attribute

from viz_platform.dynamic_datasets.adapter.model_to_subsurface import \
    data_to_subsurface, subsurface_to_pyvista
from viz_platform.dynamic_datasets.read_from_sql import read_from_mysql_database
import numpy as np
import subsurface as ss


def test_data_to_subsurface(regenerate=False):
    if regenerate is True:
        scenario = read_from_mysql_database()
        data = pickle.loads(scenario.simulations[0].fields[0].data)
    else:
        data = np.load('../data/pressure.npy')

    sd = data_to_subsurface(data, coords_names=['x', 'y', 'z', 'time'])
    ss.interfaces.base_structs_to_binary_file('pressure_order_F', sd)
    subsurface_to_pyvista(sd, image_2d=True, attribute_slice={'time': 2})


