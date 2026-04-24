import numpy as np

def metropolis(lattice, T, h, J):
    """
    π = min(1, exp(-ß*dE))
    """
    size = lattice.shape[0]
    beta = 1.0 / T

    for m in range(size * size):
        i = np.random.randint(0, size)
        j = np.random.randint(0, size)

        s = lattice[i, j]

        vecinos = lattice[(i+1) % size, j] + lattice[(i-1) % size, j] + lattice[i, (j+1) % size] + lattice[i, (j-1) % size]

        dE = 2 * s * (J * vecinos + h)

        if dE < 0 or np.random.rand() < np.exp(- beta * dE):
            lattice[i, j] *= -1

    return lattice

def glauber(lattice, T, h, J):
    """
    π = 1 / (1 + exp(ß*dE))
    """
    size = lattice.shape[0]
    beta = 1.0 / T

    for m in range(size * size):
        i = np.random.randint(0, size)
        j = np.random.randint(0, size)

        s = lattice[i, j]

        vecinos = lattice[(i+1) % size, j] + lattice[(i-1) % size, j] + lattice[i, (j+1) % size] + lattice[i, (j-1) % size]

        dE = 2 * s * (J * vecinos + h)

        if np.random.rand() < 1 / (1 + np.exp(beta * dE)):
            lattice[i, j] *= -1

    return lattice