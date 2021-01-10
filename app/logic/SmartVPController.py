import pathlib

from viz_platform.static_datasets.kimberlina.kemberlina_surface import wells_to_subsurface_surfaces
from viz_platform.static_datasets.kimberlina.kemberlina_volume import read_mesh_file, \
    read_attr_file, interpolate_points_to_regular_grid
from viz_platform.static_datasets.kimberlina.kemberlina_wells import \
    pandas_to_subsurface, read_borehole_file, pandas_to_collars
import subsurface as ss

root_path = pathlib.Path().parent.absolute().parent.absolute()


wells_df = read_borehole_file(
            root_path / 'tests/data/kimberlina/doggr_jlw_vedder_final.utm.dat',
            fix_df=True)


class SmartVPController:
    @staticmethod
    def file_to_subsurface_wells():

        wells_unstructured_data = pandas_to_subsurface(wells_df)
        return wells_unstructured_data.to_binary(order='F')

    @staticmethod
    def file_to_subsurface_volume():
        mesh_df = read_mesh_file(root_path / 'tests/data/kimberlina/mesh')
        attr_df = read_attr_file(root_path / 'tests/data/kimberlina/out_all00')
        combined_df = mesh_df.merge(attr_df, on='elem')

        ud = ss.UnstructuredData(vertex=combined_df[['x', 'y', 'z']],
                                 attributes=combined_df[['pres', 'temp',
                                                         'sg', 'xco2']])

        sd = interpolate_points_to_regular_grid(ud)
        return sd.to_binary(order='F')

    @staticmethod
    def file_to_subsurface_collars():

        unstruct_collars = pandas_to_collars(wells_df)
        return unstruct_collars.to_binary(order='F')

    @staticmethod
    def file_to_subsurface_surfaces():
        ud = wells_to_subsurface_surfaces(wells_df)
        return ud.to_binary(order='F')