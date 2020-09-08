import numpy as np

def sumsincos(v, s=1.0):
    """
    Given an array of vertices' 3D coordinates, `v`, evaluate 
    the sum of the sine of the y coordinate with the cosine 
    of the z coordinates at each vertex.

    Parameters
    ----------
    v : np.array
        (Nx3) array of vertex coordinates.
    s : float, optional
        Modifies the periodicity of the function.

    Returns
    -------
    f : np.array
        (Nx1) array of function evaluations.
    """
    return np.sin(s*v[:, 1]) + np.cos(s*v[:, 2])

FUNCS = {
    'sumsincos': sumsincos
}