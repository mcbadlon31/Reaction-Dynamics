"""
Visualization tools for Potential Energy Surfaces

This module provides plotting functions for LEPS and other PES representations,
including 3D surface plots, 2D contour plots, and trajectory overlays.

Author: Integration of research papers into educational framework
Date: 2025-11-27
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


def plot_pes_3d(R_AB_grid, R_BC_grid, V_grid, title="LEPS Potential Energy Surface",
                xlabel="R_AB (Å)", ylabel="R_BC (Å)", zlabel="Energy (kJ/mol)",
                elev=30, azim=45, cmap='viridis', figsize=(10, 8)):
    """
    Create 3D surface plot of potential energy surface.

    Parameters:
        R_AB_grid (ndarray): Meshgrid of R_AB coordinates
        R_BC_grid (ndarray): Meshgrid of R_BC coordinates
        V_grid (ndarray): Meshgrid of energy values
        title (str): Plot title
        xlabel, ylabel, zlabel (str): Axis labels
        elev (float): Elevation angle for viewing (degrees)
        azim (float): Azimuthal angle for viewing (degrees)
        cmap (str): Colormap name
        figsize (tuple): Figure size (width, height)

    Returns:
        fig, ax: Matplotlib figure and axes objects

    Reference: Badlon (2018) Figure 1
    """
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')

    # Create surface plot
    surf = ax.plot_surface(R_AB_grid, R_BC_grid, V_grid,
                          cmap=cmap, alpha=0.9,
                          linewidth=0, antialiased=True,
                          edgecolor='none')

    # Add colorbar
    cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)
    cbar.set_label(zlabel, rotation=270, labelpad=20)

    # Labels and title
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_zlabel(zlabel, fontsize=11)
    ax.set_title(title, fontsize=13, fontweight='bold')

    # Set viewing angle
    ax.view_init(elev=elev, azim=azim)

    # Adjust layout
    plt.tight_layout()

    return fig, ax


def plot_pes_contour(R_AB_grid, R_BC_grid, V_grid, title="LEPS Energy Contours",
                     xlabel="R_AB (Å)", ylabel="R_BC (Å)",
                     levels=20, cmap='viridis', figsize=(9, 7),
                     vmin=None, vmax=None, show_saddle=False, saddle_point=None):
    """
    Create 2D contour plot of potential energy surface.

    Parameters:
        R_AB_grid (ndarray): Meshgrid of R_AB coordinates
        R_BC_grid (ndarray): Meshgrid of R_BC coordinates
        V_grid (ndarray): Meshgrid of energy values
        title (str): Plot title
        xlabel, ylabel (str): Axis labels
        levels (int or array): Number of contour levels or specific levels
        cmap (str): Colormap name
        figsize (tuple): Figure size
        vmin, vmax (float): Min/max values for color scale
        show_saddle (bool): Whether to mark saddle point
        saddle_point (tuple): (R_AB, R_BC) coordinates of saddle point

    Returns:
        fig, ax: Matplotlib figure and axes objects

    Reference: Badlon (2018) Figures 2-3
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Create filled contour plot
    contourf = ax.contourf(R_AB_grid, R_BC_grid, V_grid,
                           levels=levels, cmap=cmap,
                           vmin=vmin, vmax=vmax)

    # Add contour lines
    contour = ax.contour(R_AB_grid, R_BC_grid, V_grid,
                        levels=levels, colors='black',
                        linewidths=0.5, alpha=0.4,
                        vmin=vmin, vmax=vmax)

    # Add contour labels
    ax.clabel(contour, inline=True, fontsize=8, fmt='%0.0f')

    # Mark saddle point if requested
    if show_saddle and saddle_point is not None:
        ax.plot(saddle_point[0], saddle_point[1], 'r*',
               markersize=15, label='Saddle Point',
               markeredgecolor='white', markeredgewidth=1)
        ax.legend(loc='best')

    # Colorbar
    cbar = fig.colorbar(contourf, ax=ax)
    cbar.set_label('Energy (kJ/mol)', rotation=270, labelpad=20)

    # Labels and title
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=13, fontweight='bold')

    # Grid
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

    # Adjust layout
    plt.tight_layout()

    return fig, ax


