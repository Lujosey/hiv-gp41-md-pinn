import MDAnalysis as mda
import numpy as np

# Load your 10ns data
u = mda.Universe("step7_production.tpr", "step7_production.xtc")

# Select your sequence: AVGIGALFLGFGAAGSTMGARS (usually the first ~22 residues)
# Adjust 'resnum 1:22' if your PDB numbering is different
harpoon_tip = u.select_atoms("resnum 1 to 22 and name CA")
membrane_surface = u.select_atoms("resname POPC and name P")

print("Tracking the Harpoon (AVGIGALFLGFGAAGSTMGARS)...")

# Get average positions over the last 1ns (frames 90 to 100)
tip_z = []
mem_z = []

for ts in u.trajectory[90:]:
    tip_z.append(harpoon_tip.center_of_mass()[2])
    mem_z.append(membrane_surface.center_of_mass()[2])

avg_dist = np.mean(tip_z) - np.mean(mem_z)
print(f"\n--- HARPOON ANALYSIS ---")
print(f"Average Tip Z-Height: {np.mean(tip_z):.2f} Angstroms")
print(f"Distance from Membrane Center: {avg_dist:.2f} Angstroms")
print(f"------------------------")

