import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch, Arc, Ellipse
from mpl_toolkits.mplot3d import Axes3D
import os

# Ensure images directory exists
os.makedirs('images', exist_ok=True)

# Set global style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'lines.linewidth': 2
})

def save_plot(filename):
    plt.savefig(f'images/{filename}', bbox_inches='tight')
    plt.close()
    print(f"Generated {filename}")

# ==========================================
# TOPIC 18A: COLLISION THEORY
# ==========================================

def plot_collision_cylinder():
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.grid(False)
    
    # Cylinder
    cylinder = Rectangle((0, -1), 8, 2, facecolor='lightblue', alpha=0.3, edgecolor='blue')
    ax.add_patch(cylinder)
    
    # Molecule A
    circle_a = Circle((0, 0), 0.5, color='red', label='Molecule A')
    ax.add_patch(circle_a)
    
    # Molecule B (inside)
    circle_b1 = Circle((4, 0.5), 0.5, color='blue', alpha=0.5)
    ax.add_patch(circle_b1)
    
    # Molecule B (outside)
    circle_b2 = Circle((4, 1.5), 0.5, color='blue', alpha=0.5)
    ax.add_patch(circle_b2)
    
    # Path
    ax.arrow(0, 0, 8, 0, head_width=0.2, head_length=0.3, fc='k', ec='k', linestyle='--')
    
    # Annotations
    ax.text(0, 0.6, 'A', fontsize=12, ha='center')
    ax.text(4, 0.6, 'Collision', fontsize=10, ha='center')
    ax.text(4, 1.6, 'Miss', fontsize=10, ha='center')
    ax.text(8.2, 0, r'$v_{rel} \Delta t$', fontsize=12, va='center')
    ax.text(0, -1.2, r'Area $\sigma = \pi d^2$', fontsize=12, ha='center')
    
    ax.set_xlim(-1, 9)
    ax.set_ylim(-2, 2)
    ax.axis('off')
    ax.set_title('Collision Cylinder Model')
    save_plot('collision_cylinder.png')

def plot_maxwell_boltzmann_speeds():
    fig, ax = plt.subplots(figsize=(8, 5))
    
    v = np.linspace(0, 2000, 500)
    m_N2 = 0.028 / 6.022e23 # kg
    k = 1.38e-23
    
    def mb_dist(v, T, m):
        return 4 * np.pi * (m / (2 * np.pi * k * T))**(1.5) * v**2 * np.exp(-m * v**2 / (2 * k * T))
    
    y1 = mb_dist(v, 300, m_N2)
    y2 = mb_dist(v, 1000, m_N2)
    
    ax.plot(v, y1, 'b-', label='300 K')
    ax.plot(v, y2, 'r-', label='1000 K')
    
    ax.set_xlabel('Speed (m/s)')
    ax.set_ylabel('Probability Density')
    ax.set_title('Maxwell-Boltzmann Speed Distribution ($N_2$)')
    ax.legend()
    save_plot('maxwell_boltzmann_speeds.png')

def plot_maxwell_boltzmann_energy():
    fig, ax = plt.subplots(figsize=(8, 5))
    
    E = np.linspace(0, 10, 500) # Arbitrary units
    T = 1.0
    
    # f(E) = 2*sqrt(E/pi) * exp(-E)
    y = 2 * np.sqrt(E/np.pi) * np.exp(-E)
    
    ax.plot(E, y, 'k-', linewidth=2)
    
    # Shading
    Ea = 4.0
    mask = E >= Ea
    ax.fill_between(E[mask], y[mask], color='red', alpha=0.3, label=r'Reactive Fraction ($E > E_a$)')
    
    ax.axvline(Ea, color='red', linestyle='--')
    ax.text(Ea, 0.05, r'$E_a$', color='red', ha='right', va='bottom', fontsize=14)
    
    ax.set_xlabel('Energy ($E/RT$)')
    ax.set_ylabel('Fraction of Molecules')
    ax.set_title('Energy Distribution and Activation Energy')
    ax.legend()
    save_plot('maxwell_boltzmann_energy.png')

