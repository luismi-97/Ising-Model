import numpy as np
import matplotlib.pyplot as plt

from dinamicas import glauber, metropolis
from model import IsingModel
from observables import energy, magnetization, chi

def simulation():
    """
    Simulaciones Montecarlo para un sistema de N = 40 x 40 espines.
    h = 1
    T = 4.0, 3.0, 2.27, 2.0, 1.0, 0.1
    pasos_MC = 1000
    ---------------------------------------------------------------
    0. Configuraciones del ejercicio
    1. Realizamos las simulaciones para ambas dinámicas
    2. Printeamos los resultados numéricos en tablas
    3. Definimos funciones analíticas
    4. Comparamos resultados de las simulaciones y analíticos en gráficas
    """

    print("\n" + "[simulation] - Empieza")

    # 0. CONFIGURACIONES -----------------------------------------

    temperatures = [4.0, 3.0, 2.27, 2.0, 1.0, 0.1]
    paths = 1000
    
    model = IsingModel.initiate()

    metropolis_results = {'T' : temperatures, 'm' : [], 'u' : [], 'chi' : []}
    glauber_results = {'T' : temperatures, 'm' : [], 'u' : [], 'chi' : []}

    # 1. SIMULACIONES ---------------------------------------------

    print("\n" + "[simulation] - Simulacion")

    def montecarlo(model, paths, T, algorithm):
        # Comprobamos que el algoritmo sea correcto
        if algorithm.lower() not in ['metropolis', 'glauber']:
            raise ValueError('Algoritmo no válido')
        
        beta = 1.0 / T
        lattice = model.lattice.copy()

        if algorithm.lower() == 'metropolis':
            algoritmo = metropolis
        else:
            algoritmo = glauber

        # inicializamos los observables medidos
        u = []
        m = []
        c = []

        for path in range(paths):
            lattice = algoritmo(lattice, T, h=1, J=0)

            if (path + 1) % 50 == 0:
                # nos guaradamos las medidas cada 50 pasos
                u_measured = energy(lattice)
                u.append(u_measured)
                m_measured = magnetization(lattice)
                m.append(m_measured)
                c_measured = chi(lattice, beta)
                c.append(c_measured)

        # promediamos
        u_avg = np.mean(u)
        m_avg = np.mean(m)
        chi_avg = np.mean(c)
        
        return {
            'lattice' : lattice,
            'energy' : u_avg,
            'magnetization' : m_avg,
            'chi' : chi_avg,
        }

    # simulamos montecarlo para cada temperatura segun ambas dinaamicas
    print("METROPOLIS")
    for T in temperatures:
        print(f"T = {T}")
        results = montecarlo(model, paths, T, 'metropolis')
        metropolis_results['u'].append(results['energy'])
        metropolis_results['m'].append(results['magnetization'])
        metropolis_results['chi'].append(results['chi'])
    
    print("GLAUBER")
    for T in temperatures:
        print(f"T = {T}")
        results = montecarlo(model, paths, T, 'glauber')
        glauber_results['u'].append(results['energy'])
        glauber_results['m'].append(results['magnetization'])
        glauber_results['chi'].append(results['chi'])
    
    # 2. TABLAS --------------------------------------------------

    print("\n" + "[simulation] - Tablas")
    
    print("\n" + "="*60)
    print("Resultados de las simulaciones por dinámica de METROPOLIS")
    print("="*60)

    print(f"{'Temperatura':<15} {'u(T)':<15} {'m(T)':<15} {'chi(T)':<15}")
    print("-"*60)

    for i, T in enumerate(temperatures):
        print(f"{T:<15.3f} | {metropolis_results['u'][i]:<15.3f} | {metropolis_results['m'][i]:<15.3f} | {metropolis_results['chi'][i]:<15.3f}")

    print("="*60 + "\n")
    
    print("\n" + "="*60)
    print("Resultados de las simulaciones por dinámica de GLAUBER")
    print("="*60)

    print(f"{'Temperatura' :<15} {'u(T)':<15} {'m(T)':<15} {'chi(T)':<15}")
    print("-"*60)

    for i, T in enumerate(temperatures):
        print(f"{T:.3f} | {glauber_results['u'][i]:.3f} | {glauber_results['m'][i]:.3f} | {glauber_results['chi'][i]:.3f}")

    print("="*60 + "\n")

    # 3. FUNCIONES ANALITICAS ------------------------------------------

    print("\n" + "[simulation] - Funciones Analiticas")

    T_analytical = np.linspace(0.1, 4.0, 200)
    beta_analytical = 1.0 / T_analytical

    # u = -h*tanh(ß*h)
    u_analytical = -1.0 * np.tanh(beta_analytical * 1.0)
    # m = tanh(ß*h)
    m_analytical = np.tanh(beta_analytical * 1.0)
    # chi/N = ß*sech^2(ß*h)
    chi_analytical = beta_analytical * (1.0 / np.cosh(beta_analytical * 1.0))**2

    # 4. GRAFICAS ------------------------------------------------------

    print("\n" + "[simulation] - Graficas")

    fig, axes = plt.subplots(1, 3, figsize = (14, 5))
    fig.suptitle('\n Comparacion de los resultados analíticos con las simulaciones de u, m y chi/N')

    for i, obs in enumerate(['m', 'u', 'chi']):
        if obs == 'm':
            func = m_analytical
        elif obs == 'u':
            func = u_analytical
        else:
            func = chi_analytical

        ax = axes[i]
        ax.plot(metropolis_results['T'], metropolis_results[obs], 'o-', label='Metropolis', lw=1.5, markersize=4, color= 'blue')
        ax.plot(glauber_results['T'], glauber_results[obs], 's-', label='Glauber', lw=1.5, markersize=4, color= 'orange')
        ax.plot(T_analytical, func, '-', label='Analytical', lw=1.5, color='green', alpha=0.7)
        ax.set_xlabel('Temperatura (T)', fontsize=11, fontweight='bold')
        ax.set_ylabel(f"{obs}(T)", fontsize=11, fontweight='bold')
        ax.set_title(f"{obs} vs T", fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()

    plt.tight_layout()
    plt.show()

    # FIN

    print("\n" + "[simulation] - Check")


# ---- CURVA DE RELAJACION ------------------------------------------

def relax_curve():
    """
    Función para mostrar la comparacion de la curva de relajacion hacia el equilibrio 
    empezando desde un estado de magnetizacion m = 1 (todos los espines s_i = +1).
    Promediamos la magnetizacion por espin cada paso montecarlo durante los primeros
    100 pasos. Luego promediamos sobre 100 realizaciones de esta simulacion. 
    T = 0.1, 2.27, 4.0
    h = 1
    pasos_MC = 100
    realizaciones = 100
    ---------------------------------------------------------------------------------
    0. Configuraciones del ejercicio
    1. Funcion que realiza simulaciones montecarlo y promedia m en cada paso 
    2. Promediamos sobre 100 realizaciones de la simulacion para cada algoritmo y temperatura
    3. Graficas comparacion de las curvas para cada dinamica y temperatura
    """

    print("\n" + "[relax_curve] - Empieza")

    # 0. CONFIGURACIONES ------------------------------------------------------------

    temperatures = [0.1, 2.27, 4.0]
    realizations = 100
    paths = 100

    # 1. SIMULACION ---------------------------------------------------------------

    print("\n" + "[relax_curve] - Simulacion")

    def montecarlo_relax(T, algorithm):
        if algorithm.lower() not in ['metropolis', 'glauber']:
            raise ValueError("Algoritmo no válido")
        
        if algorithm == "metropolis":
            algoritmo = metropolis
        else:
            algoritmo = glauber

        lattice = IsingModel.initiate_plus().lattice.copy()

        m = []

        for path in range(paths):
            lattice = algoritmo(lattice, T, h=1, J=0)
            magn = magnetization(lattice)
            m.append(magn)

        return np.array(m)
    
    # 2. PROMEDIO --------------------------------------------------------------

    print("\n" + "[relax_curve] - Promedio")

    results = {
        'metropolis' : {},
        'glauber' : {},
        'paths' : np.arange(1, 101)
    }

    for algorithm in ['metropolis', 'glauber']:
        print(f"{algorithm.upper()}:")
        for T in temperatures:
            print(f"T = {T}")
            curves = []
            for r in range(realizations):
                curve = montecarlo_relax(T, algorithm)
                curves.append(curve)

            mean_curve = np.mean(curves, axis=0)

            results[algorithm][T] = {
                'mean' : mean_curve,
            }
    
    # 3. GRAFICAS -------------------------------------------------------------

    print("\n" + "[relax_curve] - Graficas")

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    fig.suptitle('Curvas de Relajación para cada temperatura según ambas dinámicas', fontsize=11, fontweight='bold')

    for i, T in enumerate(temperatures):
        ax = axes[i]
        # Visualizamos dinámica de metropolis
        ax.plot(results['paths'], results['metropolis'][T]['mean'], label='Metropolis', lw=1, color='blue', alpha=0.8)
        # Visualizamos dinámica de glauber
        ax.plot(results['paths'], results['glauber'][T]['mean'], label='Glauber', lw=1, color='orange', alpha=0.8)
        ax.set_title(f"T = {T}", fontsize=12, fontweight='bold')
        ax.set_xlabel('Pasos Montecarlo', fontsize=11, fontweight='bold')
        ax.set_ylabel('Magnetización por spin', fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.2)
        ax.legend(loc='best', fontsize=10)

    plt.tight_layout()
    plt.show()

    # FIN

    print("\n" + "[relax_curve] - Check")

