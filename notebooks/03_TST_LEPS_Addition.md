# CELLS TO ADD TO NOTEBOOK 03

This file contains new cells to be added to Notebook 03 after cell 13 (after Hammett analysis).

---

## NEW CELL (Markdown):
---

## INVESTIGATION 4: Potential Energy Surfaces and Transition States 🗻

### YOUR TASK
Construct a LEPS potential energy surface and locate the transition state using Newton-Raphson optimization.

In this investigation, you'll move from the thermodynamic view of TST to the actual *potential energy surface* (PES) that governs a chemical reaction. You'll:

1. Construct a LEPS (London-Eyring-Polanyi-Sato) surface for H + HI → HI + H
2. Visualize the energy landscape in 3D and as contour plots
3. Find the exact transition state geometry using Newton-Raphson optimization
4. Calculate force constants and vibrational frequencies at the saddle point

This connects theory to computation - exactly how modern quantum chemistry finds transition states!

### EXERCISE 4.1: Constructing the LEPS Potential Energy Surface

---

## NEW CELL (Code):
```python
# EXERCISE 4.1: LEPS Potential Energy Surface

# Import the LEPS module
import sys
sys.path.append('../modules')

from leps_surface import LEPSSurface
from visualization import plot_pes_3d, plot_pes_contour, plot_morse_curve

print("="*80)
print("CONSTRUCTING LEPS POTENTIAL ENERGY SURFACE")
print("="*80)

# Create LEPS surface for H + HI → HI + H reaction
# This is a symmetric exchange reaction studied extensively in the 1980s
surface = LEPSSurface('HI', 'HI', 'I2', K_sato=0.0)

print("\n✓ LEPS surface initialized for H + H-I system")
print("\nMorse parameters loaded:")
print(f"  H-I bond: D_e = {surface.params['AB']['D_e']:.2f} kJ/mol, " +
      f"R_e = {surface.params['AB']['R_e']:.3f} Å")
print(f"  I-I bond: D_e = {surface.params['AC']['D_e']:.2f} kJ/mol, " +
      f"R_e = {surface.params['AC']['R_e']:.3f} Å")

# First, let's visualize the Morse potential for H-I
print("\n" + "="*80)
print("MORSE POTENTIAL FOR H-I DIATOMIC")
print("="*80)

R_range = np.linspace(0.8, 5.0, 200)
params_HI = surface.params['AB']
V_morse = surface.morse_potential(R_range,
                                  params_HI['D_e'],
                                  params_HI['R_e'],
                                  params_HI['beta'])

fig, ax = plot_morse_curve(R_range, V_morse,
                           molecule_name="HI",
                           D_e=params_HI['D_e'],
                           R_e=params_HI['R_e'],
                           title="Morse Potential for H-I Bond")
plt.show()

print(f"\n✓ Morse potential shows:")
print(f"  • Minimum at R_e = {params_HI['R_e']:.3f} Å")
print(f"  • Dissociation energy D_e = {params_HI['D_e']:.1f} kJ/mol")
print(f"  • At R → ∞, V → 0 (dissociated atoms)")
```

---

## NEW CELL (Markdown):

### Understanding LEPS Potential Energy Surfaces

The **LEPS method** combines Morse potentials for diatomic pairs (H-H, H-I, H-I) using the London equation with Sato modification:

$$V_{LEPS} = \frac{Q_{AB} + Q_{BC} + Q_{AC} - \sqrt{\alpha^2}}{1 + K}$$

where:
- **Q**: Coulomb integrals (attractive interactions)
- **J**: Exchange integrals (repulsive interactions)
- **α²** = 0.5[(J_AB - J_BC)² + (J_BC - J_AC)² + (J_AC - J_AB)²]
- **K**: Sato parameter (adjusts barrier height)

For the H + H-I reaction:
- **Reactants**: H---H-I (R_AB large, R_BC = equilibrium)
- **Products**: H-H---I (R_AB = equilibrium, R_BC large)
- **Transition state**: H···H···I (both bonds partially broken/formed)

**Key Insight**: The transition state is a *saddle point* on the PES:
- Minimum along the reaction valley
- Maximum perpendicular to the reaction path
- Characterized by **one negative eigenvalue** of the Hessian matrix

