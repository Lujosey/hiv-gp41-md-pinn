markdown# 📔 Technical Lab-Book & Comprehensive Project Log: GROMACS Deployment, Baseline Verification, and HIV-1 gp41 Fusion Peptide System Specification

**Date:** September 8, 2026  
**Author:** E. Matare  
**Category:** Molecular Dynamics Workflow / Environment Setup / Machine Learning Integration  
**Tags:** WSL, Ubuntu, GROMACS-2023, HEWL, HIV-1 gp41, Fusion Peptide, CHARMM36m, POPC, MDAnalysis, PyTorch, DeepXDE, PINN  

---

## 🛠️ 1. Environment Build & Core Engine Configuration

To establish a stable high-performance computing baseline on Windows 11 without native compilation conflicts, a sandboxed Linux subsystem environment was deployed.

### Environment Specification
*   **Subsystem Layer:** Windows Subsystem for Linux (WSL2)
*   **Linux Distribution:** Ubuntu Linux via Windows Terminal (`Admin` elevation)
*   **MD Engine Package:** GROMACS Version `2023.3-Ubuntu_2023.3_1ubuntu3`
*   **Python Engine Stack:** Python version `3.12.x` configured with `PyTorch (v2.11.0)` with CUDA runtime bindings and `DeepXDE (v1.15.0+)`

### Exact Deployment Command History
Powershell Setup:
```powershell
wsl --install -d Ubuntu
# [System Reboot Executed Here to Initialize WSL Kernel Hooks]
```

Ubuntu Bash Setup:
```bash
sudo apt update
sudo apt install gromacs
~/.local/bin/pip install --user pandas torch deepxde mdanalysis matplotlib --break-system-packages
gmx
```

### Output and System Verification
GROMACS environment and PyTorch machine learning dependencies confirmed active. The system successfully returned the operational syntax manual and the Rosalind Franklin quote block, verifying package integrity.

---

## 🧪 2. Sandbox Verification Run: HEWL Processing & Path Troubleshooting

Before deploying the primary gp41 membrane workspace, a validation study was executed using Hen Egg-White Lysozyme (PDB ID: 1AKI) to verify file handling, cleaning scripts, and the `pdb2gmx` topology parser.

### Technical Hurdles & Directory Fixes
1.  **Automated Download Failure:** Standard terminal fetching commands (`wget`) pulled the web interface wrapper (HTML) rather than the raw structural text stream. This caused a fatal error downstream: `Fatal error: An input file contains a line longer than 4096 characters... in fgets2`.
2.  **Resolution Protocol:** The file was manually downloaded via the Windows browser engine from the RCSB repository in pure PDB text format and mapped directly from the Windows directory path into the Linux directory layer.

### Commands & Processing Pipeline
```bash
mkdir lysozyme_tutorial && cd lysozyme_tutorial
cp /mnt/c/Users/ematare.AIRCON/Downloads/1AKI.pdb .
grep -v HOH 1AKI.pdb > 1AKI_clean.pdb
gmx pdb2gmx -f 1AKI_clean.pdb -o 1AKI_processed.gro -water spce -ff oplsaa
```

### Parameter Selection & Run Analytics
Configured utilizing **Option 15 (OPLS-AA/L all-atom force field)** paired with the **SPC/E water model**. The run completed without warnings, yielding the structural coordinate files (`.gro`) and the core system master blueprint file (`topol.top`). Following system solvation and neutralization via 8 Chloride (Cl⁻) ions using `gmx genion`, a 1-nanosecond unconstrained Production MD phase was executed under NPT conditions at 300 K (Average: 300.011 K, RMSD: 1.76 K) clocking a sustained performance benchmarking speed of **~28 ns/day**.

---

## 🧬 3. Targeted Simulation Framework: HIV-1 gp41 Fusion Peptide System Architecture

### 3.1 Molecular System Parameters
*   **Simulated Construct:** HIV-1 gp41 **Fusion Peptide (FP)** segment.
*   **Source Structure:** Solution NMR structure (**PDB ID: 2PJV**, originally bound to DPC micelles).
*   **Residue Range & Sequence:** Residues 1–22; Primary Sequence: `AVGIGALFLGFGAAGSTMGARS`.
*   **Oligomeric State:** Monomer (configured for local exploratory baseline stability testing).
*   **Initial Membrane Orientation:** The longitudinal helical axis of the peptide was oriented parallel to the membrane normal (Z-axis).
*   **Peptide Placement:** The construct was **pre-inserted** symmetrically into the center of the hydrophobic core of the lipid bilayer during coordinate generation via CHARMM-GUI.

