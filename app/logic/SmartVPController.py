import pathlib

from viz_platform.static_datasets.kimberlina.kemberlina_wells import \
    pandas_to_subsurface, read_borehole_file
import subsurface as ss

root_path = pathlib.Path().parent.absolute().parent.absolute()


class SmartVPController:
    def file_to_subsurface(self):
        wells_df = read_borehole_file(
            root_path / 'tests/data/kimberlina/doggr_jlw_vedder_final.utm.dat',
            fix_df=True)

        wells_unstructured_data = pandas_to_subsurface(wells_df)
        return wells_unstructured_data.to_binary(order='F')
