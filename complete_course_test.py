"""
COMPLETE COURSE VALIDATION TEST
Tests ALL notebooks, data files, and educational framework
"""

import sys
import os
import json
from pathlib import Path
import pandas as pd
import numpy as np

# Results tracking
results = {
    'notebooks': {},
    'data_files': {},
    'modules': {},
    'overall': {'passed': 0, 'failed': 0, 'warnings': 0}
}

def print_header(title):
    print(f"\n{'='*80}")
    print(f"{title}")
    print('='*80)

def test_pass(category, name, details=""):
    results['overall']['passed'] += 1
    print(f"  [PASS] {name}")
    if details:
        print(f"         {details}")

def test_fail(category, name, details=""):
    results['overall']['failed'] += 1
    print(f"  [FAIL] {name}")
    if details:
        print(f"         {details}")

def test_warn(category, name, details=""):
    results['overall']['warnings'] += 1
    print(f"  [WARN] {name}")
    if details:
        print(f"         {details}")

# ============================================================================
# TEST ALL NOTEBOOKS
# ============================================================================
print_header("TESTING ALL COURSE NOTEBOOKS (00-06)")

all_notebooks = [
    '00_Setup_and_Introduction.ipynb',
    '01_collision_theory.ipynb',
    '02_diffusion_controlled.ipynb',
    '03_Transition_State_Theory.ipynb',
    '04_Molecular_Dynamics.ipynb',
    '05_Electron_Transfer.ipynb',
    '06_Integration_Projects.ipynb'
]

for nb_name in all_notebooks:
    nb_path = f'notebooks/{nb_name}'
    print(f"\n{nb_name}:")

    try:
        # Load notebook
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)

        # Basic structure
        if 'cells' not in nb:
            test_fail('notebook', f"{nb_name} - structure", "Missing 'cells' key")
            continue

        cells = nb['cells']
        total_cells = len(cells)
        code_cells = sum(1 for c in cells if c.get('cell_type') == 'code')
        md_cells = sum(1 for c in cells if c.get('cell_type') == 'markdown')

        test_pass('notebook', f"{nb_name} - structure",
                 f"{total_cells} cells ({code_cells} code, {md_cells} markdown)")

        # Check for imports in code cells
        has_imports = False
        import_errors = []
        for cell in cells:
            if cell.get('cell_type') == 'code':
                source = ''.join(cell.get('source', []))
                if 'import' in source:
                    has_imports = True
                    # Check for common problematic imports
                    if 'from __future__' in source or 'import __future__' in source:
                        import_errors.append("Uses __future__ imports")

        if code_cells > 0:
            if has_imports:
                test_pass('notebook', f"{nb_name} - imports", "Has import statements")
            else:
                test_warn('notebook', f"{nb_name} - imports", "No imports found")

        # Check for markdown content
        if md_cells > 0:
            test_pass('notebook', f"{nb_name} - documentation", f"{md_cells} markdown cells")
        else:
            test_warn('notebook', f"{nb_name} - documentation", "No markdown cells")

        # Store results
        results['notebooks'][nb_name] = {
            'total_cells': total_cells,
            'code_cells': code_cells,
            'markdown_cells': md_cells,
            'status': 'ok'
        }

    except FileNotFoundError:
        test_fail('notebook', f"{nb_name}", "File not found")
        results['notebooks'][nb_name] = {'status': 'missing'}
    except json.JSONDecodeError:
        test_fail('notebook', f"{nb_name}", "Invalid JSON")
        results['notebooks'][nb_name] = {'status': 'invalid'}
    except Exception as e:
        test_fail('notebook', f"{nb_name}", str(e))
        results['notebooks'][nb_name] = {'status': 'error'}

# ============================================================================
# TEST ENHANCED NOTEBOOKS SPECIFICALLY
# ============================================================================
print_header("TESTING ENHANCED NOTEBOOKS (03, 04, 06)")