def plot_reactive_cross_section():
    fig, ax = plt.subplots(figsize=(8, 5))
    
    E = np.linspace(0, 10, 500)
    Ea = 3.0
    sigma_0 = 1.0
    
    sigma_r = np.zeros_like(E)
    mask = E >= Ea
    sigma_r[mask] = sigma_0 * (1 - Ea/E[mask])
    
    ax.plot(E, sigma_r, 'b-', linewidth=2)
    ax.axvline(Ea, color='red', linestyle='--', label=r'Threshold $E_a$')
    
    ax.set_xlabel('Collision Energy $\epsilon$')
    ax.set_ylabel(r'Reactive Cross-Section $\sigma_r(\epsilon)$')
    ax.set_title('Energy Dependence of Reactive Cross-Section')
    ax.legend()
    save_plot('reactive_cross_section.png')

def plot_arrhenius_plot():
    fig, ax = plt.subplots(figsize=(8, 5))
    
    inv_T = np.linspace(0.002, 0.004, 100) # 1/K
    ln_k = 20 - 5000 * inv_T
    
    ax.plot(inv_T, ln_k, 'b-', linewidth=2)
    
    # Annotations
    ax.text(0.003, 5, r'Slope = $-E_a/R$', fontsize=12, rotation=-20)
    ax.text(0.0021, 10, r'Intercept = $\ln A$', fontsize=12)
    
    ax.set_xlabel(r'$1/T$ (K$^{-1}$)')
    ax.set_ylabel(r'$\ln k$')
    ax.set_title('Arrhenius Plot')
    save_plot('arrhenius_plot.png')

def plot_steric_factor_geometry():
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('off')
    
    # Reactive
    ax.text(0, 2.5, 'Reactive Orientation', fontsize=12, fontweight='bold', ha='center')
    c1 = Circle((-1, 2), 0.4, color='lightblue')
    c2 = Circle((-1, 2), 0.1, color='red') # Active site
    ax.add_patch(c1)
    ax.add_patch(c2)
    
    c3 = Circle((1, 2), 0.3, color='lightgreen')
    ax.add_patch(c3)
    
    ax.arrow(0.5, 2, -0.8, 0, head_width=0.1, head_length=0.1, fc='k', ec='k')
    
    # Non-reactive
    ax.text(4, 2.5, 'Non-Reactive Orientation', fontsize=12, fontweight='bold', ha='center')
    c4 = Circle((3, 2), 0.4, color='lightblue')
    c5 = Circle((2.7, 2), 0.1, color='red') # Active site facing away
    ax.add_patch(c4)
    ax.add_patch(c5)
    
    c6 = Circle((5, 2), 0.3, color='lightgreen')
    ax.add_patch(c6)
    
    ax.arrow(4.5, 2, -0.8, 0, head_width=0.1, head_length=0.1, fc='k', ec='k')
    ax.text(4, 1.3, 'Steric Factor $P < 1$', ha='center', fontsize=12)
    
    ax.set_xlim(-2, 6)
    ax.set_ylim(1, 3)
    save_plot('steric_factor_geometry.png')

def plot_harpoon_mechanism():
    fig, ax = plt.subplots(figsize=(8, 5))
    
    r = np.linspace(0.2, 1.5, 200) # nm
    
    V_covalent = np.zeros_like(r) 
    V_ionic = 1.79 - 1.44/r 
    
    ax.plot(r, V_covalent, 'b-', linewidth=2, label='Neutral: K + Br$_2$')
    ax.plot(r, V_ionic, 'r-', linewidth=2, label='Ionic: K$^+$ + Br$_2^-$')
    
    idx = np.argwhere(np.diff(np.sign(V_ionic - V_covalent))).flatten()
    if len(idx) > 0:
        rc = r[idx[0]]
        ax.plot(rc, V_covalent[idx[0]], 'ko', markersize=8)
        ax.annotate('Electron Jump', xy=(rc, 0), xytext=(rc+0.3, 1),
                    arrowprops=dict(facecolor='black', shrink=0.05))
        ax.axvline(rc, color='gray', linestyle='--')
        ax.text(rc, -5, r'$R^* \approx 0.8$ nm', fontsize=12, ha='center', backgroundcolor='white')
        
    ax.set_ylim(-6, 4)
    ax.set_xlim(0, 1.5)
    ax.set_xlabel('Distance r (nm)')
    ax.set_ylabel('Potential Energy (eV)')
    ax.set_title('Harpoon Mechanism: Potential Energy Curves')
    ax.legend()
    save_plot('harpoon_mechanism.png')

