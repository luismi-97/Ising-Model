# Ising-Model

## Overview

This project implements Monte Carlo simulations of the 2D Ising Model on
a 40×40 lattice, exploring phase transitions and equilibrium properties
using two different Monte Carlo dynamics: Metropolis and Glauber
algorithms. The simulation investigates the temperature-dependent
behavior of magnetization, energy, and magnetic susceptibility.

## Part 1: External Field Case (h = 1, J = 0)

### Part 1A: Thermal Equilibrium Comparison (function: `simulation()`)

This section performs Monte Carlo simulations for a non-interacting
Ising system under an external magnetic field.

#### Setup

-   Lattice size: 40 × 40 spins
-   External field: h = 1
-   Coupling constant: J = 0 (no spin-spin interactions)
-   Temperatures: T = {0.1, 1.0, 2.0, 2.27, 3.0, 4.0}
-   Monte Carlo steps: 1000
-   Measurement interval: Every 50 steps

#### Methodology

The simulation runs both Metropolis and Glauber dynamics independently
for each temperature.

1.  Initialize a random spin configuration
2.  Apply Monte Carlo algorithm for 1000 steps
3.  Record energy (u), magnetization (m), and susceptibility (χ) every
    50 steps
4.  Average observables over the measurement period

#### Results

-   Magnetization m(T): Average magnetic moment per spin
-   Energy u(T): Average energy per spin
-   Susceptibility χ(T): Magnetic response to field changes

### Part 1B: Relaxation Curves (function: `relax_curve()`)

This section studies how the system relaxes from a fully ordered state
to thermal equilibrium.

#### Setup

-   Initial state: all spins +1
-   Temperatures: T = {0.1, 2.27, 4.0}
-   Monte Carlo steps: 100
-   Realizations: 100

#### Methodology

1.  Initialize all spins up
2.  Apply Monte Carlo dynamics
3.  Record magnetization per step
4.  Repeat 100 times
5.  Average results

## Part 2: Ferromagnetic Case (h = 0, J = 1)

### Energy Change for Spin Flip

ΔE = 2 s_i (J Σ_nn s_j + h)

#### Setup

-   Lattice size: 40 × 40
-   J = 1
-   h = 0
-   Temperatures: same as above
-   Steps: 1000

#### Results

-   Clear phase transition around T ≈ 2.27
-   Magnetization drops to zero above Tc
-   Susceptibility peaks at Tc

## Project Structure

main.py\
parte1.py\
parte2.py\
model.py\
dinamicas.py\
observables.py

## Summary

The project demonstrates: - Agreement between simulation and theory -
Same equilibrium from different dynamics - Phase transition in
ferromagnetic system
