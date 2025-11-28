#!/usr/bin/env python3
"""Add Google Colab setup cells to all notebooks"""

import json
from pathlib import Path

# GitHub configuration
GITHUB_USER = "mcbadlon31"
REPO_NAME = "Reaction-Dynamics-Physical-Chemistry"

# Get directories
script_dir = Path(__file__).parent
project_root = script_dir.parent
notebooks_dir = project_root / "notebooks"

# Colab setup cell content
SETUP_CELL = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# ============================================================\n",
        "# GOOGLE COLAB SETUP\n",
        "# ============================================================\n",
        "import sys\n",
        "import os\n",
        "\n",
        "# Check if running in Google Colab\n",
        "IN_COLAB = 'google.colab' in sys.modules\n",
        "\n",
        "if IN_COLAB:\n",
        "    print(\"=\" * 60)\n",
        "    print(\"RUNNING IN GOOGLE COLAB\")\n",
        "    print(\"=\" * 60)\n",
        "\n",
        f"    # Clone repository to access images\n",
        f"    repo_url = \"https://github.com/{GITHUB_USER}/{REPO_NAME}.git\"\n",
        "\n",
        "    print(f\"\\nCloning repository: {repo_url}\")\n",
        "    print(\"This may take a minute...\")\n",
        "\n",
        "    !git clone {repo_url} --depth 1 --quiet\n",
        "\n",
        f"    # Change to repository directory\n",
        f"    os.chdir('{REPO_NAME}')\n",
        "\n",
        "    # Install additional packages if needed\n",
        "    print(\"\\nInstalling additional packages...\")\n",
        "    !pip install -q seaborn plotly ipywidgets\n",
        "\n",
        "    print(\"\\n\" + \"=\" * 60)\n",
        "    print(\"[SUCCESS] Colab setup complete!\")\n",
        "    print(\"=\" * 60)\n",
        "    print(f\"Current directory: {os.getcwd()}\")\n",
        "    print(\"\\nYou can now run all cells normally.\")\n",
        "    print(\"Images will load from the cloned repository.\")\n",
        "\n",
        "else:\n",
        "    print(\"=\" * 60)\n",
        "    print(\"RUNNING IN LOCAL JUPYTER ENVIRONMENT\")\n",
        "    print(\"=\" * 60)\n",
        "    print(\"\\nNo setup needed - using local files\")"
    ]
}

def add_setup_cell_to_notebook(notebook_path):
    """Add Colab setup cell to a notebook if not already present"""

    print(f"\nProcessing: {notebook_path.name}")

    # Read notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    # Check if setup cell already exists
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code' and any('GOOGLE COLAB SETUP' in line for line in cell.get('source', [])):
            print(f"  [SKIP] Setup cell already exists")
            return False

    # Find insertion point (after first markdown cell, usually title)
    insert_index = 1
    if len(notebook['cells']) > 0 and notebook['cells'][0]['cell_type'] == 'markdown':
        insert_index = 1

    # Insert setup cell
    notebook['cells'].insert(insert_index, SETUP_CELL)

    # Write back notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)

    print(f"  [OK] Setup cell added at position {insert_index}")
    return True

def main():
    """Process all notebooks"""

    print("=" * 60)
    print("ADDING COLAB SETUP CELLS TO NOTEBOOKS")
    print("=" * 60)
    print(f"GitHub: {GITHUB_USER}/{REPO_NAME}")
    print(f"Notebooks directory: {notebooks_dir}")
    print("=" * 60)

    # Find all notebooks
    notebooks = sorted(notebooks_dir.glob("*.ipynb"))

    if not notebooks:
        print("\n[ERROR] No notebooks found!")
        return

    print(f"\nFound {len(notebooks)} notebooks:")
    for nb in notebooks:
        print(f"  - {nb.name}")

    # Process each notebook
    print("\n" + "=" * 60)
    print("PROCESSING NOTEBOOKS")
    print("=" * 60)

    modified_count = 0
    for notebook_path in notebooks:
        if add_setup_cell_to_notebook(notebook_path):
            modified_count += 1

    # Summary
    print("\n" + "=" * 60)
    print("[SUCCESS] PROCESSING COMPLETE")
    print("=" * 60)
    print(f"Total notebooks: {len(notebooks)}")
    print(f"Modified: {modified_count}")
    print(f"Skipped: {len(notebooks) - modified_count}")

    if modified_count > 0:
        print("\n" + "=" * 60)
        print("NEXT STEPS")
        print("=" * 60)
        print("1. Test notebooks locally:")
        print("   jupyter lab")
        print("   Run setup cell - should print 'LOCAL JUPYTER ENVIRONMENT'")
        print("\n2. Commit changes:")
        print("   git add notebooks/")
        print(f"   git commit -m 'Add Colab setup cells to notebooks'")
        print("\n3. Push to GitHub:")
        print("   git push origin main")
        print("\n4. Test in Colab:")
        print(f"   https://colab.research.google.com/github/{GITHUB_USER}/{REPO_NAME}/blob/main/notebooks/01_Collision_Theory.ipynb")

if __name__ == "__main__":
    main()