# ==========================================
# TOPIC 18B: DIFFUSION
# ==========================================

def plot_solvent_cage_trajectory():
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.grid(False)
    
    np.random.seed(42)
    n_steps = 1000
    x, y = np.zeros(n_steps), np.zeros(n_steps)
    
    for i in range(1, n_steps):
        dx = np.random.normal(0, 0.1)
        dy = np.random.normal(0, 0.1)
        fx = -0.05 * x[i-1]
        fy = -0.05 * y[i-1]
        x[i] = x[i-1] + dx + fx
        y[i] = y[i-1] + dy + fy
        
    ax.plot(x, y, 'b-', alpha=0.5, linewidth=1)
    ax.plot(x[0], y[0], 'go', label='Start')
    ax.plot(x[-1], y[-1], 'ro', label='End')
    
    cage = Circle((0, 0), 2.5, color='gray', fill=False, linestyle='--', linewidth=2, label='Solvent Cage')
    ax.add_patch(cage)
    
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_aspect('equal')
    ax.set_title('Solvent Cage Effect (Simulated Trajectory)')
    ax.legend()
    ax.axis('off')
    save_plot('solvent_cage_trajectory.png')

def plot_encounter_pair_dynamics():
    fig, ax = plt.subplots(figsize=(8, 4))
    
    t = np.linspace(0, 20, 200)
    # Oscillations in cage then escape
    r = 0.3 + 0.1 * np.sin(5*t) * np.exp(-0.1*t)
    mask = t > 15
    r[mask] = 0.3 + 0.1 * np.sin(5*15) * np.exp(-0.1*15) + 0.2*(t[mask]-15)
    
    ax.plot(t, r, 'b-', linewidth=2)
    ax.axvline(15, color='r', linestyle='--', label='Cage Escape')
    
    ax.set_xlabel('Time (ps)')
    ax.set_ylabel('Separation Distance (nm)')
    ax.set_title('Encounter Pair Dynamics')
    ax.legend()
    save_plot('encounter_pair_dynamics.png')

def plot_diffusion_vs_activation_energy():
    fig, ax = plt.subplots(figsize=(8, 5))
    
    x = np.linspace(0, 10, 100)
    y_diff = 0.5 * np.sin(2 * np.pi * x) + 0.5
    y_act = 5 * np.exp(-(x-5)**2 / 2)
    y = y_diff + y_act
    
    ax.plot(x, y, 'k-', linewidth=2)
    
    ax.annotate('Diffusion\nBarrier', xy=(1.2, 1.2), xytext=(1, 3),
                arrowprops=dict(facecolor='blue', shrink=0.05))
    ax.annotate('Activation\nBarrier', xy=(5, 5.5), xytext=(5, 7),
                arrowprops=dict(facecolor='red', shrink=0.05))
    
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('Diffusion vs Activation Control')
    save_plot('diffusion_vs_activation_energy.png')

def plot_rate_vs_viscosity():
    fig, ax = plt.subplots(figsize=(8, 5))
    
    inv_eta = np.linspace(0, 10, 100)
    k_diff = 1.0 * inv_eta
    k_act = np.ones_like(inv_eta) * 5.0
    k_mixed = (k_diff * k_act) / (k_diff + k_act)
    
    ax.plot(inv_eta, k_diff, 'b--', label='Diffusion Limit')
    ax.plot(inv_eta, k_act, 'r--', label='Activation Limit')
    ax.plot(inv_eta, k_mixed, 'k-', linewidth=2, label='Observed Rate')
    
    ax.set_xlabel(r'Fluidity ($1/\eta$)')
    ax.set_ylabel('Rate Constant $k$')
    ax.set_title('Viscosity Dependence of Reaction Rate')
    ax.legend()
    save_plot('rate_vs_viscosity.png')