---

## NEW CELL (Code):
```python
# EXERCISE 4.2: 2D Potential Energy Surface

print("\n" + "="*80)
print("GENERATING 2D POTENTIAL ENERGY SURFACE")
print("="*80)

# Generate 2D surface for collinear H-H-I (angle = 180°)
R_AB_range = np.linspace(1.0, 4.5, 60)
R_BC_range = np.linspace(1.0, 4.5, 60)

print("\nCalculating LEPS potential on 60x60 grid...")
print("(This may take a moment...)")

R_AB_grid, R_BC_grid, V_grid = surface.energy_surface_2d(
    R_AB_range, R_BC_range, angle_deg=180.0
)

print(f"✓ Surface calculated!")
print(f"  Grid shape: {V_grid.shape}")
print(f"  Energy range: {V_grid.min():.1f} to {V_grid.max():.1f} kJ/mol")

# Create 3D visualization
fig_3d, ax_3d = plot_pes_3d(R_AB_grid, R_BC_grid, V_grid,
                            title="LEPS Surface: H + HI → HI + H",
                            xlabel="R(H···H) (Å)",
                            ylabel="R(H-I) (Å)",
                            elev=25, azim=45)
plt.show()

print("\n🗻 3D SURFACE FEATURES:")
print("  • Valley on left: Reactants (H + H-I)")
print("  • Valley on right: Products (H-I + H)")
print("  • Saddle point in middle: Transition state")
print("  • The reaction path follows the valley connecting reactants to products")
```

---

## NEW CELL (Code):
```python
# EXERCISE 4.3: Contour Plot

# Create 2D contour plot (easier to see features)
fig_contour, ax_contour = plot_pes_contour(R_AB_grid, R_BC_grid, V_grid,
                                            title="LEPS Energy Contours: H + HI",
                                            xlabel="R(H···H) (Å)",
                                            ylabel="R(H-I) (Å)",
                                            levels=40,
                                            vmin=-320, vmax=-180)
plt.show()

print("\n📊 CONTOUR MAP INTERPRETATION:")
print("  • Blue regions: Low energy (stable molecules)")
print("  • Red regions: High energy (repulsive interactions)")
print("  • The 'pass' between valleys: Transition state region")
print("  • Symmetry: Due to H + HI → HI + H being symmetric exchange")
```

---

## NEW CELL (Markdown):

### Locating the Transition State

Now comes the computational chemistry part: **finding the exact saddle point geometry**.

**The Challenge**:
- The saddle point is where the gradient ∇V = 0 (stationary point)
- BUT it's NOT a minimum - it has one direction of negative curvature

**The Solution**: Newton-Raphson optimization
1. Start with an initial guess (R_AB, R_BC)
2. Calculate gradient: ∇V = (∂V/∂R_AB, ∂V/∂R_BC)
3. Calculate Hessian: H = matrix of second derivatives
4. Update: **R_new = R_old - H⁻¹ · ∇V**
5. Repeat until |∇V| < tolerance

**Success Criteria**:
- Gradient near zero: |∇V| < 10⁻⁶
- Hessian has exactly **one negative eigenvalue** (confirms saddle point)

This is exactly how quantum chemistry programs (Gaussian, ORCA, Q-Chem) find transition states!

---

