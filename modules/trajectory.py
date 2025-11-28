"""
Classical Trajectory Calculation Module

This module implements quasiclassical trajectory (QCT) methods for
triatomic A + BC → AB + C reactions using numerical integration of
Newton's equations of motion on potential energy surfaces.

Theory Background:
    - Garcia et al., J. Chem. Educ. (2000) - Li + HF trajectory tutorial
    - Badlon, Student Report (2018) - H + HI trajectory calculations
    - Hase et al., VENUS96 - Classical trajectory program structure

Key Features:
    - Velocity Verlet integration algorithm
    - Energy conservation monitoring
    - Multiple trajectory batch calculations
    - Outcome analysis (reactive vs non-reactive)

Author: Integration of research papers into educational framework
Date: 2025-11-27
"""

import numpy as np
import pandas as pd
from pathlib import Path


class ClassicalTrajectory:
    """
    Classical trajectory calculator for triatomic A-B-C systems.

    Uses numerical integration to solve Newton's equations of motion
    on a given potential energy surface.

    Attributes:
        surface: PES object with leps_potential(R_AB, R_BC, R_AC) method
        masses: Dictionary of atomic masses (amu)
        dt: Integration time step (femtoseconds)
    """

    # Atomic masses (amu) - NIST values
    ATOMIC_MASSES = {
        'H': 1.00783,
        'D': 2.01410,
        'T': 3.01605,
        'He': 4.00260,
        'Li': 6.941,
        'C': 12.011,
        'N': 14.007,
        'O': 15.999,
        'F': 18.998,
        'Cl': 35.45,
        'Br': 79.904,
        'I': 126.90
    }

    # Unit conversions
    AMU_TO_KG = 1.66054e-27  # kg
    ANGSTROM_TO_M = 1e-10    # m
    KJ_MOL_TO_J = 1000 / 6.022e23  # J
    FS_TO_S = 1e-15          # s

    def __init__(self, surface, atom_A, atom_B, atom_C, dt=0.010):
        """
        Initialize trajectory calculator.

        Parameters:
            surface: PES object with leps_potential(R_AB, R_BC, R_AC) method
            atom_A (str): Symbol for atom A
            atom_B (str): Symbol for atom B
            atom_C (str): Symbol for atom C
            dt (float): Time step in femtoseconds (default 0.010 fs)

        Reference: Garcia et al. (2000) - optimal dt = 0.010 fs
        """
        self.surface = surface
        self.atom_A = atom_A
        self.atom_B = atom_B
        self.atom_C = atom_C
        self.dt = dt  # femtoseconds

        # Get atomic masses
        self.m_A = self.ATOMIC_MASSES[atom_A]
        self.m_B = self.ATOMIC_MASSES[atom_B]
        self.m_C = self.ATOMIC_MASSES[atom_C]

        # Total mass (for center of mass)
        self.M_total = self.m_A + self.m_B + self.m_C

    def calculate_forces(self, R_AB, R_BC, R_AC, delta=0.001):
        """
        Calculate forces from potential energy surface using numerical gradients.

        F = -dV/dR

        Parameters:
            R_AB (float): A-B distance (Angstroms)
            R_BC (float): B-C distance (Angstroms)
            R_AC (float): A-C distance (Angstroms)
            delta (float): Step size for numerical derivative (Angstroms)

        Returns:
            tuple: (F_AB, F_BC, F_AC) forces in kJ/(mol·Angstrom)

        Reference: Badlon (2018) Equations 23-33 for analytical gradients
        Note: Using numerical gradients here for generality
        """
        # Central difference for F_AB = -dV/dR_AB
        V_plus = self.surface.leps_potential(R_AB + delta, R_BC, R_AC)
        V_minus = self.surface.leps_potential(R_AB - delta, R_BC, R_AC)
        F_AB = -(V_plus - V_minus) / (2 * delta)

        # Central difference for F_BC = -dV/dR_BC
        V_plus = self.surface.leps_potential(R_AB, R_BC + delta, R_AC)
        V_minus = self.surface.leps_potential(R_AB, R_BC - delta, R_AC)
        F_BC = -(V_plus - V_minus) / (2 * delta)

        # Central difference for F_AC = -dV/dR_AC
        V_plus = self.surface.leps_potential(R_AB, R_BC, R_AC + delta)
        V_minus = self.surface.leps_potential(R_AB, R_BC, R_AC - delta)
        F_AC = -(V_plus - V_minus) / (2 * delta)

        return F_AB, F_BC, F_AC

    def velocity_verlet_step(self, R_AB, R_BC, R_AC, v_AB, v_BC, v_AC):
        """
        Single step of Velocity Verlet integration algorithm.

        The Velocity Verlet algorithm is symplectic and conserves energy well:
        1. R(t+dt) = R(t) + v(t)*dt + 0.5*a(t)*dt²
        2. a(t+dt) = F(R(t+dt))/m
        3. v(t+dt) = v(t) + 0.5*(a(t) + a(t+dt))*dt

        Parameters:
            R_AB, R_BC, R_AC (float): Current distances (Angstroms)
            v_AB, v_BC, v_AC (float): Current velocities (Angstroms/fs)

        Returns:
            tuple: (R_AB_new, R_BC_new, R_AC_new, v_AB_new, v_BC_new, v_AC_new)

        Reference:
            - Verlet, Phys. Rev. 159, 98 (1967)
            - Swope et al., J. Chem. Phys. 76, 637 (1982)
        """
        # Calculate current accelerations
        F_AB, F_BC, F_AC = self.calculate_forces(R_AB, R_BC, R_AC)

        # Convert forces to accelerations (need to account for reduced masses)
        # For simplicity, treating each coordinate independently
        # More rigorous treatment would use Jacobi or mass-weighted coordinates
        mu_AB = (self.m_A * self.m_B) / (self.m_A + self.m_B)
        mu_BC = (self.m_B * self.m_C) / (self.m_B + self.m_C)
        mu_AC = (self.m_A * self.m_C) / (self.m_A + self.m_C)

        # Convert F (kJ/mol/Angstrom) to acceleration (Angstrom/fs²)
        # F/m = (kJ/mol/Å) / (amu) → Å/fs²
        # Conversion: kJ/mol = 1000/NA J, amu = 1.66e-27 kg
        # 1 kJ/mol/Å / 1 amu = 1.0364e-4 Å/fs²
        conversion = 1.0364e-4  # (kJ/mol/Å) / amu → Å/fs²

        a_AB = F_AB / mu_AB * conversion
        a_BC = F_BC / mu_BC * conversion
        a_AC = F_AC / mu_AC * conversion

        # Update positions: R(t+dt) = R(t) + v(t)*dt + 0.5*a(t)*dt²
        R_AB_new = R_AB + v_AB * self.dt + 0.5 * a_AB * self.dt**2
        R_BC_new = R_BC + v_BC * self.dt + 0.5 * a_BC * self.dt**2
        R_AC_new = R_AC + v_AC * self.dt + 0.5 * a_AC * self.dt**2

        # Calculate new accelerations at new positions
        F_AB_new, F_BC_new, F_AC_new = self.calculate_forces(R_AB_new, R_BC_new, R_AC_new)
        a_AB_new = F_AB_new / mu_AB * conversion
        a_BC_new = F_BC_new / mu_BC * conversion
        a_AC_new = F_AC_new / mu_AC * conversion

        # Update velocities: v(t+dt) = v(t) + 0.5*(a(t) + a(t+dt))*dt
        v_AB_new = v_AB + 0.5 * (a_AB + a_AB_new) * self.dt
        v_BC_new = v_BC + 0.5 * (a_BC + a_BC_new) * self.dt
        v_AC_new = v_AC + 0.5 * (a_AC + a_AC_new) * self.dt

        return R_AB_new, R_BC_new, R_AC_new, v_AB_new, v_BC_new, v_AC_new

    def calculate_kinetic_energy(self, v_AB, v_BC, v_AC):
        """
        Calculate kinetic energy from velocities.

        T = 0.5 * m * v²

        Parameters:
            v_AB, v_BC, v_AC (float): Velocities (Angstroms/fs)

        Returns:
            float: Kinetic energy (kJ/mol)
        """
        mu_AB = (self.m_A * self.m_B) / (self.m_A + self.m_B)
        mu_BC = (self.m_B * self.m_C) / (self.m_B + self.m_C)
        mu_AC = (self.m_A * self.m_C) / (self.m_A + self.m_C)

        # KE in amu*(Angstrom/fs)² → kJ/mol
        # 1 amu*(Å/fs)² = 9646.9 kJ/mol
        conversion = 9646.9

        T = 0.5 * (mu_AB * v_AB**2 + mu_BC * v_BC**2 + mu_AC * v_AC**2) * conversion

        return T

    def run_trajectory(self, R_AB_0, R_BC_0, R_AC_0, v_AB_0, v_BC_0, v_AC_0,
                      max_time=1000.0, save_interval=1):
        """
        Run a single classical trajectory.

        Parameters:
            R_AB_0, R_BC_0, R_AC_0 (float): Initial distances (Angstroms)
            v_AB_0, v_BC_0, v_AC_0 (float): Initial velocities (Angstroms/fs)
            max_time (float): Maximum simulation time (femtoseconds)
            save_interval (int): Save every Nth step

        Returns:
            dict: Trajectory data with keys:
                - 'time': Time array (fs)
                - 'R_AB', 'R_BC', 'R_AC': Distance arrays (Angstroms)
                - 'v_AB', 'v_BC', 'v_AC': Velocity arrays (Angstroms/fs)
                - 'V': Potential energy array (kJ/mol)
                - 'T': Kinetic energy array (kJ/mol)
                - 'E_total': Total energy array (kJ/mol)
                - 'outcome': 'reactive', 'non-reactive', or 'incomplete'

        Reference: Garcia et al. (2000) VENUS96 trajectory workflow
        """
        # Initialize arrays
        n_steps = int(max_time / self.dt)
        n_save = n_steps // save_interval + 1

        time = np.zeros(n_save)
        R_AB = np.zeros(n_save)
        R_BC = np.zeros(n_save)
        R_AC = np.zeros(n_save)
        v_AB = np.zeros(n_save)
        v_BC = np.zeros(n_save)
        v_AC = np.zeros(n_save)
        V = np.zeros(n_save)
        T = np.zeros(n_save)

        # Set initial conditions
        R_AB[0] = R_AB_0
        R_BC[0] = R_BC_0
        R_AC[0] = R_AC_0
        v_AB[0] = v_AB_0
        v_BC[0] = v_BC_0
        v_AC[0] = v_AC_0
        V[0] = self.surface.leps_potential(R_AB_0, R_BC_0, R_AC_0)
        T[0] = self.calculate_kinetic_energy(v_AB_0, v_BC_0, v_AC_0)

        # Integration loop
        save_idx = 1
        for step in range(1, n_steps):
            # Velocity Verlet step
            R_AB_new, R_BC_new, R_AC_new, v_AB_new, v_BC_new, v_AC_new = \
                self.velocity_verlet_step(
                    R_AB[save_idx-1], R_BC[save_idx-1], R_AC[save_idx-1],
                    v_AB[save_idx-1], v_BC[save_idx-1], v_AC[save_idx-1]
                )

            # Save at intervals
            if step % save_interval == 0:
                time[save_idx] = step * self.dt
                R_AB[save_idx] = R_AB_new
                R_BC[save_idx] = R_BC_new
                R_AC[save_idx] = R_AC_new
                v_AB[save_idx] = v_AB_new
                v_BC[save_idx] = v_BC_new
                v_AC[save_idx] = v_AC_new
                V[save_idx] = self.surface.leps_potential(R_AB_new, R_BC_new, R_AC_new)
                T[save_idx] = self.calculate_kinetic_energy(v_AB_new, v_BC_new, v_AC_new)

                save_idx += 1

                # Check for completion (molecule dissociation)
                if R_AB_new > 10.0 or R_BC_new > 10.0 or R_AC_new > 10.0:
                    break

        # Trim arrays to actual size
        time = time[:save_idx]
        R_AB = R_AB[:save_idx]
        R_BC = R_BC[:save_idx]
        R_AC = R_AC[:save_idx]
        v_AB = v_AB[:save_idx]
        v_BC = v_BC[:save_idx]
        v_AC = v_AC[:save_idx]
        V = V[:save_idx]
        T = T[:save_idx]

        # Total energy
        E_total = V + T

        # Determine outcome
        outcome = self._determine_outcome(R_AB, R_BC, R_AC)

        return {
            'time': time,
            'R_AB': R_AB,
            'R_BC': R_BC,
            'R_AC': R_AC,
            'v_AB': v_AB,
            'v_BC': v_BC,
            'v_AC': v_AC,
            'V': V,
            'T': T,
            'E_total': E_total,
            'outcome': outcome,
            'energy_drift': (E_total[-1] - E_total[0]) / E_total[0] * 100  # percent
        }

    def _determine_outcome(self, R_AB, R_BC, R_AC, threshold=6.0):
        """
        Determine if trajectory is reactive or non-reactive.

        For A + BC → AB + C:
        - Reactive: R_BC > threshold and R_AB < threshold (AB formed)
        - Non-reactive: R_BC < threshold (BC remains)

        Parameters:
            R_AB, R_BC, R_AC (array): Distance trajectories
            threshold (float): Distance threshold for "dissociated" (Angstroms)

        Returns:
            str: 'reactive', 'non-reactive', or 'incomplete'
        """
        final_R_AB = R_AB[-1]
        final_R_BC = R_BC[-1]

        if final_R_BC > threshold and final_R_AB < threshold:
            return 'reactive'
        elif final_R_AB > threshold and final_R_BC < threshold:
            return 'non-reactive'
        else:
            return 'incomplete'


