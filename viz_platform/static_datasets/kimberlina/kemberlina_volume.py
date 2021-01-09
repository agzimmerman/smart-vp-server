import pandas as pd
import numpy as np
from scipy.interpolate import griddata

from subsurface import UnstructuredData, StructuredData


def read_mesh_file(path):
    # row_until_mesh_no_longer = _find_CONN_sring(path)

    df = pd.read_table(path, engine='python',
                       skiprows=1,
                       header=0,
                       names=['elem', '_2', '_3', 'x', 'y', 'z'],
                       sep="\s{2,}",
                       error_bad_lines=False,
                       nrows=None
                       # escapechar='\\'
                       )
    df.dropna(axis=0, inplace=True)
    df['x'] = df.x.astype(float)

    return df


def read_attr_file(path):
    df = pd.read_table(path, sep=',')
    df.columns = df.columns.str.strip()
    df['elem'] = df.elem.str.strip()
    return df


def interpolate_points_to_regular_grid(ud: UnstructuredData):
    boundaries_max = ud.data.vertex.max(axis=0)
    boundaries_min = ud.data.vertex.min(axis=1)
    coords=dict()
    dims = ['x', 'y', 'z']
    resolution = [50, 50, 50]
    for e, i in enumerate(dims):
        coords[i] = np.linspace(boundaries_min[e], boundaries_max[e], resolution[e],
                                endpoint=False)

    grid = np.meshgrid(*coords.values())

    attr_name = 'pres'

    interpolated_attributes = griddata(ud.data.vertex,
                                       ud.data.attributes.loc[:, attr_name],
                                       tuple(grid), method='linear')

    sd = StructuredData(data=interpolated_attributes,
                        data_array_name=attr_name,
                        coords=coords)
    return sd