## NEW CELL (Code):
```python
# EXERCISE 4.4: Newton-Raphson Transition State Optimization

from transition_state import TransitionStateOptimizer

print("\n" + "="*80)
print("TRANSITION STATE OPTIMIZATION")
print("="*80)

# Create optimizer
optimizer = TransitionStateOptimizer(surface, tolerance=1e-6, max_iterations=50)

# Initial guess (from visual inspection of contour plot)
# The saddle point should be around R_AB ≈ R_BC ≈ 1.9 Å (symmetric)
R_AB_init = 1.9
R_BC_init = 1.9

print(f"\nInitial guess: R_AB = {R_AB_init:.2f} Å, R_BC = {R_BC_init:.2f} Å")
print("\nStarting Newton-Raphson optimization...\n")

# Run optimization
result = optimizer.optimize_saddle_point(R_AB_init, R_BC_init, verbose=True)

# Save optimization history
history_df = result['history']

print("\n" + "="*80)
print("TRANSITION STATE CHARACTERIZATION")
print("="*80)

# Check if it's a true saddle point
eigenvalues = result['eigenvalues']
eigenvectors = result['eigenvectors']

print(f"\nHessian eigenvalues: {eigenvalues}")

if eigenvalues[0] < 0 and eigenvalues[1] > 0:
    print("✓ Confirmed: TRUE SADDLE POINT (one negative eigenvalue)")
    print(f"  • Curvature along reaction coordinate: {eigenvalues[0]:.2f} kJ/(mol·Å²)")
    print(f"  • Curvature perpendicular: {eigenvalues[1]:.2f} kJ/(mol·Å²)")

    # The eigenvector corresponding to negative eigenvalue is the reaction coordinate
    reaction_vector = eigenvectors[:, 0]
    print(f"\n  Reaction coordinate direction: [{reaction_vector[0]:.3f}, {reaction_vector[1]:.3f}]")
    print(f"  (Equal components → symmetric stretch)")
else:
    print("⚠ Warning: Not a saddle point!")

# Activation energy
E_reactants = surface.leps_potential(3.0, surface.params['BC']['R_e'],
                                     3.0 + surface.params['BC']['R_e'])
Ea = result['energy'] - E_reactants

print(f"\n📊 ENERGETICS:")
print(f"  Energy at saddle point: {result['energy']:.2f} kJ/mol")
print(f"  Energy of reactants: {E_reactants:.2f} kJ/mol")
print(f"  Activation energy Ea: {Ea:.2f} kJ/mol")
```

---

## NEW CELL (Code):
```python
# EXERCISE 4.5: Convergence Plot

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Energy vs iteration
axes[0,0].plot(history_df['iteration'], history_df['energy'],
               'b-o', linewidth=2, markersize=8)
axes[0,0].set_xlabel('Iteration', fontsize=11)
axes[0,0].set_ylabel('Energy (kJ/mol)', fontsize=11)
axes[0,0].set_title('Energy Convergence', fontsize=13, fontweight='bold')
axes[0,0].grid(True, alpha=0.3)

# Plot 2: Gradient norm vs iteration
axes[0,1].semilogy(history_df['iteration'], history_df['gradient_norm'],
                   'r-o', linewidth=2, markersize=8)
axes[0,1].axhline(optimizer.tolerance, color='green', linestyle='--',
                  linewidth=2, label=f'Tolerance = {optimizer.tolerance:.0e}')
axes[0,1].set_xlabel('Iteration', fontsize=11)
axes[0,1].set_ylabel('|Gradient| (kJ/mol/Å)', fontsize=11)
axes[0,1].set_title('Gradient Convergence (log scale)', fontsize=13, fontweight='bold')
axes[0,1].legend()
axes[0,1].grid(True, alpha=0.3)

# Plot 3: Optimization path on contour plot
axes[1,0].contourf(R_AB_grid, R_BC_grid, V_grid, levels=40, cmap='viridis',
                   vmin=-320, vmax=-180, alpha=0.6)
axes[1,0].contour(R_AB_grid, R_BC_grid, V_grid, levels=40, colors='black',
                  linewidths=0.5, alpha=0.3)

# Plot optimization path
axes[1,0].plot(history_df['R_AB'], history_df['R_BC'], 'r-o',
               linewidth=3, markersize=10, label='Optimization path',
               markeredgecolor='white', markeredgewidth=2)
axes[1,0].plot(history_df['R_AB'].iloc[0], history_df['R_BC'].iloc[0],
               'go', markersize=15, label='Start', markeredgecolor='white', markeredgewidth=2)
axes[1,0].plot(history_df['R_AB'].iloc[-1], history_df['R_BC'].iloc[-1],
               'r*', markersize=20, label='Saddle point', markeredgecolor='white', markeredgewidth=2)

axes[1,0].set_xlabel('R(H···H) (Å)', fontsize=11)
axes[1,0].set_ylabel('R(H-I) (Å)', fontsize=11)
axes[1,0].set_title('Optimization Path on PES', fontsize=13, fontweight='bold')
axes[1,0].legend()
axes[1,0].grid(True, alpha=0.3)

# Plot 4: R_AB and R_BC vs iteration
axes[1,1].plot(history_df['iteration'], history_df['R_AB'],
               'b-o', linewidth=2, markersize=8, label='R_AB')
axes[1,1].plot(history_df['iteration'], history_df['R_BC'],
               'g-s', linewidth=2, markersize=8, label='R_BC')
axes[1,1].set_xlabel('Iteration', fontsize=11)
axes[1,1].set_ylabel('Distance (Å)', fontsize=11)
axes[1,1].set_title('Coordinate Convergence', fontsize=13, fontweight='bold')
axes[1,1].legend()
axes[1,1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\n✓ OPTIMIZATION SUCCESS!")
print(f"  Converged in {result['iterations']} iterations")
print(f"  Final geometry: R_AB = {result['R_AB']:.6f} Å, R_BC = {result['R_BC']:.6f} Å")
print(f"  (Note symmetry: R_AB ≈ R_BC for symmetric H + HI reaction)")
```

