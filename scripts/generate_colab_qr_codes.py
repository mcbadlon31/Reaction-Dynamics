#!/usr/bin/env python3
"""Generate QR codes for Google Colab links"""

import qrcode
import os
from pathlib import Path

# GitHub username and repository
GITHUB_USER = "mcbadlon31"
REPO_NAME = "Reaction-Dynamics-Physical-Chemistry"

# Base Colab URL
COLAB_BASE = f"https://colab.research.google.com/github/{GITHUB_USER}/{REPO_NAME}/blob/main/notebooks"

# Get the script directory and project root
script_dir = Path(__file__).parent
project_root = script_dir.parent
qr_output_dir = project_root / "presentation" / "qr_codes"

# Create QR codes directory if it doesn't exist
qr_output_dir.mkdir(parents=True, exist_ok=True)

# Notebook information with Colab URLs
notebooks = {
    "00_Setup": {
        "url": f"{COLAB_BASE}/00_Setup_and_Introduction.ipynb",
        "title": "Setup and Python Introduction"
    },
    "01_Collision_Theory": {
        "url": f"{COLAB_BASE}/01_Collision_Theory.ipynb",
        "title": "Topic 18A: Collision Theory Interactive"
    },
    "02_Diffusion_Controlled": {
        "url": f"{COLAB_BASE}/02_Diffusion_Controlled.ipynb",
        "title": "Topic 18B: Diffusion-Controlled Interactive"
    },
    "03_Transition_State_Theory": {
        "url": f"{COLAB_BASE}/03_Transition_State_Theory.ipynb",
        "title": "Topic 18C: Transition-State Theory Interactive"
    },
    "04_Molecular_Dynamics": {
        "url": f"{COLAB_BASE}/04_Molecular_Dynamics.ipynb",
        "title": "Topic 18D: Molecular Dynamics Interactive"
    },
    "05_Electron_Transfer": {
        "url": f"{COLAB_BASE}/05_Electron_Transfer.ipynb",
        "title": "Topic 18E: Electron Transfer Interactive"
    }
}

print("=" * 60)
print("GENERATING GOOGLE COLAB QR CODES")
print("=" * 60)
print(f"GitHub: {GITHUB_USER}/{REPO_NAME}")
print(f"Output: {qr_output_dir}")
print("=" * 60)

# Generate QR codes
for name, info in notebooks.items():
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )

    # Add the Colab URL
    qr.add_data(info["url"])
    qr.make(fit=True)

    # Create image
    img = qr.make_image(fill_color="black", back_color="white")

    # Save
    output_path = qr_output_dir / f"{name}.png"
    img.save(output_path)
    print(f"[OK] Generated: {output_path.name}")
    print(f"  URL: {info['url']}")
    print(f"  Title: {info['title']}\n")

print("=" * 60)
print("[SUCCESS] All QR codes generated successfully!")
print("=" * 60)
print("\nNext steps:")
print("1. QR codes are in: presentation/qr_codes/")
print("2. LaTeX slides already reference these QR code files")
print("3. Recompile presentation: pdflatex reaction_dynamics_main.tex")
print("4. Test QR codes by scanning with your phone")
