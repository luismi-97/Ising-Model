from parte1 import simulation, relax_curve
from parte2 import simulation2

def main():
    print("\n" + "="*60)
    print("Proyecto Modelo de Ising")
    print("="*60)

    # 1. Simulaciones Ejercicio 1
    simulation()

    # 2. Curva de Relajacion
    relax_curve()

    # 3. Ejercicio 2
    simulation2()

    # Todo bien
    print("\n" + "-"*30 + "TODO BIEN" + "-"*30)

if __name__ == "__main__":
    main()
