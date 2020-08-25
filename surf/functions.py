import numpy as np

def sumsincos(v):
    """
    Given an array of vertices' 3D coordinates, `v`, evaluate 
    the sum of the sine of the y coordinate with the cosine 
    of the z coordinates at each vertex.
    """
    return np.sin(0.1*v[:, 1]) + np.cos(0.1*v[:, 2])

FUNCS = {
    'sumsincos': sumsincos
}