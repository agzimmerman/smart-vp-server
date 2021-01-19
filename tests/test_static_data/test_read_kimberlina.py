from viz_platform.static_datasets.kimberlina.kemberlina_surface import \
    wells_to_subsurface_surfaces
from viz_platform.static_datasets.kimberlina.kemberlina_wells import \
    read_borehole_file, pandas_to_subsurface, pandas_to_collars
from viz_platform.static_datasets.kimberlina.kemberlina_volume import read_mesh_file, \
    read_attr_file, interpolate_points_to_regular_grid
import subsurface as ss
import pandas as pd
import numpy as np


def test_read_mesh():
    mesh_df = read_mesh_file('../data/kimberlina/mesh')
    print(mesh_df)


def test_read_attr():
    attr_file = read_attr_file('../data/kimberlina/out_all00')
    print(attr_file)


def test_kimberlina_to_subsurface():
    mesh_df = read_mesh_file('../data/kimberlina/mesh')
    attr_df = read_attr_file('../data/kimberlina/out_all00')
    combined_df = mesh_df.merge(attr_df, on='elem')

    ud = ss.UnstructuredData(vertex=combined_df[['x', 'y', 'z']],
                             attributes=combined_df[['pres', 'temp',
                                                     'sg', 'xco2']])

    ss.interfaces.base_structs_to_binary_file('kimberline_point_order_F', ud)
    ps = ss.PointSet(ud)
    mesh = ss.visualization.to_pyvista_points(ps)
    ss.visualization.pv_plot([mesh], image_2d=True)


def test_interpolate_to_regular_grid():
    mesh_df = read_mesh_file('../data/kimberlina/mesh')
    attr_df = read_attr_file('../data/kimberlina/out_all00')
    combined_df = mesh_df.merge(attr_df, on='elem')

    ud = ss.UnstructuredData(vertex=combined_df[['x', 'y', 'z']],
                             attributes=combined_df[['pres', 'temp',
                                                     'sg', 'xco2']])

    sd = interpolate_points_to_regular_grid(ud)
    ss.interfaces.base_structs_to_binary_file('VP_challenge_volume_order_F',
                                              sd)

    sg = ss.StructuredGrid(sd)


    mesh = ss.visualization.to_pyvista_grid(sg)
    ss.visualization.pv_plot([mesh], image_2d=False)

    return


def test_read_kimberlina_wells():
    wells_df = read_borehole_file('../data/kimberlina/doggr_jlw_vedder_final.utm.dat',
                                  fix_df=True)
    return wells_df


def test_pandas_to_welly():
    wells_df = test_read_kimberlina_wells()
    wells_unstructured_data = pandas_to_subsurface(wells_df)

    wells_element = ss.LineSet(wells_unstructured_data)

    # Pyvista mesh
    wells_mesh = ss.visualization.to_pyvista_line(wells_element, radius=50)

    ss.interfaces.base_structs_to_binary_file('VP_challenge_wells_order_F',
                                              wells_unstructured_data)

    # Plotting
    ss.visualization.pv_plot(
        [wells_mesh],
        image_2d=True,
        ve=5
    )

    return wells_mesh


def test_pandas_to_collars():
    wells_df = test_read_kimberlina_wells()
    unstruct_collars = pandas_to_collars(wells_df)
    ss.interfaces.base_structs_to_binary_file('VP_challenge_wells_collars_order_F',
                                              unstruct_collars)
    print(unstruct_collars)


def test_surfaces_to_subsurface():
    wells_df = test_read_kimberlina_wells()
    ud = wells_to_subsurface_surfaces(wells_df)

    tri = ss.TriSurf(ud)
    mesh = ss.visualization.to_pyvista_mesh(tri)

    ss.visualization.pv_plot([mesh], image_2d=True, ve=10)

    return mesh


def test_wells_and_surfaces():
    well_mesh = test_pandas_to_welly()
    surface_mesh = test_surfaces_to_subsurface()
    ss.visualization.pv_plot([well_mesh, surface_mesh], image_2d=True, ve=3)




