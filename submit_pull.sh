#!/bin/bash
#SBATCH --job-name=gp41_pull      # Job name
#SBATCH --nodes=1                 # Run on a single node
#SBATCH --ntasks-per-node=32      # Use 32 CPU cores
#SBATCH --time=24:00:00           # 24-hour walltime limit
#SBATCH --partition=batch         # Standard UL/Bernal partition

# Load GROMACS (the exact command depends on the UL cluster setup)
module load gromacs/2023.3

# Step 1: Pre-process the pulling simulation
# We use the index file you just made (-n index.ndx)
gmx grompp -f pull.mdp -c step7_production.gro -p topol.top -n index.ndx -o pull.tpr

# Step 2: Run the Steered MD (The 100 pN Force Test)
# -px saves the position, -pf saves the force data for your Digital Twin
gmx mdrun -v -deffnm pull -s pull.tpr -px pullx.xvg -pf pullf.xvg