def plot_smoluchowski_profile():
    fig, ax = plt.subplots(figsize=(8, 5))
    
    r = np.linspace(1, 10, 100)
    R_star = 1.0
    c_bulk = 1.0
    c = c_bulk * (1 - R_star/r)
    
    ax.plot(r, c, 'b-', linewidth=2)
    ax.axhline(c_bulk, color='k', linestyle='--', label='Bulk Concentration')
    ax.axvline(R_star, color='r', linestyle=':', label='Contact Radius R*')
    ax.fill_between(r, 0, c, alpha=0.1, color='blue')
    
    ax.set_xlabel('Distance r')
    ax.set_ylabel('Concentration [B]')
    ax.set_title('Smoluchowski Concentration Profile')
    ax.set_ylim(0, 1.2)
    ax.set_xlim(0, 10)
    ax.legend()
    save_plot('smoluchowski_profile.png')

# ==========================================
# TOPIC 18C: TST
# ==========================================

def plot_reaction_coordinate_tst():
    fig, ax = plt.subplots(figsize=(8, 5))
    
    x = np.linspace(-2, 2, 100)
    y = -x**2 + 4
    
    ax.plot(x, y, 'k-', linewidth=2)
    
    ax.text(-1.5, 0.5, 'Reactants\n(A+B)', ha='center')
    ax.text(1.5, 0.5, 'Products\n(P)', ha='center')
    ax.text(0, 4.2, 'Transition State\n($C^\ddagger$)', ha='center')
    
    ax.annotate(r'$\Delta G^\ddagger$', xy=(0, 4), xytext=(0.5, 2),
                arrowprops=dict(arrowstyle='<->'))
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('Reaction Coordinate')
    ax.set_ylabel('Free Energy')
    ax.set_title('Transition State Theory Profile')
    save_plot('reaction_coordinate_tst.png')

def plot_eyring_plot():
    fig, ax = plt.subplots(figsize=(8, 5))
    
    inv_T = np.linspace(0.002, 0.004, 100)
    ln_k_T = 25 - 6000 * inv_T
    
    ax.plot(inv_T, ln_k_T, 'b-', linewidth=2)
    
    ax.text(0.003, 7, r'Slope = $-\Delta H^\ddagger/R$', fontsize=12, rotation=-20)
    ax.text(0.0021, 12, r'Intercept = $\ln(k_B/h) + \Delta S^\ddagger/R$', fontsize=12)
    
    ax.set_xlabel(r'$1/T$ (K$^{-1}$)')
    ax.set_ylabel(r'$\ln(k/T)$')
    ax.set_title('Eyring Plot')
    save_plot('eyring_plot.png')

def plot_kinetic_salt_effect():
    fig, ax = plt.subplots(figsize=(8, 5))
    
    sqrt_I = np.linspace(0, 0.5, 100)
    
    # Debye-Huckel Limiting Law: log k = log k0 + 2AzAzB sqrt(I)
    # A = 0.509 for water at 25 C
    A = 0.509
    
    y_pos = 0 + 2 * A * 1 * 1 * sqrt_I # Like charges (+1, +1)
    y_neg = 0 + 2 * A * 1 * (-1) * sqrt_I # Opposite charges (+1, -1)
    y_zero = np.zeros_like(sqrt_I) # Neutral
    
    ax.plot(sqrt_I, y_pos, 'b-', label=r'$z_A z_B = +1$ (Like)')
    ax.plot(sqrt_I, y_neg, 'r-', label=r'$z_A z_B = -1$ (Opposite)')
    ax.plot(sqrt_I, y_zero, 'k--', label=r'$z_A z_B = 0$ (Neutral)')
    
    ax.set_xlabel(r'$\sqrt{I}$ (M$^{1/2}$)')
    ax.set_ylabel(r'$\log(k/k^\circ)$')
    ax.set_title('Kinetic Salt Effect (Water, 25$^\circ$C)')
    ax.legend()
    save_plot('kinetic_salt_effect.png')

