import numpy as np

class IsingModel:
    """
    Clase para simular el modelo de Ising en 40x40
    """

    def __init__(self, lattice):
        self.lattice = lattice
        self.size = lattice.shape[0]
    
    @classmethod

    # Iniciamos la red de manera random
    def initiate(cls, size=40):
        random_lattice = 2 * np.random.randint(0, 2, size=(size, size)) - 1
        return cls(random_lattice)
    
    @classmethod

    # Iniciamos la red con todos los espines en +1
    def initiate_plus(cls, size=40, spin=1):
        lattice = np.full((size, size), spin)
        return cls(lattice)
    
    @classmethod

    # Mostrar la configuración de la red
    def visualize(self):
        print(f"Configuración de la red: {self.size} x {self.size}:")
        print(self.lattice)