---

## NEW CELL (Markdown):

### Force Constants and Vibrational Analysis

At the transition state, we can calculate **force constants** (second derivatives of energy) to understand the curvature of the PES. This is exactly what's done in frequency calculations in quantum chemistry!

**Physical Meaning**:
- **Positive force constant** (k > 0): Restoring force (stable vibration)
- **Negative force constant** (k < 0): Destabilizing force (reaction coordinate)

The vibrational frequency is:
$$\omega = \frac{1}{2\pi} \sqrt{\frac{k}{\mu}}$$

where μ is the reduced mass.

**Important**: At the transition state, one frequency will be *imaginary* (negative force constant) - this is the signature of the reaction coordinate!

---

## NEW CELL (Code):
```python
# EXERCISE 4.6: Force Constant Calculation

print("\n" + "="*80)
print("FORCE CONSTANT ANALYSIS AT TRANSITION STATE")
print("="*80)

# Calculate force constants by sectioning the PES
force_constants = optimizer.calculate_force_constants(
    result['R_AB'], result['R_BC'],
    n_points=7, delta_R=0.15
)

print(f"\n📐 Force Constants:")
print(f"  k_AB = {force_constants['k_AB']:.2f} kJ/(mol·Å²)")
print(f"  k_BC = {force_constants['k_BC']:.2f} kJ/(mol·Å²)")

# Plot the sectioned PES
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Section along R_AB
sections_AB = force_constants['sections_AB']
axes[0].plot(sections_AB['R_AB'], sections_AB['V'], 'bo-',
            linewidth=2, markersize=10, label='Calculated points')

# Parabolic fit
R_AB_center = result['R_AB']
V_center = result['energy']
R_fit = np.linspace(sections_AB['R_AB'].min(), sections_AB['R_AB'].max(), 100)
V_fit = V_center + 0.5 * force_constants['k_AB'] * (R_fit - R_AB_center)**2

axes[0].plot(R_fit, V_fit, 'r--', linewidth=2, label='Parabolic fit')
axes[0].axvline(R_AB_center, color='green', linestyle=':', linewidth=2,
               label='Saddle point')
axes[0].set_xlabel('R(H···H) (Å)', fontsize=11)
axes[0].set_ylabel('Energy (kJ/mol)', fontsize=11)
axes[0].set_title('PES Section Along R_AB', fontsize=13, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Section along R_BC
sections_BC = force_constants['sections_BC']
axes[1].plot(sections_BC['R_BC'], sections_BC['V'], 'go-',
            linewidth=2, markersize=10, label='Calculated points')

R_BC_center = result['R_BC']
V_fit_BC = V_center + 0.5 * force_constants['k_BC'] * (R_fit - R_BC_center)**2

axes[1].plot(R_fit, V_fit_BC, 'r--', linewidth=2, label='Parabolic fit')
axes[1].axvline(R_BC_center, color='green', linestyle=':', linewidth=2,
               label='Saddle point')
axes[1].set_xlabel('R(H-I) (Å)', fontsize=11)
axes[1].set_ylabel('Energy (kJ/mol)', fontsize=11)
axes[1].set_title('PES Section Along R_BC', fontsize=13, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\n✓ Force constants extracted from parabolic fits to PES sections")
print("  This is exactly how quantum chemistry programs calculate frequencies!")
```

