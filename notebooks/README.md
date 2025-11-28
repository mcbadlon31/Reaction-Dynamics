# Interactive Jupyter Notebooks

## Overview
6 interactive notebooks covering all aspects of reaction dynamics with:
- Live calculators and sliders
- Animated simulations
- Practice problems with solutions
- 3D visualizations

## Using with Google Colab
Click the "Open in Colab" badges in the main README, or:
1. Visit: `https://colab.research.google.com/github/[USER]/Reaction-Dynamics-Physical-Chemistry/blob/main/notebooks/01_Collision_Theory.ipynb`
2. Click "Copy to Drive" to save your own editable copy
3. Run all cells to load interactive widgets

## Local Installation
```bash
pip install -r ../requirements.txt
jupyter lab
```

## Notebook Descriptions

**00_Setup_and_Introduction.ipynb**
- Python basics for chemists
- NumPy, Matplotlib, SciPy intro
- Interactive widget examples

**01_Collision_Theory.ipynb**
- Collision frequency calculator
- Maxwell-Boltzmann distributions
- Harpoon mechanism
- RRK unimolecular decay

**02_Diffusion_Controlled.ipynb**
- Cage effect visualizer
- Smoluchowski equation
- Viscosity effects
- Encounter pair dynamics

**03_Transition_State_Theory.ipynb**
- Eyring equation calculator
- Kinetic isotope effects
- Tunneling corrections
- Salt effects

**04_Molecular_Dynamics.ipynb**
- 3D potential energy surfaces
- Trajectory simulations
- Differential cross-sections
- Newton diagrams

**05_Electron_Transfer.ipynb**
- Marcus theory explorer
- Normal/inverted regions
- Reorganization energy
- Distance decay

**06_Integration_Projects.ipynb**
- Capstone projects
- Combined concepts
- Real research examples

## Troubleshooting

**Widgets not displaying:**
```python
!pip install ipywidgets
```

**Images not loading in Colab:**
- Notebooks auto-clone repository on first run
- Check first cell executed successfully

**3D plots not rendering:**
- Try different browser (Chrome recommended)
- Check Plotly installed: `!pip install plotly`
