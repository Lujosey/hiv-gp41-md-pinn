import MDAnalysis as mda
import numpy as np
import pandas as pd

# 1. Load the "Digital Twin" Universe
u = mda.Universe("step7_production.tpr", "step7_production.xtc")
harpoon = u.select_atoms("resnum 1 to 22") # Your AVGIG... sequence
membrane = u.select_atoms("resname POPC")

data_log = []

print(f"Starting Data Extraction for {len(u.trajectory)} frames...")

# 2. Extract Features for the PINN
for ts in u.trajectory:
    # Feature A: Time in picoseconds
    time = u.trajectory.time
    
    # Feature B: Relative Z-position (Distance from membrane center)
    z_pos = harpoon.center_of_mass()[2] - membrane.center_of_mass()[2]
    
    # Feature C: Radius of Gyration (How 'bunched up' the harpoon is)
    rg = harpoon.radius_of_gyration()
    
    data_log.append([time, z_pos, rg])

# 3. Save to a clean CSV for Azure/DeepXDE
df = pd.DataFrame(data_log, columns=['time_ps', 'z_dist_angstrom', 'rad_gyration'])
df.to_csv('pinn_training_data.csv', index=False)

print("Success! 'pinn_training_data.csv' is ready for the Digital Twin.")
