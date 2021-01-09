import numpy as np
import scipy
import pandas as pd
from scipy.spatial.qhull import Delaunay, QhullError
import subsurface as ss


def wells_to_subsurface_surfaces(wells: pd.DataFrame):
    wells_temp = wells.set_index('formation')

    formations = ["topo",
                  "etchegoin",
                  "macoma",
                  "chanac",
                  "mclure",
                  "santa_margarita",
                  "fruitvale",
                  "round_mountain",
                  "olcese",
                  "freeman_jewett",
                  "vedder",
                  "eocene",
                  "cretaceous",
                  "basement",
                  "null"]

    nn = 100
    vertex = np.zeros((0, 3))
    cells = np.zeros((0, 3), dtype=int)
    attributes = np.zeros((0), dtype=int)

    last_cell = 0

    for e, f in enumerate(formations[:-2]):
        try:
            vertex_item = interp(wells_temp.loc[[f], 'x'],
                            wells_temp.loc[[f], 'y'],
                            wells_temp.loc[[f], 'z'].values,
                            nn)

            faces = Delaunay(vertex_item[:, [0, 1]]).simplices

            cells_item = faces + last_cell
            attribute_item = np.ones((vertex_item.shape[0])) * e + 1

            vertex = np.vstack((vertex, vertex_item))
            cells = np.vstack((cells, cells_item))
            attributes = np.append(attributes, attribute_item)
            last_cell = cells.max() + 1

        except QhullError:
            print(f'Formation {f} could not be interpolated.')
            continue

    ud = ss.UnstructuredData(vertex=vertex,
                             cells=cells,
                             points_attributes=pd.DataFrame({'formation': attributes.T}))

    return ud


def interp(x, y, z, nn):
    pts = np.zeros([len(x), 2], dtype='float')
    pts[:, 0] = x
    pts[:, 1] = y
    np.max(pts)
    X, Y = np.meshgrid(np.linspace(np.min(x), np.max(x), nn),
                       np.linspace(np.min(y), np.max(y), nn))
    X = X.ravel()
    Y = Y.ravel()

    f1 = scipy.interpolate.LinearNDInterpolator(pts, z, rescale=True)
    Z = f1(X, Y)

    # Drop nans and make an array from them
    vertex = pd.DataFrame(np.array([X, Y, Z]).T).dropna().values

    return vertex
