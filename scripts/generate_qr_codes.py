#!/usr/bin/env python3
"""Generate QR codes for interactive notebooks"""

import qrcode
import os

# Create QR_codes directory
os.makedirs("QR_codes", exist_ok=True)

# Notebook information
notebooks = {
    "01_Collision_Theory": {
        "file": "Reaction_Dynamics_Interactive/01_Collision_Theory.ipynb",
        "title": "Topic 18A: Collision Theory Interactive"
    },
    "02_Diffusion_Controlled": {
        "file": "Reaction_Dynamics_Interactive/02_Diffusion_Controlled.ipynb",
        "title": "Topic 18B: Diffusion-Controlled Interactive"
    },
    "03_Transition_State_Theory": {
        "file": "Reaction_Dynamics_Interactive/03_Transition_State_Theory.ipynb",
        "title": "Topic 18C: Transition-State Theory Interactive"
    },
    "04_Molecular_Dynamics": {
        "file": "Reaction_Dynamics_Interactive/04_Molecular_Dynamics.ipynb",
        "title": "Topic 18D: Molecular Dynamics Interactive"
    },
    "05_Electron_Transfer": {
        "file": "Reaction_Dynamics_Interactive/05_Electron_Transfer.ipynb",
        "title": "Topic 18E: Electron Transfer Interactive"
    },
    "00_Setup": {
        "file": "Reaction_Dynamics_Interactive/00_Setup_and_Introduction.ipynb",
        "title": "Setup and Python Introduction"
    }
}

# Generate QR codes
for name, info in notebooks.items():
    # Create QR code with file path
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )

    # Add the relative file path
    qr.add_data(info["file"])
    qr.make(fit=True)

    # Create image
    img = qr.make_image(fill_color="black", back_color="white")

    # Save
    output_path = f"QR_codes/{name}.png"
    img.save(output_path)
    print(f"[OK] Generated: {output_path}")
    print(f"  Links to: {info['file']}")
    print(f"  Title: {info['title']}\n")

print(f"\nAll QR codes generated successfully in QR_codes/ directory!")
