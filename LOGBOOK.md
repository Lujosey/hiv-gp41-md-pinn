markdown# Technical Log-Book: GROMACS Deployment, Baseline Verification, and HIV-1 gp41 Fusion Peptide System Specification

**Date:** September 8, 2026  
**Author:** E. Matare  
**Category:** Molecular Dynamics Workflow / Environment Setup  
**Tags:** WSL, Ubuntu, GROMACS-2023, HEWL, HIV-1 gp41, Fusion Peptide, CHARMM36n, POPC  

---

## 1. Environment Build & Core Engine Configuration
To establish a stable high-performance computing baseline on Windows 11 without native compilation conflicts, a sandboxed Linux subsystem environment was deployed.

### Environment Specification
*   **Subsystem Layer:** Windows Subsystem for Linux (WSL2)
*   **Linux Distribution:** Ubuntu Linux via Windows Terminal (`Admin` elevation)
*   **MD Engine Package:** GROMACS Version `2023.3-Ubuntu_2023.3_1ubuntu3`

### Exact Deployment Command History
```powershell
# Step 1: Open Windows Terminal (Admin) and initialize the Linux Subsystem
wsl --install -d Ubuntu

# [System Reboot Executed Here to Initialize WSL Kernel Hooks]
```
```bash
# Step 2: Open the Ubuntu Terminal App and configure the UNIX local account
# Account Created: Username = ematare

# Step 3: Refresh local mirrors and install pre-built GROMACS binary package
sudo apt update
sudo apt install gromacs

# Step 4: Verify absolute path and functional binary engine path hooks
gmx
```
*   **Result:** GROMACS environment confirmed active. The system successfully returned the operational syntax manual and the Rosalind Franklin quote block, verifying package integrity.

---

## 2. Sandbox Verification Run: HEWL Processing & Path Troubleshooting
Before deploying the primary gp41 membrane workspace, a validation study was executed using Hen Egg-White Lysozyme (**PDB ID: 1AKI**) to verify file handling, cleaning scripts, and the `pdb2gmx` topology parser.

### Technical Hurdles & Directory Fixes
1.  **Automated Download Failure:** Standard terminal fetching commands (`wget`) pulled the web interface wrapper (HTML) rather than the raw structural text stream. This caused a fatal error downstream: `Fatal error: An input file contains a line longer than 4096 characters... in fgets2`.
2.  **Resolution Protocol:** The file was manually downloaded via the Windows browser engine from the RCSB repository in pure PDB text format and mapped directly from the Windows directory path into the Linux directory layer.

### Commands & Processing Pipeline
```bash
# Initialize clean sandbox folder layout
mkdir lysozyme_tutorial && cd lysozyme_tutorial

# Map and copy the verified raw file from the host download partition
cp /mnt/c/Users/ematare.AIRCON/Downloads/1AKI.pdb .

# Clean structural space by filtering crystal water coordinate lines (HOH)
grep -v HOH 1AKI.pdb > 1AKI_clean.pdb

# Run coordinate conversion, hydrogen addition, and topology layout generation
gmx pdb2gmx -f 1AKI_clean.pdb -o 1AKI_processed.gro -water tip3p
```
*   **Parameter Parameters Selection:** Configured utilizing **Option 15 (OPLS-AA/L all-atom force field)**. The run completed without warnings, yielding the structural coordinate files (`.gro`) and the core system master blueprint file (`topol.top`).

---

## 3. Targeted Production Framework: HIV-1 gp41 Fusion Peptide System Architecture
With the engine verified, the workspace has been migrated to configure the **HIV-1 gp41 Fusion Peptide (FP)** structural framework. 

### Molecular Architecture Parameters
*   **Construct Target:** HIV-1 gp41 Fusion Peptide (Highly hydrophobic N-terminal anchor sequence).
*   **Oligomeric State:** Monomer (Exploratory baseline stability test frame).
*   **Force Field Selection:** **CHARMM36n** (Port optimized explicitly for complex interfacial structural behaviors at the lipid-peptide boundary layer).
*   **Membrane Environment Matrix:** POPC (1-palmitoyl-2-oleoyl-glycero-3-phosphocholine) bilayer matrix.
*   **Solvation Parameters:** CHARMM-modified TIP3P water model with a background ionic strength of **0.15 M NaCl** to ensure physiological neutrality.

### Mandatory `.mdp` Configuration Parameters for CHARMM36n Bilayers
To prevent artificial membrane distortion or structural artifacts, the non-bonded force-switching parameters in GROMACS must strictly replicate native CHARMM formatting. The following parameter blocks are established for the minimization and equilibration runs:

```ini
; Required parameter blocks for CHARMM36n membrane stability
cutoff-scheme    = Verlet      ; Pair list generation scheme
vdwtype          = Cut-off     ; Treat Van der Waals via cutoff
vdw-modifier     = Force-switch; Smoothly switch forces over a set window
rlist            = 1.2         ; Neighbor list cutoff distance (nm)
rvdw             = 1.2         ; Van der Waals cutoff distance (nm)
rvdw-switch      = 1.0         ; Distance where force switching begins (nm)
coulombtype      = PME         ; Particle Mesh Ewald for long-range electrostatics
DispCorr         = no          ; Long-range dispersion corrections must be off for lipid bilayers
```

### Planned Simulation Protocol Breakdown
System Preparation] ──> [Minimization] ──> [NVT Equilibration] ──> [NPT Equilibration] ──> [10 ns Stability Run]
1.  **Energy Minimization:** Steepest descent algorithm configured to run until maximum force ($F_{max}$) is under $1000\text{ kJ/mol/nm}$ to resolve structural lipid-protein clashes.
2.  **NVT Heating:** Thermal ramp targeting **310 K** using a V-rescale thermostat. Position restraints are heavily mapped onto the peptide backbone to protect the initial configuration coordinates.
3.  **NPT Thermal Balancing:** Pressure stabilization at **1.0 bar** utilizing a semi-isotropic Parrinello-Rahman barostat. The $x/y$ plane (membrane surface area) and $z$ plane (membrane thickness) are coupled independently to ensure optimal lipid freedom.
4.  **10 ns Production Phase:** Initial unconstrained execution designed to capture structural behavior. Data outputs will be logged via `gmx energy` to track system variables (Potential Energy, Temperature, Pressure, Density) and structural trajectories (RMSD in nm, peptide center-of-mass depth).

---

## 4. Machine Learning Framework: PINN Baseline Frame
An exploratory baseline for a Physics-Informed Neural Network (PINN) structure was evaluated utilizing a `DeepXDE` and `PyTorch` wrapper script.
*   **Data Boundaries:** The current operational script processes time ($t$) as the spatial feature input data and the absolute trans-membrane axis coordinate ($z$) as the training target output.
*   **Loss Equation Physics Constraint:** The optimization loop forces a stationary-state derivative approximation ($dz/dt \approx 0$).
*   **Current Scientific Interpretation:** This script functions strictly as an **initial trajectory-smoothing tool** and stationary baseline verification test. It does *not* model or claim to resolve a full mechanobiological digital twin, free-energy barrier landscape, or active force field projection until extended steered molecular data trajectories are generated.