### 3.2 Membrane & Force-Field Specification
*   **Preparation Tool:** CHARMM-GUI Membrane Builder.
*   **Force Field Registry:** **CHARMM36m** (explicitly port-optimized for coupled lipid-protein interfacial boundaries).
*   **Lipid Matrix Composition:** Pure, symmetrical **1-palmitoyl-2-oleoyl-sn-glycero-3-phosphocholine (POPC)** bilayer matrix.
*   **Lipid Allocation:** 64 lipids in the upper leaflet, 64 lipids in the lower leaflet (**128 POPC molecules total**).
*   **Solvation Phase:** Explicit **CHARMM-modified TIP3P** water model (**8,135 water molecules**).
*   **Ion Concentration:** Neutralized with explicit counter-ions to achieve a **0.15 M NaCl** physiological concentration (20 Na⁺ [`POT`] / 20 Cl⁻ [`CLA`]).
*   **Initial Box Dimensions:** Orthorhombic cell geometry (X × Y × Z ≈ 7.2 nm × 7.2 nm × 10.1 nm).
*   **Total System Size:** **41,893 explicit atoms**.

### 3.3 Mandatory Non-Bonded `.mdp` Configuration Parameters for CHARMM36m Bilayers
To prevent artificial membrane distortion or structural artifacts, the non-bonded force-switching parameters in GROMACS strictly replicate native CHARMM formatting. The following parameter blocks are established for the minimization and equilibration runs:

```ini
cutoff-scheme    = Verlet      ; Pair list generation scheme
vdwtype          = Cut-off     ; Treat Van der Waals via cutoff
vdw-modifier     = Force-switch; Smoothly switch forces over a set window
rlist            = 1.2         ; Neighbor list cutoff distance (nm)
rvdw             = 1.2         ; Van der Waals cutoff distance (nm)
rvdw-switch      = 1.0         ; Distance where force switching begins (nm)
coulombtype      = PME         ; Particle Mesh Ewald for long-range electrostatics
DispCorr         = no          ; Long-range dispersion corrections must be off for lipid bilayers
```

---

## 📈 4. Chronological Execution Logs & Stepwise Equilibration Phase Tracking

The system was relaxed through a rigorous multi-stage minimization and equilibration sequence prior to the production stage to allow the lipid tails to pack around the newly introduced peptide helix.

### 4.1 Granular Step-by-Step Simulation Protocol Breakdown

*   **Step 6.0: Energy Minimization (EM)**
    *   Input Coordinates / Script: `step5_input.gro` / `step6.0_minimization.mdp`
    *   Ensemble / Algorithm: Steepest Descent (Target Criterion: \(F_{\text{max}} < 1000 \text{ kJ/mol/nm}\))
    *   Timestep / Duration: N/A / Max 5000 steps
    *   Thermostat / Barostat Settings: None
    *   Position Restraints (k): Protein Backbone: 4000, Side Chains: 2000; Lipid Headgroups: 1000
    *   Output Frequency: N/A
    *   *Result Metrics:* Converged cleanly in **1,075 steps**.
        *   Potential Energy (\(E_{pot}\)) = -4.0926075 x 10⁵ kJ/mol
        *   Maximum Force (\(F_{max}\)) = 9.0395886 x 10² kJ/mol/nm on atom 10543.
        *   Norm of Force = 2.0121827 x 10¹ kJ/mol/nm.

*   **Step 6.1: NVT Equilibration & Thermal Initialization**
    *   Input Coordinates / Script: `step6.0.gro` / `step6.1_equilibration.mdp`
    *   Ensemble / Algorithm: NVT / MD Integrator
    *   Timestep / Duration: 1 fs / 125 ps (125,000 steps)
    *   Thermostat / Barostat Settings: Berendsen Thermostat (303.15 K, \(\tau_t = 1.0\text{ ps}\), split coupling groups: `SOLU` for peptide, `MEMB` for lipids, `SOLV` for water/ions)
    *   Position Restraints (k): Protein Backbone: 4000, Side Chains: 2000; Lipid Headgroups: 1000
    *   Output Frequency: Every 50,000 steps
    *   *Result Metrics:* Completed successfully. Trajectory records indicate fluid lipid tail settlement under rigid heavy-atom position restraints.