def plot_lennard_jones():
    fig, ax = plt.subplots(figsize=(8, 5))
    
    r = np.linspace(0.8, 3, 200)
    sigma = 1.0
    epsilon = 1.0
    
    # V(r) = 4*epsilon*((sigma/r)^12 - (sigma/r)^6)
    V = 4 * epsilon * ((sigma/r)**12 - (sigma/r)**6)
    
    ax.plot(r, V, 'k-', linewidth=2)
    ax.axhline(0, color='gray', linestyle='--')
    ax.axvline(sigma, color='r', linestyle=':', label=r'$\sigma$ (Collision Diameter)')
    ax.axvline(2**(1/6)*sigma, color='b', linestyle=':', label=r'$r_m$ (Min Energy)')
    
    ax.set_ylim(-1.5, 2)
    ax.set_xlim(0.5, 3)
    ax.set_xlabel(r'Distance $r/\sigma$')
    ax.set_ylabel(r'Potential Energy $V/\epsilon$')
    ax.set_title('Lennard-Jones Potential')
    ax.legend()
    save_plot('lennard_jones_potential.png')

def plot_kie_zpe():
    fig, ax = plt.subplots(figsize=(8, 6))
    
    x = np.linspace(-2, 2, 100)
    # Morse potential approx: V(x) = D(1-exp(-a*x))^2
    V = 10 * (1 - np.exp(-x))**2
    ax.plot(x, V, 'k-', linewidth=2)
    
    # ZPE levels (approx harmonic)
    # E_n = (n+1/2)hbar*omega
    # omega_D = omega_H / sqrt(2) -> E_D = E_H / sqrt(2)
    E_H = 1.0
    E_D = 1.0 / np.sqrt(2)
    
    ax.hlines(E_H, -0.5, 0.5, colors='b', linewidth=2, label='C-H ZPE')
    ax.hlines(E_D, -0.5, 0.5, colors='r', linewidth=2, label='C-D ZPE')
    
    # Activation Barrier (Transition State)
    E_TS = 8.0
    ax.hlines(E_TS, 2, 3, colors='k', linestyle='--')
    
    # Arrows for Ea
    ax.annotate('', xy=(2.5, E_TS), xytext=(0, E_H), 
                arrowprops=dict(arrowstyle='<->', color='blue', lw=1.5))
    ax.text(1.2, (E_TS+E_H)/2, r'$E_a^H$', color='blue')
    
    ax.annotate('', xy=(2.7, E_TS), xytext=(0, E_D), 
                arrowprops=dict(arrowstyle='<->', color='red', lw=1.5))
    ax.text(1.5, (E_TS+E_D)/2 - 1, r'$E_a^D$', color='red')
    
    ax.set_ylim(0, 12)
    ax.set_xlim(-1, 3)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('Bond Length')
    ax.set_ylabel('Potential Energy')
    ax.set_title('Kinetic Isotope Effect (Zero Point Energy)')
    ax.legend()
    save_plot('kie_zpe.png')

def plot_quantum_tunneling_comparison():
    fig, ax = plt.subplots(figsize=(8, 5))
    
    x = np.linspace(-3, 3, 100)
    y = np.exp(-x**2) * 5
    
    ax.plot(x, y, 'k-', linewidth=2)
    
    # Over
    ax.annotate('Classical Crossing', xy=(0, 5), xytext=(0, 6),
                arrowprops=dict(facecolor='blue', shrink=0.05))
    
    # Through
    ax.annotate('Tunneling', xy=(1, 2), xytext=(-2, 2),
                arrowprops=dict(facecolor='red', shrink=0.05))
    ax.hlines(2, -3, 3, colors='red', linestyles='--')
    
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('Classical Crossing vs Quantum Tunneling')
    save_plot('quantum_tunneling_comparison.png')

def plot_free_energy_entropy():
    fig, ax = plt.subplots(figsize=(8, 5))
    
    x = np.linspace(0, 4, 100)
    # Base profile
    y_base = 4 * np.exp(-(x-2)**2)
    
    # High entropy (lower G)
    y_highS = y_base - 1.0 * np.exp(-(x-2)**2)
    # Low entropy (higher G)
    y_lowS = y_base + 1.0 * np.exp(-(x-2)**2)
    
    ax.plot(x, y_highS, 'r--', label=r'$\Delta S^\ddagger > 0$ (Loose TS)')
    ax.plot(x, y_lowS, 'b-', label=r'$\Delta S^\ddagger < 0$ (Tight TS)')
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('Reaction Coordinate')
    ax.set_ylabel('Free Energy $G$')
    ax.set_title('Effect of Activation Entropy on Barrier Height')
    ax.legend()
    save_plot('free_energy_entropy.png')

