import numpy as np
from .functions import *

def curv_sincosxy(v, s=1.0):
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
    f = sumsincosxy(v, s)
    Lf = (s**2) * f
    return Lf

def curv_sincosxz(v, s=1.0):
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
    f = sumsincosxz(v, s)
    Lf = (s**2) * f
    return Lf

def curv_sincosyz(v, s=1.0):
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
    f = sumsincosyz(v, s)
    Lf = (s**2) * f
    return Lf

CURVS = {
    'sumsincosxy': curv_sincosxy,
    'sumsincosxz': curv_sincosxz,
    'sumsincosyz': curv_sincosyz
}

def analytic_curvature(v, func, s=1.0):
    """
    Return the analytical curvature of the function `func`.

    Will throw an error if analytic curvature has not been 
    defined for this function.

    Parameters
    ----------
    v : numpy array
        Array of vertex coordinates.
    func : str
        Function which has been evaluated on the surface.
    s : float
        Speed at which the function varies.
    
    Returns
    -------
    Lf : numpy array
        (N x 1) array of curvatures at each vertex.
    """

    try:
        curv_func = CURVS[func]
    except KeyError:
        print("The analytic curvature is not defined"
            +" for your chosen function!")
    Lf = curv_func(v, s)
    return Lf