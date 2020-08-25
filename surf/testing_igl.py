import igl
import nibabel as nb
import scipy as sp
from .functions import *

def write_func_data(fname, vertex_data, surf_gii):
    vertex_data = vertex_data.astype(np.float32)
    array = nb.gifti.GiftiDataArray(vertex_data, coordsys=None, datatype=nb.nifti1.data_type_codes['NIFTI_TYPE_FLOAT32'], encoding='GIFTI_ENCODING_ASCII')
    array.coordsys = None
    func_gii = nb.gifti.GiftiImage(surf_gii.header, darrays=[array])
    func_gii.to_filename(fname)

def get_lbo(vertices, faces):
    l = igl.cotmatrix(vertices, faces)
    m = igl.massmatrix(vertices, faces, igl.MASSMATRIX_TYPE_VORONOI)
    minv = sp.sparse.diags(1 / m.diagonal())
    L = -minv.dot(l)
    return L

def get_graph_laplacian(faces):
    A = -igl.adjacency_matrix(faces)
    D = A.sum(axis=1)
    A.setdiag(-np.squeeze(np.asarray(D)))
    return A

def get_laplacian(surface_name, function, u_name, lbo_u_name, gl_u_name=None):
    # check function is available
    try:
        FUNCS[function]
    except KeyError:
        print("That function isn't recognised! Please choose from:")
        for key in FUNCS.keys():
            print(key)
    
    # load surface's vertices and faces
    surface = nb.load(surface_name)
    v, f = surface.agg_data()

    # evaluate chosen function on surface's vertices' positions
    u = FUNCS[function](v)
    # save u as .func.gii for visualisation
    write_func_data(u_name, u, surface)

    # calculate laplace-beltrami operator
    lbo = get_lbo(v, f)
    # apply lbo to function evaluation and save result
    lbo_u = lbo.dot(u)
    write_func_data(lbo_u_name, lbo_u, surface)

    if gl_u_name:
        # calculate graph laplacian
        gl = get_graph_laplacian(f)
        gl_u = gl.dot(u)
        write_func_data(gl_u_name, gl_u, surface)