*   **Step 6.2: NPT Equilibration (Initial Density & Pressure Balancing)**
    *   Input Coordinates / Script: `step6.1.gro` / `step6.2_equilibration.mdp`
    *   Ensemble / Algorithm: NPT / MD Integrator
    *   Timestep / Duration: 1 fs / 125 ps (125,000 steps)
    *   Thermostat / Barostat Settings: Berendsen Thermostat (303.15 K) / Berendsen Semi-Isotropic Barostat (1.0 bar, \(\tau_p = 5.0\text{ ps}\))
    *   Position Restraints (k): Protein Backbone: 2000, Side Chains: 1000; Lipid Headgroups: 400
    *   Output Frequency: Every 50,000 steps
    *   *Result Metrics:* Achieved sustained rendering performance clocking **5.655 ns/day** (Wall Time: 31 minutes, 49 seconds). System box dimensions compressed smoothly to accommodate real-world lipid-packing density.

*   **Step 6.3: NPT Equilibration (Timestep Escalation)**
    *   Input Coordinates / Script: `step6.2.gro` / `step6.3_equilibration.mdp`
    *   Ensemble / Algorithm: NPT / MD Integrator
    *   Timestep / Duration: 2 fs / 250 ps (125,000 steps)
    *   Thermostat / Barostat Settings: Berendsen Thermostat (303.15 K) / Berendsen Semi-Isotropic Barostat (1.0 bar)
    *   Position Restraints (k): Protein Backbone: 1000, Side Chains: 500; Lipid Headgroups: 400
    *   Output Frequency: Every 50,000 steps

*   **Step 6.4: NPT Equilibration (Restraint Step-Down Stage 1)**
    *   Input Coordinates / Script: `step6.3.gro` / `step6.4_equilibration.mdp`
    *   Ensemble / Algorithm: NPT / MD Integrator
    *   Timestep / Duration: 2 fs / 500 ps (250,000 steps)
    *   Thermostat / Barostat Settings: Berendsen Thermostat (303.15 K) / Berendsen Semi-Isotropic Barostat (1.0 bar)
    *   Position Restraints (k): Protein Backbone: 500, Side Chains: 200; Lipid Headgroups: 200
    *   Output Frequency: Every 50,000 steps
    *   *   **Step 6.5: NPT Equilibration (Restraint Step-Down Stage 2)**
    *   Input Coordinates / Script: `step6.4.gro` / `step6.5_equilibration.mdp`
    *   Ensemble / Algorithm: NPT / MD Integrator
    *   Timestep / Duration: 2 fs / 500 ps (250,000 steps)
    *   Thermostat / Barostat Settings: Berendsen Thermostat (303.15 K) / Berendsen Semi-Isotropic Barostat (1.0 bar)
    *   Position Restraints (k): Protein Backbone: 200, Side Chains: 50; Lipid Headgroups: 40
    *   Output Frequency: Every 50,000 steps

*   **Step 6.6: NPT Equilibration (Production Ensemble Transition)**
    *   Input Coordinates / Script: `step6.5.gro` / `step6.6_equilibration.mdp`
    *   Ensemble / Algorithm: NPT / MD Integrator
    *   Timestep / Duration: 2 fs / 500 ps (250,000 steps)
    *   Thermostat / Barostat Settings: **Nosé-Hoover Thermostat** (303.15 K, split coupling groups) / **Parrinello-Rahman Semi-Isotropic Barostat** (1.0 bar, \(\tau_p = 5.0\text{ ps}\), compressibility = 4.5 × 10⁻⁵ bar⁻¹)
    *   Position Restraints (k): Protein Backbone: 50, Side Chains: 0; Lipid Headgroups: 0
    *   Output Frequency: Every 50,000 steps

