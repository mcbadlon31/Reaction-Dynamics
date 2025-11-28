"""
LEPS (London-Eyring-Polanyi-Sato) Potential Energy Surface Module

This module implements the LEPS method for constructing potential energy surfaces
for triatomic systems (A + B-C → A-B + C).

Theory Background:
    - Moss & Coady, J. Chem. Educ. (1983) 60(6), 455-461
    - Badlon, Student Report (2018) - Complete H+HI calculation workflow
    - Ochoa de Aspuru & Hernandez, Tutorial on Fitting of PES (2000)

Author: Integration of research papers into educational framework
Date: 2025-11-27
"""

import numpy as np
import pandas as pd
from pathlib import Path

class LEPSSurface:
    """
    LEPS potential energy surface for triatomic A-B-C systems.

    The LEPS method combines Morse and anti-Morse functions for diatomic
    pairs with the London equation and Sato modification.

    Attributes:
        params (dict): Morse parameters for each diatomic pair
        K_sato (float): Sato parameter for the triatomic interaction
    """

    def __init__(self, molecule_AB, molecule_BC, molecule_AC, K_sato=0.0):
        """
        Initialize LEPS surface with molecular parameters.

        Parameters:
            molecule_AB (str): Name of AB diatomic (e.g., 'HI')
            molecule_BC (str): Name of BC diatomic (e.g., 'I2')
            molecule_AC (str): Name of AC diatomic (e.g., 'HI')
            K_sato (float): Sato parameter (default 0.0 for pure London equation)
        """
        self.molecule_AB = molecule_AB
        self.molecule_BC = molecule_BC
        self.molecule_AC = molecule_AC
        self.K_sato = K_sato

        # Load Morse parameters from CSV file
        self.params = self._load_parameters()

    def _load_parameters(self):
        """Load Morse parameters from data file."""
        # Get path to data file
        data_path = Path(__file__).parent.parent / 'data' / 'tst' / 'morse_parameters.csv'
        df = pd.read_csv(data_path)

        # Extract parameters for the three diatomics
        params = {}
        for molecule_name, pair_name in [(self.molecule_AB, 'AB'),
                                          (self.molecule_BC, 'BC'),
                                          (self.molecule_AC, 'AC')]:
            row = df[df['molecule'] == molecule_name]
            if len(row) == 0:
                raise ValueError(f"Molecule {molecule_name} not found in parameters file")

            params[pair_name] = {
                'D_e': row['D_e_kJ_mol'].values[0],
                'R_e': row['R_e_angstrom'].values[0],
                'beta': row['beta_inv_angstrom'].values[0]
            }

        return params

    def morse_potential(self, R, D_e, R_e, beta):
        """
        Morse potential for attractive diatomic interaction.

        V(R) = D_e * [exp(-2β(R-Re)) - 2exp(-β(R-Re))]

        Parameters:
            R (float or array): Internuclear distance (Angstroms)
            D_e (float): Dissociation energy (kJ/mol)
            R_e (float): Equilibrium distance (Angstroms)
            beta (float): Morse parameter (1/Angstroms)

        Returns:
            float or array: Morse potential energy (kJ/mol)

        Reference: Morse, Phys. Rev. 34, 57 (1929)
        """
        x = beta * (R - R_e)
        return D_e * (np.exp(-2*x) - 2*np.exp(-x))

    def anti_morse_potential(self, R, D_e, R_e, beta):
        """
        Anti-Morse potential for repulsive diatomic interaction.

        V(R) = (D_e/2) * [exp(-2β(R-Re)) + 2exp(-β(R-Re))]

        Parameters:
            R (float or array): Internuclear distance (Angstroms)
            D_e (float): Dissociation energy (kJ/mol)
            R_e (float): Equilibrium distance (Angstroms)
            beta (float): Morse parameter (1/Angstroms)

        Returns:
            float or array: Anti-Morse potential energy (kJ/mol)
        """
        x = beta * (R - R_e)
        return 0.5 * D_e * (np.exp(-2*x) + 2*np.exp(-x))

    def coulomb_integral(self, R, D_e, R_e, beta, K):
        """
        Coulomb integral Q for LEPS formulation.

        Q = (D/4) * [(3+K)exp(-2β(R-Re)) - (2+6K)exp(-β(R-Re))]

        Parameters:
            R (float): Internuclear distance
            D_e (float): Dissociation energy
            R_e (float): Equilibrium distance
            beta (float): Morse parameter
            K (float): Sato parameter

        Returns:
            float: Coulomb integral value

        Reference: Badlon (2018) Equations 22-23
        """
        x = beta * (R - R_e)
        return 0.25 * D_e * ((3 + K) * np.exp(-2*x) - (2 + 6*K) * np.exp(-x))

    def exchange_integral(self, R, D_e, R_e, beta, K):
        """
        Exchange integral J for LEPS formulation.

        J = (D/4) * [(1+3K)exp(-2β(R-Re)) - (6+2K)exp(-β(R-Re))]

        Parameters:
            R (float): Internuclear distance
            D_e (float): Dissociation energy
            R_e (float): Equilibrium distance
            beta (float): Morse parameter
            K (float): Sato parameter

        Returns:
            float: Exchange integral value

        Reference: Badlon (2018) Equations 22-23
        """
        x = beta * (R - R_e)
        return 0.25 * D_e * ((1 + 3*K) * np.exp(-2*x) - (6 + 2*K) * np.exp(-x))

    def leps_potential(self, R_AB, R_BC, R_AC):
        """
        Calculate LEPS potential energy for triatomic system.

        The LEPS potential uses the London equation with Sato modification:
        V_LEPS = Q_AB + Q_BC + Q_AC - sqrt(α²_AB + α²_BC + α²_AC) / (1 + K)

        where α_ij = (J_ij - J_jk), and the division by (1+K) is the Sato modification.

        Parameters:
            R_AB (float): A-B distance (Angstroms)
            R_BC (float): B-C distance (Angstroms)
            R_AC (float): A-C distance (Angstroms)

        Returns:
            float: LEPS potential energy (kJ/mol)

        Reference:
            - London, Z. Elektrochem. 35, 552 (1929)
            - Eyring & Polanyi, Z. Phys. Chem. Abt. B 12, 279 (1931)
            - Sato, J. Chem. Phys. 23, 592 (1955)
        """
        # Get parameters for each pair
        p_AB = self.params['AB']
        p_BC = self.params['BC']
        p_AC = self.params['AC']

        # Calculate Coulomb integrals Q
        Q_AB = self.coulomb_integral(R_AB, p_AB['D_e'], p_AB['R_e'], p_AB['beta'], self.K_sato)
        Q_BC = self.coulomb_integral(R_BC, p_BC['D_e'], p_BC['R_e'], p_BC['beta'], self.K_sato)
        Q_AC = self.coulomb_integral(R_AC, p_AC['D_e'], p_AC['R_e'], p_AC['beta'], self.K_sato)

        # Calculate exchange integrals J
        J_AB = self.exchange_integral(R_AB, p_AB['D_e'], p_AB['R_e'], p_AB['beta'], self.K_sato)
        J_BC = self.exchange_integral(R_BC, p_BC['D_e'], p_BC['R_e'], p_BC['beta'], self.K_sato)
        J_AC = self.exchange_integral(R_AC, p_AC['D_e'], p_AC['R_e'], p_AC['beta'], self.K_sato)

        # London equation with Sato modification
        V_london = Q_AB + Q_BC + Q_AC - np.sqrt(
            0.5 * ((J_AB - J_BC)**2 + (J_BC - J_AC)**2 + (J_AC - J_AB)**2)
        )

        V_sato = V_london / (1 + self.K_sato)

        return V_sato

    def energy_surface_2d(self, R_AB_range, R_BC_range, R_AC_fixed=None, angle_deg=None):
        """
        Calculate 2D potential energy surface.

        Parameters:
            R_AB_range (array): Array of A-B distances
            R_BC_range (array): Array of B-C distances
            R_AC_fixed (float, optional): Fixed A-C distance (for 2D slice)
            angle_deg (float, optional): ABC angle in degrees (alternative to R_AC_fixed)

        Returns:
            tuple: (R_AB_grid, R_BC_grid, V_grid) meshgrids of coordinates and energies
        """
        R_AB_grid, R_BC_grid = np.meshgrid(R_AB_range, R_BC_range)
        V_grid = np.zeros_like(R_AB_grid)

        for i in range(len(R_BC_range)):
            for j in range(len(R_AB_range)):
                if R_AC_fixed is not None:
                    R_AC = R_AC_fixed
                elif angle_deg is not None:
                    # Law of cosines: R_AC² = R_AB² + R_BC² - 2*R_AB*R_BC*cos(angle)
                    angle_rad = np.radians(angle_deg)
                    R_AC = np.sqrt(R_AB_grid[i,j]**2 + R_BC_grid[i,j]**2
                                   - 2*R_AB_grid[i,j]*R_BC_grid[i,j]*np.cos(angle_rad))
                else:
                    raise ValueError("Either R_AC_fixed or angle_deg must be specified")

                V_grid[i,j] = self.leps_potential(R_AB_grid[i,j], R_BC_grid[i,j], R_AC)

        return R_AB_grid, R_BC_grid, V_grid


def example_usage():
    """Example: Create LEPS surface for H + HI → HI + H reaction."""
    # Create LEPS surface with default K_sato = 0.0 (pure London equation)
    surface = LEPSSurface('HI', 'HI', 'I2', K_sato=0.0)

    # Calculate energy at a single geometry
    E = surface.leps_potential(R_AB=1.6, R_BC=2.5, R_AC=3.0)
    print(f"Energy at (1.6, 2.5, 3.0) Å: {E:.2f} kJ/mol")

    # Create 2D surface at fixed angle
    R_AB = np.linspace(1.0, 4.0, 50)
    R_BC = np.linspace(1.5, 4.0, 50)
    R_AB_grid, R_BC_grid, V_grid = surface.energy_surface_2d(R_AB, R_BC, angle_deg=180.0)

    print(f"2D surface calculated: shape = {V_grid.shape}")
    print(f"Energy range: {V_grid.min():.2f} to {V_grid.max():.2f} kJ/mol")


if __name__ == "__main__":
    example_usage()