# ==========================================
# TOPIC 18D: DYNAMICS
# ==========================================

def plot_molecular_beam_setup():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axis('off')
    
    # Source A
    rect_a = Rectangle((-4, 1), 1, 1, facecolor='lightgray', edgecolor='k')
    ax.add_patch(rect_a)
    ax.text(-3.5, 1.5, 'Source A', ha='center', va='center')
    ax.arrow(-3, 1.5, 2, 0, head_width=0.2, fc='k')
    
    # Source B
    rect_b = Rectangle((-1, -2), 1, 1, facecolor='lightgray', edgecolor='k')
    ax.add_patch(rect_b)
    ax.text(-0.5, -1.5, 'Source B', ha='center', va='center')
    ax.arrow(-0.5, -1, 0, 2, head_width=0.2, fc='k')
    
    # Collision
    circle = Circle((-0.5, 1.5), 0.2, color='red')
    ax.add_patch(circle)
    ax.text(-0.5, 1.8, 'Collision Zone', ha='center')
    
    # Detector
    det = Arc((-0.5, 1.5), 4, 4, theta1=-45, theta2=45, linestyle='--')
    ax.add_patch(det)
    rect_d = Rectangle((1.5, 1.5), 0.5, 0.5, facecolor='gold', edgecolor='k')
    ax.add_patch(rect_d)
    ax.text(1.75, 1.75, 'Det', ha='center', va='center')
    ax.text(1.5, 2.2, 'Rotatable Detector', ha='center')
    
    ax.set_xlim(-5, 3)
    ax.set_ylim(-3, 3)
    ax.set_title('Molecular Beam Apparatus Schematic')
    save_plot('molecular_beam_setup.png')

def plot_velocity_selection():
    fig, ax = plt.subplots(figsize=(8, 5))
    
    v = np.linspace(0, 5, 100)
    # Maxwell
    y_mb = v**2 * np.exp(-v**2)
    # Supersonic
    y_ss = np.exp(-(v-2.5)**2 / 0.05)
    
    ax.plot(v, y_mb, 'b--', label='Maxwell-Boltzmann (Thermal)')
    ax.plot(v, y_ss, 'r-', label='Supersonic Expansion (Monochromatic)')
    
    ax.set_xlabel('Velocity')
    ax.set_ylabel('Probability')
    ax.set_title('Velocity Selection')
    ax.legend()
    save_plot('velocity_selection.png')

def plot_differential_cross_section_polar():
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='polar')
    
    theta = np.linspace(0, 2*np.pi, 200)
    # Forward scattering
    r_fwd = 1 + 2 * np.cos(theta)
    r_fwd[r_fwd < 0] = 0
    
    # Backward scattering
    r_bwd = 1 - 0.8 * np.cos(theta)
    
    ax.plot(theta, r_fwd, 'b-', label='Forward (Stripping)')
    ax.plot(theta, r_bwd, 'r--', label='Backward (Rebound)')
    
    ax.set_title('Differential Cross-Section (Polar Plot)', va='bottom')
    ax.legend(loc='lower right')
    save_plot('differential_cross_section_polar.png')

def plot_newton_diagram():
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.axis('off')
    
    # CM Circle
    circle = Circle((0, 0), 2, color='lightblue', alpha=0.3)
    ax.add_patch(circle)
    ax.text(0, -2.3, 'CM Frame', ha='center', color='blue')
    
    # Lab Origin
    ax.plot(-3, 0, 'ko')
    ax.text(-3, -0.3, 'Lab Origin')
    
    # Vectors
    ax.arrow(-3, 0, 3, 0, head_width=0.1, fc='k', ec='k', length_includes_head=True)
    ax.text(-1.5, 0.1, r'$\vec{v}_{CM}$', ha='center')
    
    # Product vector in CM
    ax.arrow(0, 0, 1.4, 1.4, head_width=0.1, fc='b', ec='b', length_includes_head=True)
    ax.text(0.5, 0.8, r'$\vec{u}_{prod}$', color='blue')
    
    # Product vector in Lab
    ax.arrow(-3, 0, 4.4, 1.4, head_width=0.1, fc='r', ec='r', length_includes_head=True)
    ax.text(-0.5, 1.5, r'$\vec{v}_{lab}$', color='red')
    
    ax.set_xlim(-4, 3)
    ax.set_ylim(-3, 3)
    ax.set_title('Newton Diagram')
    save_plot('newton_diagram.png')