*   **Step 7: Production MD Baseline Run**
    *   Input Coordinates / Script: `step6.6.gro` / `step7_production.mdp`
    *   Ensemble / Algorithm: NPT / MD Integrator
    *   Timestep / Duration: 2 fs / **10.0 ns** (5,000,000 steps)
    *   Thermostat / Barostat Settings: **Nosé-Hoover Thermostat** (303.15 K, split groups) / **Parrinello-Rahman Semi-Isotropic Barostat** (1.0 bar)
    *   Position Restraints (k): **None (Fully Unrestrained)**
    *   Output Frequency: Every 50,000 steps (Data sampled every 100 ps, total 101 frames)

---

## 📊 5. Unrestrained Trajectory Performance (10 ns Initial Stability Check)

The 10 ns production phase functions strictly as an **initial stability check** to assess structural drift under the CHARMM36m force field, rather than as a complete biological validation. 

### Trajectory Evaluation Averages
Post-processing calculations were carried out on the local drive using structural tracking utilities (`gmx rmsd`, `gmx sasa`, `gmx energy`) to pull thermodynamic metrics across the 101 saved frames:
*   **Structural Deviation (RMSD):** The protein backbone reached an early-stage plateau at a mean value of **0.216 nm** (reported correctly in nanometers, avoiding squared notation metrics).
*   **System Temperature:** Maintained structural distribution profile centering tightly around **303.11 K**.
*   **System Pressure:** Fluctuated around a mean of **1.03 bar** (consistent with small-system NPT noise components).
*   **Density Profile:** Consolidated uniformly at an average liquid density phase of **1012.4 kg/m³**.
*   **Hydrophobic Solvation Boundary (SASA):** Calculated via `gmx sasa`. The mean solvent accessible surface area settled at **22.0 nm**, confirming that the hydrophobic peptide segment remained stably shielded from full solvent contact within the lipid tails.
*   **Center-of-Mass (COM) Displacement:** Tracked using a custom script (`track_harpoon.py`). The absolute vertical distance between the peptide COM and the POPC phosphorus bilayer reference matrix coordinates calculated out to an anchored deviation of just **0.20 Å**.

> ⚠️ **Scientific Boundary Note:** These trajectory calculations serve strictly as an initial equilibration and setup stability check. They do not represent a validation of full biological thermodynamic equilibrium.

---

## 🤖 6. Machine Learning Regression: Stationary-Baseline Verification Test

To test data parsing protocols, a prototype machine learning pipeline was constructed using **DeepXDE** on top of a **PyTorch** mathematics backend. At this stage, this routine serves strictly as a **stationary-baseline or trajectory-smoothing test** to filter out thermal noise; it is insufficient to claim a force landscape or a free-energy insertion barrier.

### 💻 Feature Extraction Configuration (`prep_pinn_data.py`)
A custom Python parsing wrapper script was executed locally to condense the **277 explicit atoms** constituting the 22-residue "Harpoon" index group into regularized space-time arrays:

```csv
time_ps,z_dist_angstrom,rad_gyration
0.0,-0.20916824475580142,8.935861281913178
100.0,-0.4420380220125324,9.262409053916135
200.0,-0.3650672778363173,9.383931593378756
300.0,0.4072002245749218,8.991424275292758
```

### 🧠 Neural Network Infrastructure (`train_gp41_pinn.py`)
*   **Input Layer (X):** Time (t) in picoseconds.
*   **Hidden Network Architecture:** Fully connected Feed-Forward Neural Network (`dde.nn.FNN`) mapped across 3 layers of 20 neurons each ``, utilizing hyperbolic tangent (\(\tanh\)) activations and Glorot Normal weight initializations.
*   **Output Layer (Y):** Spatial separation, Z-axis tracking distance in Angstroms.
*   **Regularization Term:** Constrained via a basic first-order differential velocity check:
    $$\mathcal{L}_{\text{physics}} = \frac{dz}{dt} - 0 = 0$$
*   **Optimization Framework:** Run across 2,000 iterations via the Adam algorithm (lr = 0.0005). The loss function converged efficiently:
    *   Final Train Loss = **6.27 × 10⁻¹**
    *   Final Test Loss = **6.27 × 10⁻¹**
    *   Wall Execution Time = **4.588 seconds**
