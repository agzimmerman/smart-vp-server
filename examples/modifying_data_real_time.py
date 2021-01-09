from subsurface.visualization import update_grid_attribute

from viz_platform.dynamic_datasets.adapter.model_to_subsurface import \
    data_to_subsurface, subsurface_to_pyvista

import numpy as np
import subsurface as ss
import pathlib

root_path = pathlib.Path().parent.absolute()

# %%
# This is the code to interactively change the time property.
#
# %%
data = np.load(root_path / 'tests/data/pressure.npy')

sd = data_to_subsurface(data, coords_names=['x', 'y', 'z', 'time'])
mesh = subsurface_to_pyvista(sd, attribute_slice={'time': 2}, background_plotter=True)


# %%
update_grid_attribute(mesh, ss.StructuredGrid(sd),
                      attribute_slice={'time': 20})

