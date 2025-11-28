"""
Transition State Optimization Module

This module implements methods for locating and characterizing transition states
(saddle points) on potential energy surfaces using Newton-Raphson optimization.

Theory Background:
    - Badlon, Student Report (2018) - Newton-Raphson saddle point optimization
    - Moss & Coady, J. Chem. Educ. (1983) - TST formulation
    - Eyring, J. Chem. Phys. 3, 107 (1935) - Transition state theory

Key Features:
    - Newton-Raphson saddle point optimization
    - Analytical gradient calculation
    - Numerical Hessian calculation
    - Force constant determination
    - Vibrational frequency analysis

Author: Integration of research papers into educational framework
Date: 2025-11-27
"""

import numpy as np
import pandas as pd
from pathlib import Path


class TransitionStateOptimizer:
    """
    Newton-Raphson optimizer for locating saddle points on PES.

    For triatomic A-B-C systems, optimizes to find the transition state
    where gradient is zero and Hessian has one negative eigenvalue.

    Attributes:
        surface: PES object with leps_potential(R_AB, R_BC, R_AC) method
        tolerance: Convergence tolerance for gradient norm
        max_iterations: Maximum optimization iterations
    """

    def __init__(self, surface, tolerance=1e-6, max_iterations=100):
        """
        Initialize transition state optimizer.

        Parameters:
            surface: PES object with leps_potential method
            tolerance (float): Convergence criterion for |gradient|
            max_iterations (int): Maximum Newton-Raphson iterations
        """
        self.surface = surface
        self.tolerance = tolerance
        self.max_iterations = max_iterations

    def calculate_gradient(self, R_AB, R_BC, delta=0.0001):
        """
        Calculate analytical gradient of LEPS potential.

        For collinear A-B-C geometry: R_AC = R_AB + R_BC

        ∇V = (∂V/∂R_AB, ∂V/∂R_BC)

        Parameters:
            R_AB (float): A-B distance (Angstroms)
            R_BC (float): B-C distance (Angstroms)
            delta (float): Step size for numerical derivatives (Angstroms)

        Returns:
            array: Gradient vector [dV/dR_AB, dV/dR_BC] in kJ/(mol·Angstrom)

        Reference: Badlon (2018) Equations 23-33
        """
        R_AC = R_AB + R_BC  # Collinear geometry

        # Central difference for ∂V/∂R_AB
        V_plus = self.surface.leps_potential(R_AB + delta, R_BC, R_AC + delta)
        V_minus = self.surface.leps_potential(R_AB - delta, R_BC, R_AC - delta)
        dV_dR_AB = (V_plus - V_minus) / (2 * delta)

        # Central difference for ∂V/∂R_BC
        V_plus = self.surface.leps_potential(R_AB, R_BC + delta, R_AC + delta)
        V_minus = self.surface.leps_potential(R_AB, R_BC - delta, R_AC - delta)
        dV_dR_BC = (V_plus - V_minus) / (2 * delta)

        return np.array([dV_dR_AB, dV_dR_BC])

    def calculate_hessian(self, R_AB, R_BC, delta=0.0001):
        """
        Calculate numerical Hessian matrix (second derivatives).

        H = | ∂²V/∂R_AB²      ∂²V/∂R_AB∂R_BC |
            | ∂²V/∂R_AB∂R_BC  ∂²V/∂R_BC²     |

        Parameters:
            R_AB (float): A-B distance (Angstroms)
            R_BC (float): B-C distance (Angstroms)
            delta (float): Step size for numerical derivatives (Angstroms)

        Returns:
            array: 2x2 Hessian matrix in kJ/(mol·Angstrom²)

        Reference: Badlon (2018) Equations 34-36
        """
        R_AC = R_AB + R_BC

        # Calculate ∂²V/∂R_AB² using central difference
        V_plus = self.surface.leps_potential(R_AB + delta, R_BC, R_AC + delta)
        V_center = self.surface.leps_potential(R_AB, R_BC, R_AC)
        V_minus = self.surface.leps_potential(R_AB - delta, R_BC, R_AC - delta)
        d2V_dR_AB2 = (V_plus - 2*V_center + V_minus) / delta**2

        # Calculate ∂²V/∂R_BC² using central difference
        V_plus = self.surface.leps_potential(R_AB, R_BC + delta, R_AC + delta)
        V_center = self.surface.leps_potential(R_AB, R_BC, R_AC)
        V_minus = self.surface.leps_potential(R_AB, R_BC - delta, R_AC - delta)
        d2V_dR_BC2 = (V_plus - 2*V_center + V_minus) / delta**2

        # Calculate ∂²V/∂R_AB∂R_BC using mixed derivative
        V_pp = self.surface.leps_potential(R_AB + delta, R_BC + delta, R_AC + 2*delta)
        V_pm = self.surface.leps_potential(R_AB + delta, R_BC - delta, R_AC)
        V_mp = self.surface.leps_potential(R_AB - delta, R_BC + delta, R_AC)
        V_mm = self.surface.leps_potential(R_AB - delta, R_BC - delta, R_AC - 2*delta)
        d2V_dR_AB_dR_BC = (V_pp - V_pm - V_mp + V_mm) / (4 * delta**2)

        # Construct Hessian matrix
        H = np.array([
            [d2V_dR_AB2, d2V_dR_AB_dR_BC],
            [d2V_dR_AB_dR_BC, d2V_dR_BC2]
        ])

        return H

    def optimize_saddle_point(self, R_AB_init, R_BC_init, verbose=True):
        """
        Find saddle point using Newton-Raphson optimization.

        Newton-Raphson iteration:
        R_new = R_old - H⁻¹ · ∇V

        where H is the Hessian and ∇V is the gradient.

        Parameters:
            R_AB_init (float): Initial guess for R_AB (Angstroms)
            R_BC_init (float): Initial guess for R_BC (Angstroms)
            verbose (bool): Print iteration details

        Returns:
            dict: Optimization results with keys:
                - 'R_AB': Optimized R_AB (Angstroms)
                - 'R_BC': Optimized R_BC (Angstroms)
                - 'R_AC': Optimized R_AC (Angstroms)
                - 'energy': Energy at saddle point (kJ/mol)
                - 'gradient': Final gradient vector
                - 'hessian': Final Hessian matrix
                - 'eigenvalues': Hessian eigenvalues
                - 'eigenvectors': Hessian eigenvectors
                - 'iterations': Number of iterations
                - 'converged': Whether optimization converged
                - 'history': DataFrame of iteration history

        Reference: Badlon (2018) Table 1 - Newton-Raphson iterations
        """
        # Initialize
        R_AB = R_AB_init
        R_BC = R_BC_init
        converged = False

        # History tracking
        history = []

        if verbose:
            print("Newton-Raphson Saddle Point Optimization")
            print("=" * 60)
            print(f"{'Iter':>4} {'R_AB':>10} {'R_BC':>10} {'Energy':>12} {'|Gradient|':>12}")
            print("-" * 60)

        for iteration in range(self.max_iterations):
            # Calculate gradient and Hessian
            grad = self.calculate_gradient(R_AB, R_BC)
            H = self.calculate_hessian(R_AB, R_BC)

            # Calculate energy
            R_AC = R_AB + R_BC
            energy = self.surface.leps_potential(R_AB, R_BC, R_AC)

            # Calculate gradient norm
            grad_norm = np.linalg.norm(grad)

            # Store history
            history.append({
                'iteration': iteration,
                'R_AB': R_AB,
                'R_BC': R_BC,
                'R_AC': R_AC,
                'energy': energy,
                'gradient_norm': grad_norm,
                'dV_dR_AB': grad[0],
                'dV_dR_BC': grad[1]
            })

            if verbose:
                print(f"{iteration:4d} {R_AB:10.6f} {R_BC:10.6f} {energy:12.4f} {grad_norm:12.8f}")

            # Check convergence
            if grad_norm < self.tolerance:
                converged = True
                if verbose:
                    print("-" * 60)
                    print(f"Converged in {iteration} iterations!")
                break

            # Newton-Raphson step: R_new = R_old - H⁻¹ · grad
            try:
                H_inv = np.linalg.inv(H)
                delta_R = -H_inv @ grad

                # Update coordinates
                R_AB += delta_R[0]
                R_BC += delta_R[1]

            except np.linalg.LinAlgError:
                if verbose:
                    print("Warning: Hessian is singular, using gradient descent instead")
                # Fall back to gradient descent
                alpha = 0.01  # Step size
                R_AB -= alpha * grad[0]
                R_BC -= alpha * grad[1]

        # Final calculations
        final_grad = self.calculate_gradient(R_AB, R_BC)
        final_H = self.calculate_hessian(R_AB, R_BC)
        R_AC = R_AB + R_BC
        final_energy = self.surface.leps_potential(R_AB, R_BC, R_AC)

        # Eigenanalysis of Hessian
        eigenvalues, eigenvectors = np.linalg.eig(final_H)

        if verbose:
            print(f"\nFinal Results:")
            print(f"  R_AB = {R_AB:.6f} Å")
            print(f"  R_BC = {R_BC:.6f} Å")
            print(f"  R_AC = {R_AC:.6f} Å")
            print(f"  Energy = {final_energy:.4f} kJ/mol")
            print(f"  |Gradient| = {np.linalg.norm(final_grad):.8f}")
            print(f"  Hessian eigenvalues: {eigenvalues}")
            if eigenvalues[0] < 0 and eigenvalues[1] > 0:
                print("  [OK] Confirmed saddle point (one negative eigenvalue)")
            elif eigenvalues[0] < 0 and eigenvalues[1] < 0:
                print("  [X] Maximum (two negative eigenvalues)")
            else:
                print("  [X] Minimum (no negative eigenvalues)")

        return {
            'R_AB': R_AB,
            'R_BC': R_BC,
            'R_AC': R_AC,
            'energy': final_energy,
            'gradient': final_grad,
            'hessian': final_H,
            'eigenvalues': eigenvalues,
            'eigenvectors': eigenvectors,
            'iterations': iteration + 1,
            'converged': converged,
            'history': pd.DataFrame(history)
        }

    def calculate_force_constants(self, R_AB, R_BC, n_points=7, delta_R=0.1):
        """
        Calculate force constants by sectioning the PES.

        Force constant k = ∂²V/∂R²

        Parameters:
            R_AB (float): A-B distance at saddle point (Angstroms)
            R_BC (float): B-C distance at saddle point (Angstroms)
            n_points (int): Number of points for sectioning (odd number)
            delta_R (float): Total range for sectioning (Angstroms)

        Returns:
            dict: Force constants and fitted parameters
                - 'k_AB': Force constant along R_AB (kJ/(mol·Angstrom²))
                - 'k_BC': Force constant along R_BC (kJ/(mol·Angstrom²))
                - 'sections_AB': DataFrame of R_AB section energies
                - 'sections_BC': DataFrame of R_BC section energies

        Reference: Badlon (2018) Tables 5-6 - PES sectioning
        """
        R_AC = R_AB + R_BC

        # Section along R_AB (holding R_BC constant)
        R_AB_range = np.linspace(R_AB - delta_R/2, R_AB + delta_R/2, n_points)
        V_section_AB = []

        for R_AB_i in R_AB_range:
            R_AC_i = R_AB_i + R_BC
            V_i = self.surface.leps_potential(R_AB_i, R_BC, R_AC_i)
            V_section_AB.append(V_i)

        V_section_AB = np.array(V_section_AB)

        # Fit parabola: V = a + b*R + c*R²
        # Force constant k = 2*c
        coeffs_AB = np.polyfit(R_AB_range - R_AB, V_section_AB - V_section_AB[n_points//2], 2)
        k_AB = 2 * coeffs_AB[0]

        # Section along R_BC (holding R_AB constant)
        R_BC_range = np.linspace(R_BC - delta_R/2, R_BC + delta_R/2, n_points)
        V_section_BC = []

        for R_BC_i in R_BC_range:
            R_AC_i = R_AB + R_BC_i
            V_i = self.surface.leps_potential(R_AB, R_BC_i, R_AC_i)
            V_section_BC.append(V_i)

        V_section_BC = np.array(V_section_BC)

        # Fit parabola
        coeffs_BC = np.polyfit(R_BC_range - R_BC, V_section_BC - V_section_BC[n_points//2], 2)
        k_BC = 2 * coeffs_BC[0]

        # Create DataFrames
        sections_AB = pd.DataFrame({
            'R_AB': R_AB_range,
            'V': V_section_AB
        })

        sections_BC = pd.DataFrame({
            'R_BC': R_BC_range,
            'V': V_section_BC
        })

        return {
            'k_AB': k_AB,
            'k_BC': k_BC,
            'sections_AB': sections_AB,
            'sections_BC': sections_BC
        }

    def calculate_vibrational_frequencies(self, k_AB, k_BC, m_A, m_B, m_C):
        """
        Calculate vibrational frequencies from force constants.

        ω = √(k/μ) where μ is the reduced mass

        Parameters:
            k_AB (float): Force constant along R_AB (kJ/(mol·Angstrom²))
            k_BC (float): Force constant along R_BC (kJ/(mol·Angstrom²))
            m_A, m_B, m_C (float): Atomic masses (amu)

        Returns:
            dict: Vibrational frequencies
                - 'omega_AB': Frequency along R_AB (cm⁻¹)
                - 'omega_BC': Frequency along R_BC (cm⁻¹)

        Reference: Badlon (2018) Equations 45-50
        """
        # Reduced masses
        mu_AB = (m_A * m_B) / (m_A + m_B)
        mu_BC = (m_B * m_C) / (m_B + m_C)

        # Convert force constant to SI units and calculate frequency
        # k in kJ/(mol·Å²) → N/m
        # 1 kJ/(mol·Å²) = 1.6605e3 N/m
        k_AB_SI = k_AB * 1.6605e3
        k_BC_SI = k_BC * 1.6605e3

        # μ in amu → kg
        mu_AB_SI = mu_AB * 1.66054e-27
        mu_BC_SI = mu_BC * 1.66054e-27

        # ω = √(k/μ) in rad/s
        omega_AB_rad = np.sqrt(k_AB_SI / mu_AB_SI)
        omega_BC_rad = np.sqrt(k_BC_SI / mu_BC_SI)

        # Convert to cm⁻¹: ω(cm⁻¹) = ω(rad/s) / (2πc) where c = 2.998e10 cm/s
        c_cm = 2.998e10  # speed of light in cm/s
        omega_AB_cm = omega_AB_rad / (2 * np.pi * c_cm)
        omega_BC_cm = omega_BC_rad / (2 * np.pi * c_cm)

        return {
            'omega_AB': omega_AB_cm,
            'omega_BC': omega_BC_cm
        }


def example_usage():
    """Example: Find H + HI transition state."""
    from leps_surface import LEPSSurface

    # Create LEPS surface with K_sato = 0.0
    surface = LEPSSurface('HI', 'HI', 'I2', K_sato=0.0)

    # Create optimizer
    optimizer = TransitionStateOptimizer(surface, tolerance=1e-6, max_iterations=50)

    # Initial guess (from Badlon 2018 - approximately 1.9, 1.9 Angstroms)
    R_AB_init = 1.9
    R_BC_init = 1.9

    print("Finding transition state for H + HI -> HI + H reaction\n")

    # Optimize to find saddle point
    result = optimizer.optimize_saddle_point(R_AB_init, R_BC_init, verbose=True)

    # Calculate force constants
    print("\n" + "=" * 60)
    print("Force Constant Analysis")
    print("=" * 60)

    force_constants = optimizer.calculate_force_constants(
        result['R_AB'], result['R_BC'],
        n_points=7, delta_R=0.2
    )

    print(f"Force constant k_AB = {force_constants['k_AB']:.4f} kJ/(mol·Å²)")
    print(f"Force constant k_BC = {force_constants['k_BC']:.4f} kJ/(mol·Å²)")

    # Calculate vibrational frequencies
    m_H = 1.00783  # amu
    m_I = 126.90   # amu

    frequencies = optimizer.calculate_vibrational_frequencies(
        force_constants['k_AB'], force_constants['k_BC'],
        m_H, m_H, m_I
    )

    print(f"\nVibrational frequencies:")
    print(f"  omega_AB = {frequencies['omega_AB']:.2f} cm^-1")
    print(f"  omega_BC = {frequencies['omega_BC']:.2f} cm^-1")


if __name__ == "__main__":
    example_usage()
