import subsurface as sb


def data_to_subsurface(data, coords_names=None):
    sd = sb.StructuredData(data, coords_names=coords_names)
    return sd


def subsurface_to_pyvista(sd, attribute_slice=None, **kwargs):
    if 'image_2d' not in kwargs:
        kwargs['image_2d'] = False
    sg = sb.StructuredGrid(sd)
    mesh = sb.visualization.to_pyvista_grid(sg, attribute_slice=attribute_slice)
    sb.visualization.pv_plot([mesh], **kwargs)
    return mesh