# Google Colab Setup Guide

This document explains how the notebooks are configured for Google Colab integration.

## Colab Setup Cell

Each notebook should have a setup cell at the beginning (after the title/introduction) that detects the Colab environment and clones the repository to access images.

### Setup Cell Code

Add this as the **first code cell** in each notebook:

```python
# ============================================================
# GOOGLE COLAB SETUP
# ============================================================
import sys
import os

# Check if running in Google Colab
IN_COLAB = 'google.colab' in sys.modules

if IN_COLAB:
    print("=" * 60)
    print("RUNNING IN GOOGLE COLAB")
    print("=" * 60)

    # Clone repository to access images
    repo_url = "https://github.com/mcbadlon31/Reaction-Dynamics-Physical-Chemistry.git"

    print(f"\nCloning repository: {repo_url}")
    print("This may take a minute...")

    !git clone {repo_url} --depth 1 --quiet

    # Change to repository directory
    os.chdir('Reaction-Dynamics-Physical-Chemistry')

    # Install additional packages if needed
    print("\nInstalling additional packages...")
    !pip install -q seaborn plotly ipywidgets

    print("\n" + "=" * 60)
    print("[SUCCESS] Colab setup complete!")
    print("=" * 60)
    print(f"Current directory: {os.getcwd()}")
    print("\nYou can now run all cells normally.")
    print("Images will load from the cloned repository.")

else:
    print("=" * 60)
    print("RUNNING IN LOCAL JUPYTER ENVIRONMENT")
    print("=" * 60)
    print("\nNo setup needed - using local files")
```

## Image Path Handling

After adding the setup cell, image paths in notebooks should work correctly:

**Current format (already correct):**
```python
![Maxwell-Boltzmann](images/collision_theory/maxwell_boltzmann_speeds.png)
```

**Or in code:**
```python
from IPython.display import Image
Image('images/collision_theory/maxwell_boltzmann_speeds.png')
```

The Colab setup cell ensures that when running in Colab:
1. The repository is cloned to `/content/Reaction-Dynamics-Physical-Chemistry/`
2. Working directory changes to the repository root
3. Relative paths like `images/...` work correctly

## Adding Setup Cell to Existing Notebooks

To add the setup cell to an existing notebook:

### Option 1: Manual (via Jupyter Lab)
1. Open notebook in Jupyter Lab
2. Insert new code cell at the top (after intro/title)
3. Copy the setup cell code above
4. Test locally (should print "RUNNING IN LOCAL JUPYTER ENVIRONMENT")
5. Save notebook

### Option 2: Programmatic (Python script)

```python
import json
from pathlib import Path

notebook_dir = Path("notebooks")

setup_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# COLAB SETUP CODE HERE\n",
        # ... (full setup code as string list)
    ]
}

for nb_file in notebook_dir.glob("*.ipynb"):
    with open(nb_file, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Insert after first cell (title/intro)
    nb['cells'].insert(1, setup_cell)

    with open(nb_file, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
```

## Testing in Colab

After pushing to GitHub, test each notebook:

1. Open Colab link: `https://colab.research.google.com/github/mcbadlon31/Reaction-Dynamics-Physical-Chemistry/blob/main/notebooks/01_Collision_Theory.ipynb`
2. Run the setup cell
3. Check output:
   - Should clone repository
   - Should install packages
   - Should change directory
4. Run subsequent cells
5. Verify images load correctly
6. Test interactive widgets

## Troubleshooting

**Images not loading:**
- Check setup cell ran successfully
- Verify current directory: `!pwd` should show `/content/Reaction-Dynamics-Physical-Chemistry`
- Check image path is relative: `images/topic/filename.png`

**Widgets not displaying:**
- Colab should auto-enable ipywidgets
- If not, manually enable: `from google.colab import widgets`

**Repository not cloning:**
- Check GitHub repository is public
- Verify URL is correct
- Try manual clone: `!git clone https://github.com/mcbadlon31/Reaction-Dynamics-Physical-Chemistry.git`

## Current Status

**Notebooks with setup cell:**
- [ ] 00_Setup_and_Introduction.ipynb
- [ ] 01_Collision_Theory.ipynb
- [ ] 02_Diffusion_Controlled.ipynb
- [ ] 03_Transition_State_Theory.ipynb
- [ ] 04_Molecular_Dynamics.ipynb
- [ ] 05_Electron_Transfer.ipynb
- [ ] 06_Integration_Projects.ipynb

## Next Steps

1. Add setup cell to all notebooks (Option 2 script recommended)
2. Test locally to ensure no breakage
3. Commit and push to GitHub
4. Test each notebook in Colab
5. Update QR codes (already done with `generate_colab_qr_codes.py`)
6. Recompile presentation
7. Test QR code scanning
