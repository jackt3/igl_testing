import numpy as np
from .functions import *

def curv_sincos(v, s=1.0):
    """
    Evaluate the curvature of the sin+cos function.

    Parameters
    ----------
    v : np.array
        (Nx3) array of vertex coordinates.
    s : float, optional
        Modifies the periodicity of the function.
    
    Returns
    -------
    Lf : np.array
        (Nx1) array of curvature evaluations.
    """
    f = sumsincos(v, s)
    Lf = (s**2) * f
    return Lf

CURVS = {
    'sumsincos': curv_sincos
}

def analytic_curvature(v, func, s):
    """
    Return the analytical curvature of the function `func`.

    Parameters
    ----------
    v : numpy array
        Array of vertex coordinates.
    func : str
        Function which has been evaluated on the surface.
    
    Returns
    -------
    Lf : numpy array
        Array of curvature at each vertex.
    """

    curv_func = CURVS[func]
    Lf = curv_func(v, s)
    return Lf