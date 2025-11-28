import json

# Read the notebook
with open('03_Transition_State_Theory.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the Investigation 4 intro cell index
inv4_index = None
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell.get('source', []))
    if 'INVESTIGATION 4: Potential Energy Surfaces' in source:
        inv4_index = i
        print(f"Found Investigation 4 at index {i}")
        break

if inv4_index is None:
    print("Error: Investigation 4 not found")
    exit(1)

# Define new cells (simplified - just code cells for now)
new_cells_data = [
    ("code", """# EXERCISE 4.1: LEPS Potential Energy Surface

# Import the LEPS module
import sys
sys.path.append('../modules')

from leps_surface import LEPSSurface
from visualization import plot_pes_3d, plot_pes_contour, plot_morse_curve

print("="*80)
print("CONSTRUCTING LEPS POTENTIAL ENERGY SURFACE")
print("="*80)

# Create LEPS surface for H + HI reaction
surface = LEPSSurface('HI', 'HI', 'I2', K_sato=0.0)

print("\\n✓ LEPS surface initialized for H + H-I system")
print("\\nMorse parameters loaded:")
print(f"  H-I bond: D_e = {surface.params['AB']['D_e']:.2f} kJ/mol, " +
      f"R_e = {surface.params['AB']['R_e']:.3f} Å")

# Visualize Morse potential
R_range = np.linspace(0.8, 5.0, 200)
params_HI = surface.params['AB']
V_morse = surface.morse_potential(R_range, params_HI['D_e'], params_HI['R_e'], params_HI['beta'])

fig, ax = plot_morse_curve(R_range, V_morse, molecule_name="HI",
                           D_e=params_HI['D_e'], R_e=params_HI['R_e'])
plt.show()

print(f"\\n✓ Morse potential minimum at R_e = {params_HI['R_e']:.3f} Å")"""),

    ("code", """# EXERCISE 4.2: 2D Potential Energy Surface

print("\\n" + "="*80)
print("GENERATING 2D POTENTIAL ENERGY SURFACE")
print("="*80)

# Generate 2D surface
R_AB_range = np.linspace(1.0, 4.5, 60)
R_BC_range = np.linspace(1.0, 4.5, 60)

print("\\nCalculating LEPS potential on 60x60 grid...")
R_AB_grid, R_BC_grid, V_grid = surface.energy_surface_2d(R_AB_range, R_BC_range, angle_deg=180.0)

print(f"✓ Surface calculated! Grid shape: {V_grid.shape}")
print(f"  Energy range: {V_grid.min():.1f} to {V_grid.max():.1f} kJ/mol")

# Create 3D visualization
fig_3d, ax_3d = plot_pes_3d(R_AB_grid, R_BC_grid, V_grid,
                            title="LEPS Surface: H + HI -> HI + H",
                            xlabel="R(H···H) (Å)", ylabel="R(H-I) (Å)")
plt.show()

# Create contour plot
fig_contour, ax_contour = plot_pes_contour(R_AB_grid, R_BC_grid, V_grid,
                                            title="LEPS Energy Contours",
                                            xlabel="R(H···H) (Å)", ylabel="R(H-I) (Å)",
                                            levels=40, vmin=-320, vmax=-180)
plt.show()

print("\\n📊 The saddle point (transition state) is visible in the middle of the contour map")"""),

    ("code", """# EXERCISE 4.3: Newton-Raphson Transition State Optimization

from transition_state import TransitionStateOptimizer

print("\\n" + "="*80)
print("TRANSITION STATE OPTIMIZATION")
print("="*80)

# Create optimizer
optimizer = TransitionStateOptimizer(surface, tolerance=1e-6, max_iterations=50)

# Initial guess
R_AB_init, R_BC_init = 1.9, 1.9
print(f"\\nInitial guess: R_AB = {R_AB_init:.2f} Å, R_BC = {R_BC_init:.2f} Å\\n")

# Run optimization
result = optimizer.optimize_saddle_point(R_AB_init, R_BC_init, verbose=True)
history_df = result['history']

# Check saddle point
eigenvalues = result['eigenvalues']
print(f"\\nHessian eigenvalues: {eigenvalues}")
if eigenvalues[0] < 0 and eigenvalues[1] > 0:
    print("✓ Confirmed saddle point (one negative eigenvalue)")

# Calculate activation energy
E_reactants = surface.leps_potential(3.0, surface.params['BC']['R_e'],
                                     3.0 + surface.params['BC']['R_e'])
Ea = result['energy'] - E_reactants
print(f"\\n📊 Activation energy: {Ea:.2f} kJ/mol")"""),

    ("code", """# EXERCISE 4.4: Visualization of Optimization Convergence

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Energy convergence
axes[0].plot(history_df['iteration'], history_df['energy'], 'b-o', linewidth=2)
axes[0].set_xlabel('Iteration')
axes[0].set_ylabel('Energy (kJ/mol)')
axes[0].set_title('Energy Convergence', fontweight='bold')
axes[0].grid(True, alpha=0.3)

# Optimization path on contour
axes[1].contourf(R_AB_grid, R_BC_grid, V_grid, levels=40, cmap='viridis',
                 vmin=-320, vmax=-180, alpha=0.6)
axes[1].plot(history_df['R_AB'], history_df['R_BC'], 'r-o', linewidth=3,
             label='Optimization path', markeredgecolor='white', markeredgewidth=2)
axes[1].plot(history_df['R_AB'].iloc[0], history_df['R_BC'].iloc[0],
             'go', markersize=15, label='Start')
axes[1].plot(history_df['R_AB'].iloc[-1], history_df['R_BC'].iloc[-1],
             'r*', markersize=20, label='Saddle point')
axes[1].set_xlabel('R(H···H) (Å)')
axes[1].set_ylabel('R(H-I) (Å)')
axes[1].set_title('Optimization Path on PES', fontweight='bold')
axes[1].legend()

plt.tight_layout()
plt.show()

print(f"\\n✓ Converged in {result['iterations']} iterations")
print(f"  Final: R_AB = {result['R_AB']:.6f} Å, R_BC = {result['R_BC']:.6f} Å")""")
]

# Create cells
new_cells = []
for cell_type, source in new_cells_data:
    cell = {
        "cell_type": cell_type,
        "metadata": {},
        "source": source.split('\n')
    }
    if cell_type == "code":
        cell["outputs"] = []
        cell["execution_count"] = None
    new_cells.append(cell)

# Insert cells
insert_position = inv4_index + 1
for cell in new_cells:
    nb['cells'].insert(insert_position, cell)
    insert_position += 1

# Write back
with open('03_Transition_State_Theory.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"\n[OK] Successfully added {len(new_cells)} cells to Investigation 4")
print(f"Total cells in notebook: {len(nb['cells'])}")
