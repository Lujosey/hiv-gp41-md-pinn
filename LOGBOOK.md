markdown# Technical Log-Book: GROMACS Deployment, Baseline Verification, and HIV-1 gp41 Fusion Peptide System Specification

**Date:** September 8, 2026  
**Author:** E. Matare  
**Category:** Molecular Dynamics Workflow / Environment Setup  
**Tags:** WSL, Ubuntu, GROMACS-2023, HEWL, HIV-1 gp41, Fusion Peptide, CHARMM36m, POPC  

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
gmx pdb2gmx -f 1AKI_clean.pdb -o 1AKI_processed.gro -water spce -ff oplsaa
```
*   **Parameter Selection:** Configured utilizing **Option 15 (OPLS-AA/L all-atom force field)** paired with the **SPC/E water model**. The run completed without warnings, yielding the structural coordinate files (`.gro`) and the core system master blueprint file (`topol.top`). Following system solvation and neutralization via 8 Chloride (Cl⁻) ions using `gmx genion`, a 1-nanosecond unconstrained Production MD phase was executed under NPT conditions at 300 K (Average: 300.011 K, RMSD: 1.76 K) clocking a sustained performance benchmarking speed of ~28 ns/day.

---

## 3. Targeted Production Framework: HIV-1 gp41 Fusion Peptide System Architecture
With the engine verified, the workspace has been migrated to configure the **HIV-1 gp41 Fusion Peptide (FP)** structural framework. 

### Molecular Architecture Parameters
*   **Construct Target:** HIV-1 gp41 Fusion Peptide (Solution NMR structure, **PDB ID: 2PJV** bound to DPC micelles).
*   **Oligomeric State:** Monomer (Exploratory baseline stability test frame).
*   **Force Field Selection:** **CHARMM36m** (Port optimized explicitly for complex interfacial structural behaviors at the lipid-peptide boundary layer, generated via CHARMM-GUI Bilayer Builder).
*   **Membrane Environment Matrix:** POPC (1-palmitoyl-2-oleoyl-glycero-3-phosphocholine) bilayer matrix containing exactly **128 lipids** (64 in the upper leaflet, 64 in the lower leaflet).
*   **Solvation Parameters:** CHARMM-modified TIP3P water model (**8,135 water molecules**) with a background ionic strength of **0.15 M NaCl** to ensure physiological neutrality, yielding a total system size of **41,893 atoms**.

### Mandatory `.mdp` Configuration Parameters for CHARMM36m Bilayers
To prevent artificial membrane distortion or structural artifacts, the non-bonded force-switching parameters in GROMACS must strictly replicate native CHARMM formatting. The following parameter blocks are established for the minimization and equilibration runs:

```ini
; Required parameter blocks for CHARMM36m membrane stability
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
System Preparation] ──> [Minimization] ──> [6-Step Equilibration] ──> [Production MD]
1.  **Energy Minimization:** Steepest descent algorithm configured to run until maximum force ($F_{max}$) is under 1000 kJ/mol/nm to resolve structural lipid-protein clashes.
2.  **Multistage Stepwise Equilibration (Steps 6.1–6.6):** Thermal ramp targeting **303.15 K** using split temperature coupling groups (**SOLU** for peptide, **MEMB** for lipids, **SOLV** for water/ions) to enforce uniform kinetic energy dissemination. Position restraints are mapped via a decreasing force constant staircase (10.0 down to 0.1) across the cycles to systematically unpack lipid tails around the primary helical domain.

---

## 4. Chronological Execution Logs & Stepwise Equilibration Phase Tracking

### Step 6.0: Energy Minimization (Steepest Descents)
*   **Execution Date:** September 8, 2026
*   **Input Coordinates:** `step5_input.gro` (Assembled via CHARMM-GUI, aligned along the principal Z-axis)
*   **Target Criterion:** $F_{max} < 1000 \text{ kJ/mol/nm}$
*   **Result Metrics:** Converged cleanly in **1,075 steps**.
    *   $\text{Potential Energy } (E_{pot}) = -4.0926075 \times 10^5 \text{ kJ/mol}$
    *   $\text{Maximum Force } (F_{max}) = 9.0395886 \times 10^2 \text{ kJ/mol/nm}$ on atom 10543.
    *   $\text{Norm of Force} = 2.0121827 \times 10^1 \text{ kJ/mol/nm}$.

### Step 6.1: NVT Equilibration & Thermal Initialization
*   **Execution Date:** September 8, 2026
*   **Configuration:** 125,000 steps ($t = 125 \text{ ps}$ using a conservative $\Delta t = 1 \text{ fs}$ stepsize).
*   **Temperature Coupling:** T = 303.15 K using split V-rescale thermostat groups.
*   **Result Metrics:** Completed successfully. Trajectory records indicate fluid lipid tail settlement under rigid heavy-atom position restraints.

### Step 6.2: NPT Equilibration (Initial Density & Pressure Balancing)
*   **Execution Date:** September 8, 2026
*   **Configuration:** 125,000 steps ($t = 125 \text{ ps}$ using $\Delta t = 1 \text{ fs}$ stepsize). 
*   **Pressure Coupling:** Semi-isotropic barostat activated targeting P = 1.0 bar.
*   **Performance Benchmark:** Sustained rendering performance clocking **5.655 ns/day** (Wall Time: 31 minutes, 49 seconds). System box dimensions compressed smoothly to accommodate real-world lipid-packing density limits.

### Step 6.3: NPT Equilibration (Timestep Acceleration Step)
*   **Execution Date:** September 8, 2026
*   **Configuration:** 125,000 steps ($t = 250 \text{ ps}$ using accelerated $\Delta t = 2 \text{ fs}$ stepsize). 
*   **Current Status:** Actively running. Expected performance parameters project a benchmark speed increase to **~10–11 ns/day**, halving the computational overhead per simulated nanosecond frame.

---

## 5. Machine Learning Framework: PINN Baseline Frame
An exploratory baseline for a Physics-Informed Neural Network (PINN) structure was evaluated utilizing a `DeepXDE` and `PyTorch` wrapper script.
*   **Data Boundaries:** The current operational script processes time (t) as the spatial feature input data and the absolute trans-membrane axis coordinate (z) as the training target output.
*   **Loss Equation Physics Constraint:** The optimization loop forces a stationary-state derivative approximation ($dz/dt \approx 0$).
*   **Current Scientific Interpretation:** This script functions strictly as an **initial trajectory-smoothing tool** and stationary baseline verification test. It does *not* model or claim to resolve a full mechanobiological digital twin, free-energy barrier landscape, or active force field projection until extended steered molecular data trajectories are generated.