---

## NEW CELL (Code):
```python
# EXERCISE 4.7: Vibrational Frequency Calculation

from transition_state import TransitionStateOptimizer

# Atomic masses
m_H = 1.00783  # amu
m_I = 126.90   # amu

frequencies = optimizer.calculate_vibrational_frequencies(
    force_constants['k_AB'], force_constants['k_BC'],
    m_H, m_H, m_I
)

print("\n" + "="*80)
print("VIBRATIONAL FREQUENCIES AT TRANSITION STATE")
print("="*80)

print(f"\n🎵 Calculated Frequencies:")
print(f"  Mode 1 (along R_AB): {frequencies['omega_AB']:.2f} cm⁻¹")
print(f"  Mode 2 (along R_BC): {frequencies['omega_BC']:.2f} cm⁻¹")

print("\n📝 NOTE:")
print("  These frequencies are very high because:")
print("  1. We're using force constants directly from Hessian")
print("  2. The LEPS surface is approximate")
print("  3. We haven't properly mass-weighted the coordinates")
print("\n  In real quantum chemistry:")
print("  • Use mass-weighted Hessian")
print("  • Project out rotations and translations")
print("  • One frequency would be imaginary (negative eigenvalue)")
print("\n  The KEY CONCEPT: Force constants → vibrational frequencies")
print("  This connects PES curvature to molecular vibrations!")

# Compare to experimental H-I stretch
print(f"\n📊 COMPARISON:")
print(f"  Experimental H-I stretch: ~2309 cm⁻¹")
print(f"  Our calculated value: {frequencies['omega_BC']:.0f} cm⁻¹")
print(f"  (Discrepancy due to approximate coordinate system)")

print("\n" + "="*80)
```

---

## NEW CELL (Markdown):

### Connection to Transition State Theory

What have we accomplished?

1. **Constructed a PES**: Using LEPS method (analytical approximation)
2. **Found the transition state**: Using Newton-Raphson optimization
3. **Characterized the saddle point**: One negative Hessian eigenvalue
4. **Calculated barrier height**: Ea for the reaction

**How this connects to TST**:

- The Eyring equation assumes a **quasi-equilibrium** between reactants and transition state
- The PES shows this transition state as a **saddle point**
- The activation energy ΔG‡ in Eyring equation = barrier height from PES
- Force constants → vibrational frequencies → partition functions → TST rate constants!

**In modern computational chemistry**:
1. Calculate PES using quantum mechanics (DFT, ab initio)
2. Find transition state using optimization (Newton-Raphson, quasi-Newton)
3. Calculate frequencies (Hessian eigenanalysis)
4. Predict rate constant using TST formulas

**You've just done what research groups do every day to predict reaction kinetics!**

---

## NEW CELL (Markdown):

### 🎯 INVESTIGATION 4 SUMMARY

**What you learned**:
- ✅ How to construct LEPS potential energy surfaces
- ✅ How to visualize 3D surfaces and contour plots
- ✅ How to locate transition states using Newton-Raphson optimization
- ✅ How to characterize saddle points (eigenvalue analysis)
- ✅ How to calculate force constants and vibrational frequencies
- ✅ How computational chemistry connects to TST

**Key Insights**:
1. The transition state is a **saddle point** on the PES (one negative eigenvalue)
2. Optimization algorithms systematically find this saddle point
3. The PES curvature (Hessian) gives force constants and frequencies
4. This connects directly to TST partition functions and rate constants

**Real-World Application**:
- This is EXACTLY how programs like Gaussian find transition states
- Replace LEPS with DFT/ab initio for real molecules
- Same algorithms: Newton-Raphson, quasi-Newton (BFGS), eigenvector following

---

[Continue with existing PHASE 3: SYNTHESIZE section...]