def example_usage():
    """Example: Run H + HI trajectory."""
    from leps_surface import LEPSSurface

    # Create LEPS surface
    surface = LEPSSurface('HI', 'HI', 'I2', K_sato=0.0)

    # Create trajectory calculator
    traj_calc = ClassicalTrajectory(surface, 'H', 'H', 'I', dt=0.010)

    # Initial conditions: H approaching HI
    R_AB_0 = 3.0    # H...H distance (Angstroms)
    R_BC_0 = 1.609  # H-I equilibrium distance (Angstroms)
    R_AC_0 = R_AB_0 + R_BC_0  # Collinear

    # Initial velocities (H approaching with thermal energy ~50 kJ/mol)
    v_AB_0 = -0.05   # H moving toward HI (Angstrom/fs)
    v_BC_0 = 0.0
    v_AC_0 = -0.05

    print("Running trajectory...")
    print(f"Initial conditions: R_AB={R_AB_0:.2f} Å, R_BC={R_BC_0:.2f} Å, R_AC={R_AC_0:.2f} Å")
    print(f"Initial velocity: v_AB={v_AB_0:.3f} Å/fs")

    # Run trajectory
    result = traj_calc.run_trajectory(R_AB_0, R_BC_0, R_AC_0,
                                     v_AB_0, v_BC_0, v_AC_0,
                                     max_time=500.0, save_interval=10)

    print(f"\nTrajectory completed:")
    print(f"  Duration: {result['time'][-1]:.2f} fs")
    print(f"  Outcome: {result['outcome']}")
    print(f"  Energy drift: {result['energy_drift']:.4f}%")
    print(f"  Initial energy: {result['E_total'][0]:.2f} kJ/mol")
    print(f"  Final energy: {result['E_total'][-1]:.2f} kJ/mol")


if __name__ == "__main__":
    example_usage()
