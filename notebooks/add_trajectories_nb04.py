import json

# Read the notebook
with open('04_Molecular_Dynamics.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find where to insert (after Investigation 3, before Phase 3)
insert_idx = None
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell.get('source', []))
    if 'PHASE 3: SYNTHESIZE' in source:
        insert_idx = i
        print(f"Found Phase 3 at index {i}")
        break

if insert_idx is None:
    print("Error: Could not find insertion point")
    exit(1)

# Define new cells for Investigation 4
new_cells_data = [
    ("markdown", """---

## INVESTIGATION 4: Classical Trajectory Simulations 🚀

### YOUR TASK
Run actual molecular dynamics simulations to observe individual collision events and analyze reaction outcomes.

In this investigation, you'll use **classical trajectory calculations** - the computational method that Polanyi and coworkers used in the 1960s-70s to validate their rules! You'll:

1. Run single trajectories on the H + HI LEPS surface
2. Visualize trajectories on the PES
3. Perform Monte Carlo sampling to generate many trajectories
4. Analyze statistical outcomes (reactive vs non-reactive)
5. Validate energy conservation

This is exactly how modern reaction dynamics simulations work!

### EXERCISE 4.1: Single Trajectory Calculation"""),

    ("code", """# EXERCISE 4.1: Run a Single Classical Trajectory

# Import trajectory module
import sys
sys.path.append('../modules')

from leps_surface import LEPSSurface
from trajectory import ClassicalTrajectory
from visualization import plot_pes_contour

print("="*80)
print("CLASSICAL TRAJECTORY SIMULATION")
print("="*80)

# Create LEPS surface for H + HI reaction
surface = LEPSSurface('HI', 'HI', 'I2', K_sato=0.0)
print("\\n[OK] LEPS surface initialized for H + H-I system")

# Create trajectory calculator
traj_calc = ClassicalTrajectory(surface, 'H', 'H', 'I', dt=0.010)
print("[OK] Trajectory calculator initialized")
print(f"  Time step: {traj_calc.dt} fs (femtoseconds)")
print(f"  Atomic masses: H={traj_calc.m_A:.3f} amu, H={traj_calc.m_B:.3f} amu, I={traj_calc.m_C:.3f} amu")

# Set up initial conditions: H approaching H-I
print("\\n" + "="*80)
print("INITIAL CONDITIONS")
print("="*80)

R_AB_0 = 3.0      # H...H distance (Angstroms) - well separated
R_BC_0 = 1.609    # H-I at equilibrium distance
R_AC_0 = R_AB_0 + R_BC_0  # Collinear geometry

# Initial velocities: H approaching with 50 kJ/mol translational energy
# v = sqrt(2*E/m), where E = 50 kJ/mol per molecule
E_trans_kJ_mol = 50.0
# Convert to velocity in Angstrom/fs
# E (kJ/mol) = 0.5 * m (amu) * v^2 (Ang/fs)^2 * 9646.9 (conversion factor)
v_approach = -np.sqrt(2 * E_trans_kJ_mol / (traj_calc.m_A * 9646.9))

v_AB_0 = v_approach
v_BC_0 = 0.0
v_AC_0 = v_approach

print(f"  R_AB = {R_AB_0:.3f} Å (H...H)")
print(f"  R_BC = {R_BC_0:.3f} Å (H-I)")
print(f"  R_AC = {R_AC_0:.3f} Å (total)")
print(f"\\n  v_AB = {v_AB_0:.4f} Å/fs (H approaching)")
print(f"  Translational energy: {E_trans_kJ_mol:.1f} kJ/mol")

# Run trajectory
print("\\n" + "="*80)
print("RUNNING TRAJECTORY...")
print("="*80)

result = traj_calc.run_trajectory(R_AB_0, R_BC_0, R_AC_0,
                                 v_AB_0, v_BC_0, v_AC_0,
                                 max_time=500.0, save_interval=5)

print(f"\\n[OK] Trajectory completed")
print(f"  Duration: {result['time'][-1]:.2f} fs")
print(f"  Outcome: {result['outcome']}")
print(f"  Energy drift: {result['energy_drift']:.4f}%")
print(f"  Initial total energy: {result['E_total'][0]:.2f} kJ/mol")
print(f"  Final total energy: {result['E_total'][-1]:.2f} kJ/mol")"""),

    ("code", """# EXERCISE 4.2: Visualize Trajectory on PES

# Generate PES contour
R_AB_range = np.linspace(1.0, 4.5, 50)
R_BC_range = np.linspace(1.0, 4.5, 50)
R_AB_grid, R_BC_grid, V_grid = surface.energy_surface_2d(R_AB_range, R_BC_range, angle_deg=180.0)

# Create trajectory overlay plot
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Trajectory on contour map
contour = axes[0].contourf(R_AB_grid, R_BC_grid, V_grid, levels=40, cmap='viridis',
                           vmin=-320, vmax=-180, alpha=0.7)
axes[0].contour(R_AB_grid, R_BC_grid, V_grid, levels=40, colors='black',
               linewidths=0.5, alpha=0.3)

# Overlay trajectory
axes[0].plot(result['R_AB'], result['R_BC'], 'r-', linewidth=2.5, alpha=0.8,
            label='Trajectory path')
axes[0].plot(result['R_AB'][0], result['R_BC'][0], 'go', markersize=12,
            label='Start', markeredgecolor='white', markeredgewidth=2)
axes[0].plot(result['R_AB'][-1], result['R_BC'][-1], 'bs', markersize=12,
            label='End', markeredgecolor='white', markeredgewidth=2)

axes[0].set_xlabel('R(H···H) (Å)', fontsize=11)
axes[0].set_ylabel('R(H-I) (Å)', fontsize=11)
axes[0].set_title('Trajectory on LEPS Surface', fontsize=13, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

plt.colorbar(contour, ax=axes[0], label='Energy (kJ/mol)')

# Plot 2: Energy conservation
axes[1].plot(result['time'], result['V'], 'b-', linewidth=2, label='Potential Energy')
axes[1].plot(result['time'], result['T'], 'r-', linewidth=2, label='Kinetic Energy')
axes[1].plot(result['time'], result['E_total'], 'k--', linewidth=2.5, label='Total Energy')

axes[1].set_xlabel('Time (fs)', fontsize=11)
axes[1].set_ylabel('Energy (kJ/mol)', fontsize=11)
axes[1].set_title('Energy Conservation', fontsize=13, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\\n" + "="*80)
print("TRAJECTORY ANALYSIS")
print("="*80)

print(f"\\nInitial state:")
print(f"  V (potential): {result['V'][0]:.2f} kJ/mol")
print(f"  T (kinetic): {result['T'][0]:.2f} kJ/mol")
print(f"  E (total): {result['E_total'][0]:.2f} kJ/mol")

print(f"\\nFinal state:")
print(f"  V (potential): {result['V'][-1]:.2f} kJ/mol")
print(f"  T (kinetic): {result['T'][-1]:.2f} kJ/mol")
print(f"  E (total): {result['E_total'][-1]:.2f} kJ/mol")

print(f"\\nEnergy conservation:")
print(f"  Absolute drift: {abs(result['E_total'][-1] - result['E_total'][0]):.4f} kJ/mol")
print(f"  Percent drift: {result['energy_drift']:.4f}%")
if abs(result['energy_drift']) < 0.01:
    print("  [OK] Excellent energy conservation!")

print(f"\\nOutcome: {result['outcome'].upper()}")
if result['outcome'] == 'reactive':
    print("  → Reaction occurred: H + HI -> HI + H")
    print("  → New bond formed (H-I)")
elif result['outcome'] == 'non-reactive':
    print("  → No reaction: H bounced off")
    print("  → Original bond (H-I) intact")
else:
    print("  → Simulation incomplete (needs longer time)")"""),

    ("markdown", """### Understanding Classical Trajectories

What you just witnessed is a **classical molecular dynamics simulation** - the foundation of computational reaction dynamics!

**Key Concepts**:

1. **Velocity Verlet Integration**: Numerical method to solve Newton's equations
   - Updates positions and velocities at each time step (0.010 fs)
   - Symplectic integrator (conserves energy well)
   - Same algorithm used in modern MD programs

2. **Energy Conservation**: Critical quality check
   - Total energy should remain constant (no external forces)
   - Drift < 0.01% indicates good numerical accuracy
   - Larger drift means time step too large or numerical instability

3. **Trajectory Outcome**: Reactive vs Non-Reactive
   - **Reactive**: Products separate (R_BC > 6 Å, R_AB < 3 Å)
   - **Non-Reactive**: Reactants bounce apart (R_AB > 6 Å, R_BC < 3 Å)
   - Outcome depends on collision energy, angle, initial phase

**Connection to Polanyi's Rules**:
- Trajectories reveal WHERE energy goes (vibration vs translation)
- Statistics over many trajectories → product state distributions
- Validates predictions from PES topology!"""),

    ("markdown", """### EXERCISE 4.3: Batch Trajectory Calculations

One trajectory isn't enough - we need **statistics**! Let's run many trajectories with different initial conditions to get reaction probabilities and product distributions."""),

    ("code", """# EXERCISE 4.3: Monte Carlo Trajectory Batch

print("\\n" + "="*80)
print("MONTE CARLO TRAJECTORY SAMPLING")
print("="*80)

# Parameters for batch
n_trajectories = 20  # Number of trajectories to run
E_trans_target = 50.0  # kJ/mol

print(f"\\nRunning {n_trajectories} trajectories...")
print(f"Target collision energy: {E_trans_target:.1f} kJ/mol")
print("(This may take a minute...)\\n")

# Storage for results
batch_results = []
reactive_count = 0
non_reactive_count = 0

# Run trajectories
for i in range(n_trajectories):
    # Vary initial conditions slightly (Monte Carlo sampling)
    # Add small random perturbations to initial velocity
    v_perturbation = np.random.normal(0, 0.005)  # Small variation
    v_AB_init = v_approach + v_perturbation

    # Run trajectory
    res = traj_calc.run_trajectory(R_AB_0, R_BC_0, R_AC_0,
                                  v_AB_init, v_BC_0, v_AC_0,
                                  max_time=500.0, save_interval=10)

    batch_results.append({
        'trajectory_id': i,
        'outcome': res['outcome'],
        'energy_drift': res['energy_drift'],
        'final_R_AB': res['R_AB'][-1],
        'final_R_BC': res['R_BC'][-1],
        'duration': res['time'][-1]
    })

    if res['outcome'] == 'reactive':
        reactive_count += 1
    elif res['outcome'] == 'non-reactive':
        non_reactive_count += 1

    # Progress indicator
    if (i+1) % 5 == 0:
        print(f"  Completed {i+1}/{n_trajectories} trajectories...")

print("\\n[OK] Batch calculation complete!")

# Create summary DataFrame
batch_df = pd.DataFrame(batch_results)

# Analysis
print("\\n" + "="*80)
print("STATISTICAL ANALYSIS")
print("="*80)

print(f"\\nTotal trajectories: {n_trajectories}")
print(f"  Reactive: {reactive_count} ({reactive_count/n_trajectories*100:.1f}%)")
print(f"  Non-reactive: {non_reactive_count} ({non_reactive_count/n_trajectories*100:.1f}%)")
print(f"  Incomplete: {n_trajectories - reactive_count - non_reactive_count}")

# Reaction probability (cross section)
reaction_prob = reactive_count / n_trajectories
print(f"\\nReaction probability: {reaction_prob:.3f}")
print(f"  (This is proportional to the reaction cross section)")

# Energy conservation statistics
avg_drift = batch_df['energy_drift'].abs().mean()
max_drift = batch_df['energy_drift'].abs().max()
print(f"\\nEnergy conservation:")
print(f"  Average drift: {avg_drift:.4f}%")
print(f"  Maximum drift: {max_drift:.4f}%")
if avg_drift < 0.01:
    print("  [OK] Excellent overall conservation!")

# Visualize outcomes
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Outcome distribution
outcomes = batch_df['outcome'].value_counts()
colors = {'reactive': 'green', 'non-reactive': 'red', 'incomplete': 'gray'}
bars = axes[0].bar(range(len(outcomes)), outcomes.values,
                   color=[colors.get(k, 'blue') for k in outcomes.index],
                   edgecolor='black', linewidth=2, alpha=0.7)
axes[0].set_xticks(range(len(outcomes)))
axes[0].set_xticklabels(outcomes.index, rotation=15)
axes[0].set_ylabel('Count', fontsize=11)
axes[0].set_title('Trajectory Outcomes', fontsize=13, fontweight='bold')
axes[0].grid(True, alpha=0.3, axis='y')

# Add count labels
for i, (outcome, count) in enumerate(outcomes.items()):
    axes[0].text(i, count + 0.5, str(count), ha='center', fontweight='bold')

# Plot 2: Final geometries
reactive = batch_df[batch_df['outcome'] == 'reactive']
non_reactive = batch_df[batch_df['outcome'] == 'non-reactive']

if len(reactive) > 0:
    axes[1].scatter(reactive['final_R_AB'], reactive['final_R_BC'],
                   s=100, c='green', alpha=0.6, edgecolors='black',
                   linewidth=1.5, label='Reactive', marker='o')

if len(non_reactive) > 0:
    axes[1].scatter(non_reactive['final_R_AB'], non_reactive['final_R_BC'],
                   s=100, c='red', alpha=0.6, edgecolors='black',
                   linewidth=1.5, label='Non-reactive', marker='s')

axes[1].axhline(6, color='gray', linestyle='--', linewidth=1, alpha=0.5)
axes[1].axvline(6, color='gray', linestyle='--', linewidth=1, alpha=0.5)
axes[1].set_xlabel('Final R_AB (Å)', fontsize=11)
axes[1].set_ylabel('Final R_BC (Å)', fontsize=11)
axes[1].set_title('Final Product Geometries', fontsize=13, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\\n" + "="*80)"""),

    ("markdown", """### 🎯 INVESTIGATION 4 SUMMARY

**What you learned**:
- ✅ How to run classical trajectory simulations on PES
- ✅ How to visualize individual collision events
- ✅ How to monitor energy conservation (quality control)
- ✅ How to perform Monte Carlo sampling for statistics
- ✅ How to calculate reaction probabilities and cross sections

**Key Insights**:
1. **Individual trajectories** reveal microscopic collision dynamics
2. **Energy conservation** validates numerical accuracy (Velocity Verlet)
3. **Statistical sampling** bridges microscopic → macroscopic (rate constants)
4. **Trajectory outcomes** directly test Polanyi's Rules

**Real-World Applications**:
- This is EXACTLY how reaction dynamics are studied computationally
- Replace LEPS with quantum mechanical PES (DFT, CCSD(T))
- Modern codes: VENUS, NWChem, AMBER, GROMACS
- Used for: combustion, atmospheric chemistry, catalysis, drug design

**Connection to Experiments**:
- Molecular beam experiments measure these same quantities!
- Differential cross sections ← trajectory scattering angles
- Product state distributions ← trajectory final states
- Your simulations validate (or predict) experimental results

---""")
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

# Insert cells before Phase 3
for cell in new_cells:
    nb['cells'].insert(insert_idx, cell)
    insert_idx += 1

# Write back
with open('04_Molecular_Dynamics.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"\n[OK] Successfully added {len(new_cells)} cells to Notebook 04")
print(f"Total cells in notebook: {len(nb['cells'])}")
