import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from model import IsingModel
from dinamicas import glauber, metropolis
from observables import energy, magnetization, chi

def simulation2():
    """
    Función que realiza simulaciones Montecarlo de un sistema de N = 40 x 40 espines
    usando la dinámica de Metrópolis.
    h = 0
    J = 1
    T = 4.0, 3.0, 2.27, 2.0, 1.0, 0.1
    pasos_MC = 1000
    ---------------------------------------------------------------------------------
    0. Configuracion del ejercicio
    1. Simulaciones para cada temperatura y promediamos m, u y chi/N
    2. Representamos los resultados de las simulaciones
    3. Representamos configuraciones típicas para distintas temperaturas
    4. Video de evolucion hacia el equilibrio para T=0.1
    """

    print("\n" + "[simulation2] - Empieza")

    # 0. CONFIGURACION

    temperatures = [4.0, 3.0, 2.27, 2.0, 1.0, 0.1]
    paths = 1000

    model = IsingModel.initiate()
    
    results = {'T' : temperatures, 'm' : [], 'u' : [], 'chi' : []}
    configurations = {}
    lista = []

    # 1. SIMULACION
    
    print("METROPOLIS")
    
    for T in temperatures:
        print(f"T = {T}")
        m = []
        u = []
        c = []
        beta = 1.0 / T
        lattice = model.lattice.copy()

        for path in range(paths):
            lattice = metropolis(lattice, T, h=0, J=1)

            if (path + 1) % 50 == 0:
                u_m = energy(lattice)
                m_m = magnetization(lattice)
                chi_m = chi(lattice, beta)

                m.append(m_m)
                u.append(u_m)
                c.append(chi_m)
            
            if T == 0.1:
                lista.append(lattice.copy())
        
        # Guardamos la última configuración de cada temperatura
        configurations[T] = lattice.copy()

        m_avg = np.mean(m)
        u_avg = np.mean(u)
        chi_avg = np.mean(c)

        results['m'].append(m_avg)
        results['u'].append(u_avg)
        results['chi'].append(chi_avg)

    # 2. GRAFICAS

    print("\n" + "[simulation2] - Graficas")

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("Reprsentación de los valores de m(T), u(T), chi(T)", fontsize=11, fontweight='bold')
    colors = ['purple', 'blue', 'orange']

    for i, obs in enumerate(['m', 'u', 'chi']):
        ax = axes[i]
        ax.plot(results['T'], results[obs], 'o-', label=obs, lw=1.5, markersize=4, color=colors[i])
        ax.set_xlabel('T [K]', fontsize=11, fontweight='bold')
        ax.set_ylabel(f"{obs}/N(T)" if obs == 'chi' else f"{obs}(T)", fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.show()

    # 3. CONFIGURACIONES TÍPICAS

    print("\n" + "[simulation2] - Configuraciones Tipicas")

    num_temps = len(temperatures)
    fig, axes = plt.subplots(2, (num_temps + 1) // 2, figsize=(16, 8), constrained_layout=True)

    if num_temps > 1:
        axes = axes.flatten()
    else:
        axes = [axes]

    fig.suptitle("Configuraciones típicas para distintas temperatutas" + "\n azul: s=+1 | rojo: s=-1")

    for i, (T, lattice) in enumerate(configurations.items()):
        ax = axes[i]
        lattice_muestra = (lattice + 1) / 2
        im = ax.imshow(lattice_muestra, cmap='RdYlBu_r', vmin=0, vmax=1, origin='upper', interpolation='nearest')
        ax.set_title(f"T = {T}", fontsize=11, fontweight='bold', pad=10)
        ax.set_xticks([])
        ax.set_yticks([])
        size = lattice.shape[0]
        for j in range(0, size, 10):
            ax.axhline(y=j-0.5, color='gray', lw=0.5, alpha=0.2)
            ax.axvline(x=j-0.5, color='gray', lw=0.5, alpha=0.2)

    for i in range(num_temps, len(axes)):
        axes[i].axis['off']
    
    plt.show()

    # 4. VIDEO DE EVOLUCION

    print("\n" + "[simulation2] - Video Evolucion")

    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111)
    fig.suptitle('Dirección spin: arriba(1) | abajo(-1)')
    title = ax.set_title('', fontsize=14, fontweight='bold')
    display = (lista[0] + 1) / 2
    im = ax.imshow(display, cmap='RdYlBu_r', vmin=0, vmax=1, origin='upper', interpolation='nearest')
    ax.set_xticks([])
    ax.set_yticks([])

    for j in range(0, 40, 10):
        ax.axhline(y=j-0.5, color='gray', lw=0.5, alpha=0.2)
        ax.axvline(x=j-0.5, color='gray', lw=0.5, alpha=0.2)

    def update_muestra(frame_num):
        lattice = lista[frame_num]
        display = (lattice + 1) / 2
        im.set_array(display)
        title.set_text(f'')

        return [im, title]
    
    anim = FuncAnimation(fig, update_muestra, frames=len(lista), interval=40, blit=True, repeat=True, repeat_delay=2000)

    plt.tight_layout()
    plt.show()

    # FIN

    print("\n" + "[simulation2] - Check")
