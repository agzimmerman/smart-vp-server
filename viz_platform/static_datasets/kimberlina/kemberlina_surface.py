import numpy as np
import scipy
import pandas as pd
from scipy.spatial.qhull import Delaunay, QhullError
import subsurface as ss


def wells_to_subsurface_surfaces(wells: pd.DataFrame,
                                 accumulate_edges=True,
                                 switch_yz=False,
                                 two_faces=False):
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
    point_attributes = np.zeros((0), dtype=int)
    cell_attributes = np.zeros((0), dtype=int)

    last_cell = 0

    for e, f in enumerate(["topo",
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
                           ]):
        # if not (e) % 2 == 0:
        #     print((e) % 2)
        #     print("\n pass:", f)
        #     continue

        try:
            vertex_item = interp(wells_temp.loc[[f], 'x'],
                            wells_temp.loc[[f], 'y'],
                            wells_temp.loc[[f], 'z'].values,
                            nn)

            faces = Delaunay(vertex_item[:, [0, 1]]).simplices

            cells_item = faces + last_cell if accumulate_edges else faces

            attribute_item = np.ones((vertex_item.shape[0])) * e + 1
            cell_attribute_item = np.ones((faces.shape[0])) * e + 1

            # if two_faces:
            #     cells_aux = cells_item.copy()
            #     cells_item[:, 1] = cells_aux[:, 2]
            #     cells_item[:, 2] = cells_aux[:, 1]
            #
            #     vertex_item = np.vstack((vertex_item, vertex_item))
            #     cells_item = np.vstack((cells_item, cells_aux + last_cell)) if accumulate_edges \
            #         else np.vstack((cells_item, cells_aux))
            #     attribute_item = np.hstack((attribute_item, attribute_item))
            #     cell_attribute_item = np.hstack((cell_attribute_item, cell_attribute_item))

            vertex = np.vstack((vertex, vertex_item))
            cells = np.vstack((cells, cells_item))
            point_attributes = np.append(point_attributes, attribute_item)
            cell_attributes = np.append(cell_attributes, cell_attribute_item)
            last_cell = cells.max() + 1

        except QhullError:
            print(f'Formation {f} could not be interpolated.')
            continue

    # Switch YZ coord
    cells_aux = cells.copy()
    if switch_yz:

        cells[:, 1] = cells_aux[:, 2]
        cells[:, 2] = cells_aux[:, 1]

    if two_faces:
        vertex = np.vstack((vertex, vertex))
        cells = np.vstack((cells, cells_aux + last_cell)) if accumulate_edges else np.vstack((cells, cells_aux))
        point_attributes = np.hstack((point_attributes, point_attributes))
        cell_attributes = np.hstack((cell_attributes, cell_attributes))

    ud = ss.UnstructuredData(vertex=vertex,
                             cells=cells,
                             attributes=pd.DataFrame({'formation_cell': cell_attributes.T}),
                             points_attributes=pd.DataFrame({'formation': point_attributes.T}),
                             )

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
