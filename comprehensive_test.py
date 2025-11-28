"""
Comprehensive Test Suite for Paper Integration Project

Tests all modules, data files, and notebook integrations
"""

import sys
import os
import json
import traceback
from pathlib import Path

# Add modules to path
sys.path.append('modules')

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for testing
import matplotlib.pyplot as plt

# Track test results
test_results = {
    'passed': [],
    'failed': [],
    'warnings': []
}

def test_section(name):
    """Decorator for test sections"""
    print(f"\n{'='*80}")
    print(f"{name}")
    print('='*80)

def test_result(test_name, passed, message=""):
    """Record test result"""
    if passed:
        test_results['passed'].append(test_name)
        print(f"  [PASS] {test_name}")
        if message:
            print(f"         {message}")
    else:
        test_results['failed'].append(test_name)
        print(f"  [FAIL] {test_name}")
        if message:
            print(f"         {message}")

# ============================================================================
# TEST 1: Module Import Tests
# ============================================================================
test_section("TEST 1: MODULE IMPORTS")

try:
    from leps_surface import LEPSSurface
    test_result("Import leps_surface", True)
except Exception as e:
    test_result("Import leps_surface", False, str(e))

try:
    from visualization import plot_pes_3d, plot_pes_contour, plot_morse_curve
    test_result("Import visualization", True)
except Exception as e:
    test_result("Import visualization", False, str(e))

try:
    from trajectory import ClassicalTrajectory
    test_result("Import trajectory", True)
except Exception as e:
    test_result("Import trajectory", False, str(e))

try:
    from transition_state import TransitionStateOptimizer
    test_result("Import transition_state", True)
except Exception as e:
    test_result("Import transition_state", False, str(e))

# ============================================================================
# TEST 2: Data File Integrity
# ============================================================================
test_section("TEST 2: DATA FILE INTEGRITY")

data_tests = [
    ('data/tst/morse_parameters.csv', 8, ['molecule', 'D_e_kJ_mol', 'R_e_angstrom']),
    ('data/tst/prodrug_kinetics_temperature.csv', 18, ['candidate', 'temperature_K', 'rate_constant_s_inv']),
    ('data/tst/prodrug_kie_data.csv', 6, ['candidate', 'isotope', 'rate_constant_s_inv']),
    ('data/tst/prodrug_hammett_data.csv', 10, ['substituent', 'sigma_para', 'rate_constant_s_inv'])
]

for filepath, expected_rows, required_cols in data_tests:
    try:
        df = pd.read_csv(filepath)

        # Check row count
        if df.shape[0] == expected_rows:
            test_result(f"Data file {Path(filepath).name} - row count", True,
                       f"{df.shape[0]} rows")
        else:
            test_result(f"Data file {Path(filepath).name} - row count", False,
                       f"Expected {expected_rows}, got {df.shape[0]}")

        # Check required columns
        missing_cols = [col for col in required_cols if col not in df.columns]
        if not missing_cols:
            test_result(f"Data file {Path(filepath).name} - columns", True)
        else:
            test_result(f"Data file {Path(filepath).name} - columns", False,
                       f"Missing: {missing_cols}")

    except Exception as e:
        test_result(f"Data file {Path(filepath).name}", False, str(e))

# ============================================================================
# TEST 3: LEPS Surface Functionality
# ============================================================================
test_section("TEST 3: LEPS SURFACE FUNCTIONALITY")

try:
    # Test 3.1: Surface initialization
    surface = LEPSSurface('HI', 'HI', 'I2', K_sato=0.0)
    test_result("LEPS surface initialization", True)

    # Test 3.2: Parameter loading
    has_params = all(k in surface.params for k in ['AB', 'BC', 'AC'])
    test_result("LEPS parameter loading", has_params)

    # Test 3.3: Single point energy calculation
    E = surface.leps_potential(1.6, 2.5, 3.0)
    expected_E = -231.80
    energy_ok = abs(E - expected_E) < 1.0
    test_result("LEPS single point energy", energy_ok,
               f"E = {E:.2f} kJ/mol (expected ~{expected_E})")

    # Test 3.4: 2D surface generation
    R_AB = np.linspace(1.5, 3.5, 30)
    R_BC = np.linspace(1.5, 3.5, 30)
    R_AB_grid, R_BC_grid, V_grid = surface.energy_surface_2d(R_AB, R_BC, angle_deg=180.0)

    surface_ok = (V_grid.shape == (30, 30) and
                  not np.any(np.isnan(V_grid)) and
                  not np.any(np.isinf(V_grid)))
    test_result("LEPS 2D surface generation", surface_ok,
               f"Shape: {V_grid.shape}, Range: [{V_grid.min():.1f}, {V_grid.max():.1f}]")

    # Test 3.5: Morse potential
    R_range = np.linspace(1.0, 4.0, 50)
    params = surface.params['AB']
    V_morse = surface.morse_potential(R_range, params['D_e'], params['R_e'], params['beta'])
    morse_ok = len(V_morse) == 50 and not np.any(np.isnan(V_morse))
    test_result("LEPS Morse potential", morse_ok)