def plot_reaction_path(R_AB_grid, R_BC_grid, V_grid, path_coords,
                       title="Reaction Path on PES",
                       xlabel="R_AB (Å)", ylabel="R_BC (Å)",
                       levels=20, cmap='viridis', figsize=(9, 7)):
    """
    Plot reaction path overlaid on contour map.

    Parameters:
        R_AB_grid (ndarray): Meshgrid of R_AB coordinates
        R_BC_grid (ndarray): Meshgrid of R_BC coordinates
        V_grid (ndarray): Meshgrid of energy values
        path_coords (tuple): (R_AB_path, R_BC_path) arrays of path coordinates
        title (str): Plot title
        xlabel, ylabel (str): Axis labels
        levels (int): Number of contour levels
        cmap (str): Colormap name
        figsize (tuple): Figure size

    Returns:
        fig, ax: Matplotlib figure and axes objects

    Reference: Badlon (2018) Figure 4
    """
    # Create contour plot
    fig, ax = plot_pes_contour(R_AB_grid, R_BC_grid, V_grid,
                               title=title, xlabel=xlabel, ylabel=ylabel,
                               levels=levels, cmap=cmap, figsize=figsize)

    # Overlay reaction path
    R_AB_path, R_BC_path = path_coords
    ax.plot(R_AB_path, R_BC_path, 'r-', linewidth=2.5,
           label='Reaction Path', marker='o', markersize=4,
           markerfacecolor='white', markeredgecolor='red')

    # Mark start and end points
    ax.plot(R_AB_path[0], R_BC_path[0], 'go', markersize=10,
           label='Reactants', markeredgecolor='white', markeredgewidth=1.5)
    ax.plot(R_AB_path[-1], R_BC_path[-1], 'bs', markersize=10,
           label='Products', markeredgecolor='white', markeredgewidth=1.5)

    ax.legend(loc='best')

    return fig, ax


def plot_trajectory(R_AB_grid, R_BC_grid, V_grid, trajectory_data,
                   title="Classical Trajectory on PES",
                   xlabel="R_AB (Å)", ylabel="R_BC (Å)",
                   levels=20, cmap='viridis', figsize=(9, 7),
                   show_direction=True):
    """
    Plot classical trajectory overlaid on contour map.

    Parameters:
        R_AB_grid (ndarray): Meshgrid of R_AB coordinates
        R_BC_grid (ndarray): Meshgrid of R_BC coordinates
        V_grid (ndarray): Meshgrid of energy values
        trajectory_data (ndarray): Nx2 array of (R_AB, R_BC) trajectory points
        title (str): Plot title
        xlabel, ylabel (str): Axis labels
        levels (int): Number of contour levels
        cmap (str): Colormap name
        figsize (tuple): Figure size
        show_direction (bool): Whether to show direction arrows

    Returns:
        fig, ax: Matplotlib figure and axes objects

    Reference: Badlon (2018) Trajectory calculations
    """
    # Create contour plot
    fig, ax = plot_pes_contour(R_AB_grid, R_BC_grid, V_grid,
                               title=title, xlabel=xlabel, ylabel=ylabel,
                               levels=levels, cmap=cmap, figsize=figsize)

    # Extract trajectory coordinates
    R_AB_traj = trajectory_data[:, 0]
    R_BC_traj = trajectory_data[:, 1]

    # Plot trajectory
    ax.plot(R_AB_traj, R_BC_traj, 'r-', linewidth=1.5,
           alpha=0.7, label='Trajectory')

    # Add direction arrows if requested
    if show_direction:
        # Add arrows every N points
        arrow_spacing = max(len(R_AB_traj) // 10, 1)
        for i in range(0, len(R_AB_traj) - 1, arrow_spacing):
            dx = R_AB_traj[i+1] - R_AB_traj[i]
            dy = R_BC_traj[i+1] - R_BC_traj[i]
            ax.arrow(R_AB_traj[i], R_BC_traj[i], dx, dy,
                    head_width=0.05, head_length=0.08,
                    fc='red', ec='red', alpha=0.6)

    # Mark start point
    ax.plot(R_AB_traj[0], R_BC_traj[0], 'go', markersize=10,
           label='Start', markeredgecolor='white', markeredgewidth=1.5)

    # Mark end point
    ax.plot(R_AB_traj[-1], R_BC_traj[-1], 'bs', markersize=10,
           label='End', markeredgecolor='white', markeredgewidth=1.5)

    ax.legend(loc='best')

    return fig, ax


def plot_energy_profile(reaction_coordinate, energies,
                       title="Energy Profile Along Reaction Coordinate",
                       xlabel="Reaction Coordinate", ylabel="Energy (kJ/mol)",
                       figsize=(10, 6), show_barrier=True, barrier_height=None):
    """
    Plot 1D energy profile along reaction coordinate.

    Parameters:
        reaction_coordinate (array): Reaction coordinate values
        energies (array): Energy values along coordinate
        title (str): Plot title
        xlabel, ylabel (str): Axis labels
        figsize (tuple): Figure size
        show_barrier (bool): Whether to annotate barrier height
        barrier_height (float): Barrier height to annotate (auto-detected if None)

    Returns:
        fig, ax: Matplotlib figure and axes objects

    Reference: Badlon (2018) Figure 5
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Plot energy profile
    ax.plot(reaction_coordinate, energies, 'b-', linewidth=2.5)

    # Find and mark barrier if requested
    if show_barrier:
        if barrier_height is None:
            # Auto-detect barrier (maximum)
            barrier_idx = np.argmax(energies)
            barrier_height = energies[barrier_idx]
            barrier_coord = reaction_coordinate[barrier_idx]
        else:
            # Use provided barrier height
            barrier_idx = np.argmin(np.abs(energies - barrier_height))
            barrier_coord = reaction_coordinate[barrier_idx]

        # Mark barrier point
        ax.plot(barrier_coord, barrier_height, 'r*', markersize=15,
               label=f'Barrier: {barrier_height:.1f} kJ/mol',
               markeredgecolor='white', markeredgewidth=1)

        # Add horizontal line at barrier
        ax.axhline(y=barrier_height, color='r', linestyle='--',
                  alpha=0.5, linewidth=1)

        ax.legend(loc='best')

    # Labels and title
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=13, fontweight='bold')

    # Grid
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

    # Adjust layout
    plt.tight_layout()

    return fig, ax


def plot_morse_curve(R_range, V_morse, molecule_name="",
                    D_e=None, R_e=None,
                    title="Morse Potential Curve",
                    xlabel="Internuclear Distance R (Å)",
                    ylabel="Potential Energy (kJ/mol)",
                    figsize=(10, 6)):
    """
    Plot Morse potential curve for a diatomic molecule.

    Parameters:
        R_range (array): Range of internuclear distances
        V_morse (array): Morse potential energies
        molecule_name (str): Name of molecule for legend
        D_e (float): Dissociation energy (for annotation)
        R_e (float): Equilibrium distance (for annotation)
        title (str): Plot title
        xlabel, ylabel (str): Axis labels
        figsize (tuple): Figure size

    Returns:
        fig, ax: Matplotlib figure and axes objects

    Reference: Badlon (2018) Morse potential
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Plot Morse curve
    label = f"{molecule_name} Morse Potential" if molecule_name else "Morse Potential"
    ax.plot(R_range, V_morse, 'b-', linewidth=2.5, label=label)

    # Add reference lines if parameters provided
    if R_e is not None:
        ax.axvline(x=R_e, color='g', linestyle='--',
                  alpha=0.5, linewidth=1.5,
                  label=f'R_e = {R_e:.3f} Å')

    if D_e is not None:
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3, linewidth=1)
        ax.axhline(y=-D_e, color='r', linestyle='--',
                  alpha=0.5, linewidth=1.5,
                  label=f'D_e = {D_e:.1f} kJ/mol')

    # Labels and title
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=13, fontweight='bold')

    # Grid and legend
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    ax.legend(loc='best')

    # Adjust layout
    plt.tight_layout()

    return fig, ax


