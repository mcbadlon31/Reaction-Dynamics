# Beamer Presentation

## Compiling the Presentation

### Requirements
- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- Packages: beamer, tikz, pgfplots, xcolor, graphicx

### Compilation
```bash
pdflatex reaction_dynamics_main.tex
pdflatex reaction_dynamics_main.tex  # Run twice for references
```

### Structure
- `reaction_dynamics_main.tex` - Main file (includes all topics)
- `topics/` - Individual topic files (18A through 18E)
- `qr_codes/` - QR codes linking to Google Colab notebooks
- `../images/` - High-quality figures (referenced via relative paths)

### Customization
To update QR codes with your GitHub repository:
1. Edit `../scripts/generate_qr_codes.py`
2. Update repository URL
3. Run: `python ../scripts/generate_qr_codes.py`
4. Recompile presentation

### Notes
- Images are now loaded from `../images/` (organized by topic)
- QR codes point to Google Colab URLs (update after GitHub push)
- Presentation is 178 pages, 2.5 MB
