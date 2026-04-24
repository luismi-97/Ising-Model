import numpy as np

"""
Funciones para calcular los observables durante el proyecto.
h = 1
"""

def energy(lattice):
    """
    u = -h/N * ∑s_i
    """
    size = lattice.shape[0]
    N = size * size
    suma = np.sum(lattice)

    return - 1 / N * suma

def magnetization(lattice):
    """
    m = 1/N * ∑s_i
    """
    size = lattice.shape[0]
    N = size * size
    suma = np.sum(lattice)

    return 1 / N * suma

def chi(lattice, beta):
    """
    chi/N = ßVar(M)
    M = ∑s_i
    """
    size = lattice.shape[0]
    N = size * size
    suma = np.sum(lattice)
    var = (1 - (suma/N)**2)

    return beta * var