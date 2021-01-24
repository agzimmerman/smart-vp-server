import pathlib

from viz_platform.dynamic_datasets.adapter.model_to_subsurface import data_to_subsurface
from viz_platform.static_datasets.kimberlina.kemberlina_surface import wells_to_subsurface_surfaces
from viz_platform.static_datasets.kimberlina.kemberlina_volume import read_mesh_file, \
    read_attr_file, interpolate_points_to_regular_grid
from viz_platform.static_datasets.kimberlina.kemberlina_wells import \
    pandas_to_subsurface, read_borehole_file, pandas_to_collars
import subsurface as ss
import numpy as np

root_path = pathlib.Path().parent.absolute().parent.absolute()

wells_df = read_borehole_file(
    root_path / 'tests/data/kimberlina/doggr_jlw_vedder_final.utm.dat',
    fix_df=True)


class SmartVPController:
    @staticmethod
    def file_to_subsurface_wells(model: str):
        if model == 'model:Kimberlina':
            wells_unstructured_data = pandas_to_subsurface(wells_df)
        else:
            raise ValueError("Model guid not found in the server.")

        return wells_unstructured_data.to_binary(order='F')

    @staticmethod
    def file_to_subsurface_volume(model: str):
        if model == 'model:Kimberlina':
            sd = SmartVPController._read_and_interpolate_kimberlina()
        elif model == 'model:Dynamic':
            data = np.load(root_path / 'tests/data/pressure.npy')
            sd = data_to_subsurface(data, coords_names=['x', 'y', 'z', 'time'])
        else:
            raise ValueError("Model guid not found in the server.")

        return sd.to_binary(order='F')

    @staticmethod
    def _read_and_interpolate_kimberlina():
        mesh_df = read_mesh_file(root_path / 'tests/data/kimberlina/mesh')
        attr_df = read_attr_file(root_path / 'tests/data/kimberlina/out_all00')
        combined_df = mesh_df.merge(attr_df, on='elem')
        ud = ss.UnstructuredData(vertex=combined_df[['x', 'y', 'z']],
                                 attributes=combined_df[['pres', 'temp',
                                                         'sg', 'xco2']])
        sd = interpolate_points_to_regular_grid(ud)
        return sd

    @staticmethod
    def file_to_subsurface_collars(model: str):
        if model == 'model:Kimberlina':
            unstruct_collars = pandas_to_collars(wells_df)
        else:
            raise ValueError("Model guid not found in the server.")
        return unstruct_collars.to_binary(order='F')

    @staticmethod
    def file_to_subsurface_surfaces(model: str):
        if model == 'model:Kimberlina':
            ud = wells_to_subsurface_surfaces(wells_df, switch_yz=True, two_faces=False,
                                              accumulate_edges=False)
        else:
            raise ValueError("Model guid not found in the server.")
        return ud.to_binary(order='F')