*   **Result Evaluation:** The process generated a smoothed path configuration output (`pinn_physics_baseline.png`). 

> ⚠️ **Model Limitation Statement:** This routine functions strictly as a data-regression tracker and trajectory-smoothing baseline verification test. It is not currently parameter-mapped to calculate activation landscapes, thermodynamic free energy profiles, or force-penetration mechanics.

---

## 🚀 7. Steered Molecular Dynamics (SMD) Project Strategy Plan

Prior to deployment on the High-Performance Computing (HPC) parallel cluster infrastructure, a detailed **Steered Molecular Dynamics (SMD)** strategy has been prepared. This stage is designed to map active-force profiles rather than the stationary conditions verified locally.

### ⚙️ Pre-Compiled Configuration Parameters (`pull.mdp` directives)
```ini
pull                     = yes
pull_ncoords             = 1          ; Single reaction coordinate tracking
pull_ngroups             = 2          ; Pulled target and reference matrix
pull_group1_name         = Harpoon    ; Target index mapping containing the 277 peptide atoms
pull_group2_name         = POPC       ; Bilayer phosphorus coordinate reference matrix
pull_coord1_type         = umbrella   ; Harmonic spring constraint potential
pull_coord1_geometry     = distance   ; Direct coordinate vector tracking
pull_coord1_dim          = N N Y      ; Axis constraint: Unidirectional pulling along Z-normal
pull_coord1_groups       = 1 2        ; Pull Group 1 relative to Group 2
pull_coord1_start        = yes        ; Begin pulling from local starting position
pull_coord1_rate         = 0.01       ; Velocity constraint: 0.01 nm/ps
pull_coord1_k            = 1000       ; Constant spring stiffness: 1000 kJ/mol/nm^2
```

### Pull Group, Direction, and Boundaries Definition
*   **Pull Group:** Group `Harpoon` (consisting of all 277 explicit atoms of the 22-residue peptide).
*   **Reference Group:** Group `POPC` (specifically mapping the phosphorus atoms of the lipid matrix to represent the bilayer center).
*   **Pulling Direction:** Unidirectional pulling along the Z-axis (membrane normal vector).
*   **Spring Constant (k):** $1000 \text{ kJ}\cdot\text{mol}^{-1}\cdot\text{nm}^{-2}$.
*   **Pulling Velocity (v):** $0.01 \text{ nm/ps}$.
*   **Statistical Replication Strategy:** 5 independent configuration runs initialized with randomized velocity fields from frame snapshots extracted from the 10 ns baseline check trajectory.
*   **Expected Diagnostic Outputs:** `pullx.xvg` (displacement tracking values) and `pullf.xvg` (force vectors over time).
*   **Success Evaluation Criteria:** A calculation run will count as valid if it reveals a clean, reproducible force-extension curve that highlights a peak mechanical resistance profile without box-boundary artifacts or unphysical structural distortions.
*   **Failure Evaluation Criteria:** Excessive peptide tilting that introduces lateral friction along the X/Y coordinates will classify the simulation run as unsuccessful.

---

## 💻 8. Automated Verification & Logging Script (`log_system_state.sh`)

To maintain strict reproducibility across systems, a shell script has been deployed to automatically verify directory dependencies and append environment markers directly to the log workspace:

```bash
#!/bin/bash
echo "=== PROJECT LOG: RUNNING ENVIRONMENT CHECK ===" >> project_log.txt
date >> project_log.txt
echo "Current directory: \$(pwd)" >> project_log.txt
echo "=== TARGET FILES PRESENT ===" >> project_log.txt
ls -lh step7_production.gro topol.top index.ndx pull.mdp pinn_training_data.csv >> project_log.txt
echo "=== COMPUTE ENVIRONMENT DETECTED ===" >> project_log.txt
python3 -c "import torch; print('PyTorch version:', torch.__version__)" >> project_log.txt
python3 -c "import deepxde as dde; print('DeepXDE version:', dde.__version__)" >> project_log.txt
echo "==============================================" >> project_log.txt

h version:', torch.__version__)" >> project_log.txt python3 -c "import deepxde as dde; print('DeepXDE version:', dde.__version__)" >> project_log.txt echo "==============================================" >> project_log.txt 