except Exception as e:
    test_result("LEPS surface tests", False, str(e))
    traceback.print_exc()

# ============================================================================
# TEST 4: Transition State Optimization
# ============================================================================
test_section("TEST 4: TRANSITION STATE OPTIMIZATION")

try:
    # Test 4.1: Optimizer initialization
    optimizer = TransitionStateOptimizer(surface, tolerance=1e-6, max_iterations=50)
    test_result("TS optimizer initialization", True)

    # Test 4.2: Gradient calculation
    grad = optimizer.calculate_gradient(1.9, 1.9)
    gradient_ok = len(grad) == 2 and not np.any(np.isnan(grad))
    test_result("TS gradient calculation", gradient_ok)

    # Test 4.3: Hessian calculation
    H = optimizer.calculate_hessian(1.9, 1.9)
    hessian_ok = H.shape == (2, 2) and not np.any(np.isnan(H))
    test_result("TS Hessian calculation", hessian_ok)

    # Test 4.4: Newton-Raphson optimization
    result = optimizer.optimize_saddle_point(1.9, 1.9, verbose=False)

    converged = result['converged']
    test_result("TS optimization convergence", converged,
               f"Iterations: {result['iterations']}")

    # Test 4.5: Saddle point verification
    eigenvals = result['eigenvalues']
    is_saddle = eigenvals[0] < 0 and eigenvals[1] > 0
    test_result("TS saddle point verification", is_saddle,
               f"Eigenvalues: [{eigenvals[0]:.1f}, {eigenvals[1]:.1f}]")

    # Test 4.6: Symmetric geometry for symmetric reaction
    symmetric = abs(result['R_AB'] - result['R_BC']) < 0.001
    test_result("TS symmetric geometry (H+HI)", symmetric,
               f"R_AB={result['R_AB']:.4f}, R_BC={result['R_BC']:.4f}")

    # Test 4.7: Force constants
    force_const = optimizer.calculate_force_constants(result['R_AB'], result['R_BC'])
    fc_ok = 'k_AB' in force_const and 'k_BC' in force_const
    test_result("TS force constant calculation", fc_ok)

except Exception as e:
    test_result("TS optimization tests", False, str(e))
    traceback.print_exc()

# ============================================================================
# TEST 5: Classical Trajectories
# ============================================================================
test_section("TEST 5: CLASSICAL TRAJECTORY SIMULATIONS")

try:
    # Test 5.1: Trajectory calculator initialization
    traj_calc = ClassicalTrajectory(surface, 'H', 'H', 'I', dt=0.010)
    test_result("Trajectory calculator init", True)

    # Test 5.2: Force calculation
    F_AB, F_BC, F_AC = traj_calc.calculate_forces(1.9, 1.9, 3.8)
    forces_ok = all(not np.isnan(f) and not np.isinf(f) for f in [F_AB, F_BC, F_AC])
    test_result("Trajectory force calculation", forces_ok)

    # Test 5.3: Single trajectory run
    R_AB_0, R_BC_0, R_AC_0 = 3.0, 1.609, 4.609
    v_AB_0, v_BC_0, v_AC_0 = -0.05, 0.0, -0.05

    traj_result = traj_calc.run_trajectory(R_AB_0, R_BC_0, R_AC_0,
                                           v_AB_0, v_BC_0, v_AC_0,
                                           max_time=100.0, save_interval=5)

    traj_ok = len(traj_result['time']) > 0
    test_result("Trajectory execution", traj_ok,
               f"Duration: {traj_result['time'][-1]:.1f} fs")

    # Test 5.4: Energy conservation
    energy_drift = abs(traj_result['energy_drift'])
    excellent_conservation = energy_drift < 0.01
    test_result("Trajectory energy conservation", excellent_conservation,
               f"Drift: {energy_drift:.4f}% (target: <0.01%)")

    # Test 5.5: Outcome classification
    has_outcome = 'outcome' in traj_result
    test_result("Trajectory outcome classification", has_outcome,
               f"Outcome: {traj_result.get('outcome', 'unknown')}")

    # Test 5.6: Data integrity
    data_ok = all(len(traj_result[key]) == len(traj_result['time'])
                  for key in ['R_AB', 'R_BC', 'V', 'T', 'E_total'])
    test_result("Trajectory data integrity", data_ok)

except Exception as e:
    test_result("Trajectory tests", False, str(e))
    traceback.print_exc()

# ============================================================================
# TEST 6: Visualization Functions
# ============================================================================
test_section("TEST 6: VISUALIZATION FUNCTIONS")

