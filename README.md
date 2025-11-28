# Reaction Dynamics - Physical Chemistry Interactive Course

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue.svg)](https://github.com/mcbadlon31/Reaction-Dynamics-Physical-Chemistry)

## 📚 Overview

Complete interactive course materials for **Focus 18: Reaction Dynamics** from Atkins' Physical Chemistry. This repository contains:

- **Professional Beamer Presentation** (178 pages) with embedded QR codes
- **6 Interactive Jupyter Notebooks** with animations, calculators, and exercises
- **36 High-Quality Scientific Figures** (publication-ready)
- **Seamless Google Colab Integration** for instant access

## 🎯 Topics Covered

| Topic | Title | Notebook | Colab Link |
|-------|-------|----------|------------|
| **18A** | Collision Theory | `01_Collision_Theory.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mcbadlon31/Reaction-Dynamics-Physical-Chemistry/blob/main/notebooks/01_Collision_Theory.ipynb) |
| **18B** | Diffusion-Controlled Reactions | `02_Diffusion_Controlled.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mcbadlon31/Reaction-Dynamics-Physical-Chemistry/blob/main/notebooks/02_Diffusion_Controlled.ipynb) |
| **18C** | Transition-State Theory | `03_Transition_State_Theory.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mcbadlon31/Reaction-Dynamics-Physical-Chemistry/blob/main/notebooks/03_Transition_State_Theory.ipynb) |
| **18D** | Molecular Collision Dynamics | `04_Molecular_Dynamics.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mcbadlon31/Reaction-Dynamics-Physical-Chemistry/blob/main/notebooks/04_Molecular_Dynamics.ipynb) |
| **18E** | Electron Transfer | `05_Electron_Transfer.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mcbadlon31/Reaction-Dynamics-Physical-Chemistry/blob/main/notebooks/05_Electron_Transfer.ipynb) |

## Quick Start

### Option 1: Google Colab (Recommended - No Installation)

1. Click any "Open in Colab" badge above
2. Click "Copy to Drive" to save your own copy
3. Run cells and interact with widgets
4. All notebooks are pre-configured for Colab

### Option 2: Local Installation

```bash
# Clone repository
git clone https://github.com/mcbadlon31/Reaction-Dynamics-Physical-Chemistry.git
cd Reaction-Dynamics-Physical-Chemistry

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter Lab
jupyter lab
```

## Repository Structure

```
Reaction-Dynamics-Physical-Chemistry/
├── presentation/           # LaTeX Beamer slides + PDF
│   ├── topics/            # Individual topic files
│   └── qr_codes/          # QR codes linking to Colab
├── notebooks/             # Interactive Jupyter notebooks
├── images/                # High-quality figures (organized by topic)
├── scripts/               # Utility scripts (QR generation, etc.)
└── docs/                  # Additional documentation
```

## For Students

**During Lecture:**
- Scan QR codes on slides with your phone
- Opens notebook directly in Google Colab
- Follow along with interactive examples

**After Class:**
- Use Colab links to review and practice
- Modify code and explore parameters
- Complete interactive exercises

**No Installation Required!** Everything runs in your browser via Google Colab.

## For Instructors

**Using the Presentation:**
- Compile: `pdflatex reaction_dynamics_main.tex` (in `presentation/`)
- QR codes embedded at end of each topic
- High-quality figures replace TikZ diagrams

**Customizing Notebooks:**
- Edit notebooks in `notebooks/`
- Push changes to GitHub → Students get updates
- Fork repository to make your own version

**Updating QR Codes:**
- Run `scripts/generate_qr_codes.py` with your GitHub URL
- Recompile LaTeX presentation

## Interactive Features

- **Real-Time Calculators**: Adjust parameters with sliders
- **Animated Simulations**: Watch molecules collide and react
- **3D Visualizations**: Rotate potential energy surfaces
- **Practice Problems**: Code-based exercises with solutions
- **Parameter Exploration**: See how changing T, P, σ affects rates

## Example Notebooks

**01_Collision_Theory.ipynb:**
- Interactive collision frequency calculator
- Animated molecular collisions
- Harpoon mechanism explorer
- RRK model for unimolecular decay

**03_Transition_State_Theory.ipynb:**
- Eyring plot generator
- Kinetic isotope effect calculator
- Tunneling correction visualizer
- Salt effect ionic strength explorer

**05_Electron_Transfer.ipynb:**
- Marcus parabola interactive plotter
- Normal/inverted region explorer
- Distance decay tunneling simulator

## 📄 License

This work is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

**You are free to:**
- Share and adapt the material for educational purposes
- Must give appropriate credit
- Non-commercial use only
- Share adaptations under same license

## 🙏 Acknowledgments

Based on **Atkins' Physical Chemistry** (12th Edition), Focus 18: Reaction Dynamics.

Interactive notebooks developed with:
- Python scientific stack (NumPy, Matplotlib, SciPy)
- Plotly for 3D visualizations
- IPyWidgets for interactivity
- Google Colab for cloud hosting

## 📧 Contact

For questions, suggestions, or issues:
- Open an issue on GitHub
- Email: [your-email@university.edu]

## 🔄 Version History

- **v1.0** (2024-11-25): Initial release
  - 178-page presentation
  - 6 interactive notebooks
  - Google Colab integration
  - QR code embedding

---

**⭐ If you find this useful, please star the repository!**
