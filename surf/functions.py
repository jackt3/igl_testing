import numpy as np

def sumsincos(v):
    return np.sin(0.5*v[:, 1]) + np.cos(0.5*v[:, 2])

FUNCS = {
    'sumsincos': sumsincos
}