def plot_pes_contour_leps():
    fig, ax = plt.subplots(figsize=(7, 6))
    
    x = np.linspace(0.5, 4, 100)
    y = np.linspace(0.5, 4, 100)
    X, Y = np.meshgrid(x, y)
    
    # Mock LEPS surface
    Z = 2*np.exp(-2*(X-1)**2) + 2*np.exp(-2*(Y-1)**2) + 5*np.exp(-(X-2)**2-(Y-2)**2) - 2
    
    # Contour
    cp = ax.contour(X, Y, Z, levels=20, cmap='jet')
    fig.colorbar(cp, label='Potential Energy')
    
    ax.set_xlabel(r'$R_{AB}$')
    ax.set_ylabel(r'$R_{BC}$')
    ax.set_title('Potential Energy Surface (Contour)')
    ax.text(1, 3.5, 'Reactants', ha='center', color='white', fontweight='bold')
    ax.text(3.5, 1, 'Products', ha='center', color='white', fontweight='bold')
    ax.plot(2, 2, 'wx', markersize=10)
    ax.text(2.1, 2.1, 'TS', color='white', fontweight='bold')
    
    save_plot('pes_contour_leps.png')

def plot_pes_3d_surface():
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    x = np.linspace(-2, 2, 50)
    y = np.linspace(-2, 2, 50)
    X, Y = np.meshgrid(x, y)
    Z = X**2 - Y**2 
    
    surf = ax.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.8, edgecolor='none')
    
    path_x = np.linspace(-2, 2, 50)
    path_y = np.zeros_like(path_x)
    path_z = path_x**2
    ax.plot(path_x, path_y, path_z, 'k--', linewidth=3, label='Reaction Path')
    ax.scatter([0], [0], [0], color='green', s=100, label='Transition State')
    
    ax.set_xlabel('Coordinate 1')
    ax.set_ylabel('Coordinate 2')
    ax.set_zlabel('Energy')
    ax.set_title('PES Topology (Saddle Point)')
    ax.legend()
    save_plot('pes_3d_surface.png')

def plot_trajectory_types():
    fig, ax = plt.subplots(figsize=(7, 6))
    
    # Background contours (schematic)
    circle1 = Circle((0, 0), 1, color='lightgray', alpha=0.5)
    ax.add_patch(circle1)
    
    # Reactive
    ax.plot([-2, 0, 2], [2, 0, -2], 'b-', linewidth=2, label='Reactive')
    
    # Non-reactive
    ax.plot([-2, -0.5, -2], [1.5, 0.5, -0.5], 'r--', linewidth=2, label='Non-Reactive (Reflection)')
    
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_xlabel(r'$R_{AB}$')
    ax.set_ylabel(r'$R_{BC}$')
    ax.set_title('Trajectory Types')
    ax.legend()
    save_plot('trajectory_types.png')

def plot_attractive_vs_repulsive():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    x = np.linspace(0, 10, 100)
    
    # Attractive (Early)
    y1 = 5 * np.exp(-(x-3)**2)
    ax1.plot(x, y1, 'b-', linewidth=2)
    ax1.axvline(3, color='k', linestyle='--')
    ax1.text(3, 5.2, 'Early Barrier', ha='center')
    ax1.set_title('Attractive Surface (Early Barrier)')
    ax1.set_xlabel('Reaction Coordinate')
    ax1.set_ylabel('Energy')
    
    # Repulsive (Late)
    y2 = 5 * np.exp(-(x-7)**2)
    ax2.plot(x, y2, 'r-', linewidth=2)
    ax2.axvline(7, color='k', linestyle='--')
    ax2.text(7, 5.2, 'Late Barrier', ha='center')
    ax2.set_title('Repulsive Surface (Late Barrier)')
    ax2.set_xlabel('Reaction Coordinate')
    
    save_plot('attractive_vs_repulsive.png')

# ==========================================
# TOPIC 18E: ELECTRON TRANSFER
# ==========================================