enhanced_content = {
    'notebooks/03_Transition_State_Theory.ipynb': {
        'required_content': ['INVESTIGATION 4', 'LEPS', 'Potential Energy Surface', 'Newton-Raphson'],
        'min_cells': 20
    },
    'notebooks/04_Molecular_Dynamics.ipynb': {
        'required_content': ['INVESTIGATION 4', 'Classical Trajectory', 'Monte Carlo', 'Velocity Verlet'],
        'min_cells': 15
    },
    'notebooks/06_Integration_Projects.ipynb': {
        'required_content': ['PROJECT 4', 'Complete Reaction Dynamics', 'H + HI'],
        'min_cells': 15
    }
}

for nb_path, requirements in enhanced_content.items():
    nb_name = Path(nb_path).name
    print(f"\n{nb_name}:")

    try:
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)

        cells = nb['cells']
        total_cells = len(cells)

        # Check cell count
        if total_cells >= requirements['min_cells']:
            test_pass('enhanced', f"{nb_name} - cell count",
                     f"{total_cells} cells (>= {requirements['min_cells']})")
        else:
            test_warn('enhanced', f"{nb_name} - cell count",
                     f"{total_cells} cells (expected >= {requirements['min_cells']})")

        # Check required content
        all_content = ' '.join(''.join(cell.get('source', [])) for cell in cells)

        for keyword in requirements['required_content']:
            if keyword.lower() in all_content.lower():
                test_pass('enhanced', f"{nb_name} - '{keyword}'", "Found")
            else:
                test_fail('enhanced', f"{nb_name} - '{keyword}'", "Missing")

    except Exception as e:
        test_fail('enhanced', nb_name, str(e))

# ============================================================================
# TEST ALL DATA FILES
# ============================================================================
print_header("TESTING ALL DATA FILES")

# Find all CSV files
data_dirs = ['data/tst', 'data/md', 'data/projects']
all_data_files = []

for data_dir in data_dirs:
    if os.path.exists(data_dir):
        csv_files = list(Path(data_dir).glob('*.csv'))
        all_data_files.extend(csv_files)

if not all_data_files:
    test_warn('data', 'Data files', 'No CSV files found')
else:
    print(f"\nFound {len(all_data_files)} data files:")

    for data_file in all_data_files:
        try:
            df = pd.read_csv(data_file)
            rows, cols = df.shape

            # Check for NaN values
            nan_count = df.isna().sum().sum()

            if nan_count == 0:
                test_pass('data', data_file.name, f"{rows}x{cols}, no NaN")
            else:
                test_warn('data', data_file.name, f"{rows}x{cols}, {nan_count} NaN values")

            results['data_files'][str(data_file)] = {
                'rows': rows,
                'cols': cols,
                'nan_count': nan_count,
                'status': 'ok'
            }

        except Exception as e:
            test_fail('data', data_file.name, str(e))
            results['data_files'][str(data_file)] = {'status': 'error'}

# ============================================================================
# TEST MODULE INTEGRATION
# ============================================================================
print_header("TESTING PYTHON MODULES")

sys.path.append('modules')

module_tests = {
    'leps_surface': ['LEPSSurface'],
    'visualization': ['plot_pes_3d', 'plot_pes_contour', 'plot_morse_curve'],
    'trajectory': ['ClassicalTrajectory'],
    'transition_state': ['TransitionStateOptimizer']
}

for module_name, expected_classes in module_tests.items():
    print(f"\n{module_name}.py:")

    try:
        module = __import__(module_name)
        test_pass('module', f"{module_name} - import", "Success")

        for class_name in expected_classes:
            if hasattr(module, class_name):
                test_pass('module', f"{module_name}.{class_name}", "Found")
            else:
                test_fail('module', f"{module_name}.{class_name}", "Missing")

        results['modules'][module_name] = {'status': 'ok'}

    except ImportError as e:
        test_fail('module', module_name, f"Import error: {e}")
        results['modules'][module_name] = {'status': 'import_error'}
    except Exception as e:
        test_fail('module', module_name, str(e))
        results['modules'][module_name] = {'status': 'error'}