try:
    # Test 6.1: 3D surface plot (no display, just test it runs)
    fig_3d, ax_3d = plot_pes_3d(R_AB_grid, R_BC_grid, V_grid,
                                title="Test", xlabel="X", ylabel="Y")
    test_result("Visualization 3D surface plot", fig_3d is not None)
    plt.close(fig_3d)

    # Test 6.2: 2D contour plot
    fig_2d, ax_2d = plot_pes_contour(R_AB_grid, R_BC_grid, V_grid,
                                     title="Test", xlabel="X", ylabel="Y")
    test_result("Visualization 2D contour plot", fig_2d is not None)
    plt.close(fig_2d)

    # Test 6.3: Morse curve plot
    R_range = np.linspace(1.0, 4.0, 100)
    V_morse = -100 * np.exp(-2*(R_range-1.6)) + 50
    fig_morse, ax_morse = plot_morse_curve(R_range, V_morse, molecule_name="Test")
    test_result("Visualization Morse curve plot", fig_morse is not None)
    plt.close(fig_morse)

except Exception as e:
    test_result("Visualization tests", False, str(e))
    traceback.print_exc()

# ============================================================================
# TEST 7: Notebook Integration
# ============================================================================
test_section("TEST 7: NOTEBOOK INTEGRATION")

notebooks = {
    'notebooks/03_Transition_State_Theory.ipynb': [
        'INVESTIGATION 4',
        'Potential Energy Surface',
        'Newton-Raphson',
        'LEPS'
    ],
    'notebooks/04_Molecular_Dynamics.ipynb': [
        'INVESTIGATION 4',
        'Classical Trajectory',
        'Monte Carlo',
        'Velocity Verlet'
    ],
    'notebooks/06_Integration_Projects.ipynb': [
        'PROJECT 4',
        'Complete Reaction Dynamics',
        'H + HI'
    ]
}

for nb_path, keywords in notebooks.items():
    try:
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)

        # Check notebook structure
        has_cells = 'cells' in nb and len(nb['cells']) > 0
        test_result(f"Notebook {Path(nb_path).name} - structure", has_cells,
                   f"{len(nb.get('cells', []))} cells")

        # Check for keywords
        all_content = ' '.join(''.join(cell.get('source', []))
                               for cell in nb.get('cells', []))

        for keyword in keywords:
            found = keyword.lower() in all_content.lower()
            test_result(f"Notebook {Path(nb_path).name} - '{keyword}'", found)

    except Exception as e:
        test_result(f"Notebook {Path(nb_path).name}", False, str(e))

# ============================================================================
# TEST 8: Integration & Edge Cases
# ============================================================================
test_section("TEST 8: INTEGRATION & EDGE CASES")

try:
    # Test 8.1: Different K_sato values
    surface_k0 = LEPSSurface('HI', 'HI', 'I2', K_sato=0.0)
    surface_k03 = LEPSSurface('HI', 'HI', 'I2', K_sato=0.3)
    E_k0 = surface_k0.leps_potential(1.9, 1.9, 3.8)
    E_k03 = surface_k03.leps_potential(1.9, 1.9, 3.8)
    k_effect = E_k0 != E_k03
    test_result("LEPS K_sato parameter effect", k_effect,
               f"E(K=0)={E_k0:.1f}, E(K=0.3)={E_k03:.1f}")

    # Test 8.2: Different molecular systems
    try:
        surface_hf = LEPSSurface('HF', 'HF', 'F2', K_sato=0.0)
        test_result("LEPS different molecules (H+HF)", True)
    except:
        test_result("LEPS different molecules (H+HF)", False)

    # Test 8.3: Batch trajectory consistency
    results_batch = []
    for _ in range(5):
        res = traj_calc.run_trajectory(3.0, 1.609, 4.609,
                                       -0.05, 0.0, -0.05,
                                       max_time=50.0, save_interval=10)
        results_batch.append(res['energy_drift'])

    consistent = all(abs(drift) < 0.01 for drift in results_batch)
    test_result("Trajectory batch consistency", consistent,
               f"Avg drift: {np.mean(np.abs(results_batch)):.4f}%")

except Exception as e:
    test_result("Integration tests", False, str(e))
    traceback.print_exc()

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print(f"\n\n{'='*80}")
print("COMPREHENSIVE TEST SUMMARY")
print('='*80)

total_tests = len(test_results['passed']) + len(test_results['failed'])
pass_rate = len(test_results['passed']) / total_tests * 100 if total_tests > 0 else 0

print(f"\nTotal Tests Run: {total_tests}")
print(f"Passed: {len(test_results['passed'])} ({pass_rate:.1f}%)")
print(f"Failed: {len(test_results['failed'])}")

if test_results['failed']:
    print(f"\nFailed Tests:")
    for test in test_results['failed']:
        print(f"  - {test}")
else:
    print(f"\n[SUCCESS] ALL TESTS PASSED!")

print(f"\n{'='*80}")

# Return exit code
sys.exit(0 if not test_results['failed'] else 1)