def plot_marcus_parabolas_annotated():
    fig, ax = plt.subplots(figsize=(8, 6))
    
    q = np.linspace(-1, 2, 100)
    lambda_val = 1.0
    dG0 = -0.5
    
    GR = lambda_val * q**2
    GP = lambda_val * (q - 1)**2 + dG0
    
    ax.plot(q, GR, 'b-', label='Reactants (R)')
    ax.plot(q, GP, 'r-', label='Products (P)')
    
    ax.annotate(r'$\lambda$', xy=(1, 0), xytext=(1, 1), arrowprops=dict(arrowstyle='<->'))
    ax.annotate(r'$\Delta G^\circ$', xy=(1.5, 0), xytext=(1.5, dG0), arrowprops=dict(arrowstyle='<->'))
    
    ax.set_xlabel('Reaction Coordinate')
    ax.set_ylabel('Free Energy')
    ax.set_title('Marcus Theory Parabolas')
    ax.legend()
    save_plot('marcus_parabolas_annotated.png')

def plot_marcus_regimes_comparison():
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    
    q = np.linspace(-1, 2, 100)
    lam = 1.0
    GR = lam * q**2
    
    def plot_regime(ax, dG0, title):
        GP = lam * (q - 1)**2 + dG0
        ax.plot(q, GR, 'b-', label='R')
        ax.plot(q, GP, 'r-', label='P')
        q_star = (lam + dG0) / (2*lam)
        E_star = lam * q_star**2
        ax.plot(q_star, E_star, 'ko')
        ax.set_title(title)
        ax.set_ylim(-2, 3)
        ax.set_yticks([])
        ax.set_xticks([])
        if E_star > 0:
            ax.annotate('', xy=(q_star, E_star), xytext=(q_star, 0), arrowprops=dict(arrowstyle='<->'))
    
    plot_regime(ax1, -0.5, 'Normal Region')
    plot_regime(ax2, -1.0, 'Barrierless')
    plot_regime(ax3, -2.0, 'Inverted Region')
    
    plt.tight_layout()
    save_plot('marcus_regimes_comparison.png')

def plot_distance_decay():
    fig, ax = plt.subplots(figsize=(8, 5))
    
    r = np.linspace(0, 20, 100)
    beta1 = 1.4
    beta2 = 0.5
    k1 = np.exp(-beta1 * r)
    k2 = np.exp(-beta2 * r)
    
    ax.semilogy(r, k1, 'b-', label=r'Protein ($\beta \approx 1.4$ $\AA^{-1}$)')
    ax.semilogy(r, k2, 'r-', label=r'Conjugated Bridge ($\beta \approx 0.5$ $\AA^{-1}$)')
    
    ax.set_xlabel(r'Distance ($\AA$)')
    ax.set_ylabel('Relative Rate')
    ax.set_title('Distance Dependence of ET')
    ax.legend()
    save_plot('distance_decay.png')

if __name__ == "__main__":
    try:
        print("Generating all figures...")
        
        # 18A
        plot_collision_cylinder()
        plot_maxwell_boltzmann_speeds()
        plot_maxwell_boltzmann_energy()
        plot_reactive_cross_section()
        plot_arrhenius_plot()
        plot_steric_factor_geometry()
        plot_harpoon_mechanism()
        plot_lennard_jones()
        
        # 18B
        plot_solvent_cage_trajectory()
        plot_encounter_pair_dynamics()
        plot_diffusion_vs_activation_energy()
        plot_rate_vs_viscosity()
        plot_smoluchowski_profile()
        
        # 18C
        plot_reaction_coordinate_tst()
        plot_eyring_plot()
        plot_kinetic_salt_effect()
        plot_kie_zpe()
        plot_quantum_tunneling_comparison()
        plot_free_energy_entropy()
        
        # 18D
        plot_molecular_beam_setup()
        plot_velocity_selection()
        plot_differential_cross_section_polar()
        plot_newton_diagram()
        plot_pes_contour_leps()
        plot_pes_3d_surface()
        plot_trajectory_types()
        plot_attractive_vs_repulsive()
        
        # 18E
        plot_marcus_parabolas_annotated()
        plot_marcus_regimes_comparison()
        plot_distance_decay()
        
        print("All 29 figures generated successfully!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