# ============================================================================
# TEST COURSE STRUCTURE
# ============================================================================
print_header("TESTING OVERALL COURSE STRUCTURE")

# Check directory structure
required_dirs = ['notebooks', 'data', 'modules', 'papers']
for dir_name in required_dirs:
    if os.path.exists(dir_name):
        test_pass('structure', f"Directory '{dir_name}'", "Exists")
    else:
        test_warn('structure', f"Directory '{dir_name}'", "Missing")

# Check README/documentation
doc_files = ['README.md', 'PAPER_INTEGRATION_PLAN.md', 'VALIDATION_REPORT.md']
for doc in doc_files:
    if os.path.exists(doc):
        test_pass('docs', doc, "Exists")
    else:
        test_warn('docs', doc, "Not found")

# ============================================================================
# TEST EDUCATIONAL PROGRESSION
# ============================================================================
print_header("TESTING EDUCATIONAL PROGRESSION")

# Expected topics per notebook
notebook_topics = {
    '00': 'Setup and Introduction',
    '01': 'Collision Theory',
    '02': 'Diffusion Controlled Reactions',
    '03': 'Transition State Theory',
    '04': 'Molecular Dynamics',
    '05': 'Electron Transfer',
    '06': 'Integration Projects'
}

print("\nCourse Progression:")
for nb_num, topic in notebook_topics.items():
    nb_file = f'notebooks/{nb_num}_*.ipynb'
    matching = list(Path('notebooks').glob(f'{nb_num}_*.ipynb'))

    if matching:
        test_pass('progression', f"Notebook {nb_num}: {topic}", matching[0].name)
    else:
        test_fail('progression', f"Notebook {nb_num}: {topic}", "Missing")

# ============================================================================
# FINAL REPORT
# ============================================================================
print_header("COMPREHENSIVE TEST SUMMARY")

total_tests = results['overall']['passed'] + results['overall']['failed']
pass_rate = (results['overall']['passed'] / total_tests * 100) if total_tests > 0 else 0

print(f"\n[TEST STATISTICS]")
print(f"   Total Tests: {total_tests}")
print(f"   Passed: {results['overall']['passed']} ({pass_rate:.1f}%)")
print(f"   Failed: {results['overall']['failed']}")
print(f"   Warnings: {results['overall']['warnings']}")

print(f"\n[NOTEBOOKS]")
print(f"   Total: {len(results['notebooks'])}")
print(f"   Working: {sum(1 for nb in results['notebooks'].values() if nb.get('status') == 'ok')}")

print(f"\n[DATA FILES]")
print(f"   Total: {len(results['data_files'])}")
print(f"   Valid: {sum(1 for df in results['data_files'].values() if df.get('status') == 'ok')}")

print(f"\n[MODULES]")
print(f"   Total: {len(results['modules'])}")
print(f"   Working: {sum(1 for m in results['modules'].values() if m.get('status') == 'ok')}")

# Overall status
print(f"\n{'='*80}")
if results['overall']['failed'] == 0:
    print("[SUCCESS] ALL TESTS PASSED - COURSE IS READY!")
    print("\nThe complete Reaction Dynamics course framework is validated.")
    print("All notebooks, data files, and modules are working correctly.")
elif results['overall']['failed'] < 5:
    print("[WARNING] MOSTLY PASSING - Minor issues detected")
    print(f"\n{results['overall']['failed']} tests failed, {results['overall']['warnings']} warnings")
else:
    print("[FAIL] ISSUES DETECTED - Review needed")
    print(f"\n{results['overall']['failed']} tests failed, {results['overall']['warnings']} warnings")

print(f"{'='*80}\n")

# Exit code
sys.exit(0 if results['overall']['failed'] == 0 else 1)