def example_usage():
    """Example: Visualize H + HI LEPS surface."""
    from leps_surface import LEPSSurface

    # Create LEPS surface
    surface = LEPSSurface('HI', 'HI', 'I2', K_sato=0.0)

    # Generate 2D surface data
    R_AB = np.linspace(1.0, 4.0, 50)
    R_BC = np.linspace(1.5, 4.0, 50)
    R_AB_grid, R_BC_grid, V_grid = surface.energy_surface_2d(R_AB, R_BC, angle_deg=180.0)

    # Create 3D surface plot
    fig3d, ax3d = plot_pes_3d(R_AB_grid, R_BC_grid, V_grid,
                              title="H + HI LEPS Surface (K=0.0)")
    plt.savefig('leps_3d_surface.png', dpi=150, bbox_inches='tight')
    print("Saved 3D surface plot to leps_3d_surface.png")

    # Create 2D contour plot
    fig2d, ax2d = plot_pes_contour(R_AB_grid, R_BC_grid, V_grid,
                                   title="H + HI LEPS Contours (K=0.0)",
                                   levels=30)
    plt.savefig('leps_contour.png', dpi=150, bbox_inches='tight')
    print("Saved contour plot to leps_contour.png")

    # Example Morse potential plot
    R_range = np.linspace(0.5, 5.0, 200)
    params_HI = surface.params['AB']
    V_morse = surface.morse_potential(R_range,
                                     params_HI['D_e'],
                                     params_HI['R_e'],
                                     params_HI['beta'])

    fig_morse, ax_morse = plot_morse_curve(R_range, V_morse,
                                          molecule_name="HI",
                                          D_e=params_HI['D_e'],
                                          R_e=params_HI['R_e'])
    plt.savefig('morse_HI.png', dpi=150, bbox_inches='tight')
    print("Saved Morse curve to morse_HI.png")

    plt.show()


if __name__ == "__main__":
    example_usage()
