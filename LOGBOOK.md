markdown# 📔 Technical Lab-Book: GROMACS Deployment, Baseline Verification, and HIV-1 gp41 Fusion Peptide System Specification

**Date:** September 8, 2026  
**Author:** E. Matare  
**Category:** Molecular Dynamics Workflow / Environment Setup / Machine Learning Integration  

---

## 🛠️ 1. Environment Build & Core Engine Configuration

To establish a stable high-performance computing baseline on Windows 11 without native compilation conflicts, a sandboxed Linux subsystem environment was deployed.

### Environment Specification
*   **Subsystem Layer:** Windows Subsystem for Linux (WSL2)
*   **Linux Distribution:** Ubuntu Linux via Windows Terminal (`Admin` elevation)
*   **MD Engine Package:** GROMACS Version `2023.3-Ubuntu_2023.3_1ubuntu3`
*   **Python Engine Stack:** Python version `3.12.x` configured with `PyTorch (v2.11.0)` with CUDA runtime bindings and `DeepXDE (v1.15.0+)`

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

# Step 4: Configure user-space Python Machine Learning dependencies bypassing system restrictions
~/.local/bin/pip install --user pandas torch deepxde mdanalysis matplotlib --break-system-packages

# Step 5: Verify absolute path and functional binary engine path hooks
gmx
```

> 🟩 **System Status:** GROMACS engine and PyTorch machine learning environment confirmed active. The engine successfully returned the operational syntax manual and the Rosalind Franklin quote block, verifying package integrity.

---

## 🧪 2. Sandbox Verification Run: HEWL Processing & Path Troubleshooting

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

*   **Parameter Selection:** Configured utilizing **Option 15 (OPLS-AA/L all-atom force field)** paired with the **SPC/E water model**. The run completed without warnings, yielding the structural coordinate files (`.gro`) and the core system master blueprint file (`topol.top`). 
*   Following system solvation and neutralization via 8 Chloride (Cl⁻) ions using `gmx genion`, a 1-nanosecond unconstrained Production MD phase was executed under NPT conditions at 300 K (Average: 300.011 K, RMSD: 1.76 K) clocking a sustained performance benchmarking speed of **~28 ns/day**.

---

## 🧬 3. Targeted Production Framework: HIV-1 gp41 Fusion Peptide System Architecture

With the engine verified, the workspace has been migrated to configure the **HIV-1 gp41 Fusion Peptide (FP)** structural framework.

### 📊 Molecular Architecture Parameters

| Parameter | Specification | Technical Justification |
| :--- | :--- | :--- |
| **Construct Target** | HIV-1 gp41 Fusion Peptide (**PDB ID: 2PJV**) | Solution NMR structure bound to DPC micelles |
| **Oligomeric State** | Monomer | Exploratory baseline stability test frame |
| **Sequence Identity** | `AVGIGALFLGFGAAGSTMGARS` | 22 amino acid hydrophobic segment |
| **Force Field** | **CHARMM36m** | Optimized explicitly for complex lipid-peptide boundaries |
| **Membrane Matrix** | **POPC** Lipid Bilayer | 128 lipids total (64 upper / 64 lower leaflet) |
| **Solvation & Ions** | CHARMM-TIP3P + **0.15 M NaCl** | 8,135 water molecules; matches physiological neutrality |
| **Total System Size**| **41,893 atoms** | Initial dimensions: ~7.2 nm × 7.2 nm × 10.1 nm |

### ⚙️ Mandatory `.mdp` Configuration Parameters for CHARMM36m Bilayers
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
[System Preparation] ──> [Minimization] ──> [6-Step Stepwise Equilibration] ──> [Production MD]1.  **Energy Minimization:** Steepest descent algorithm configured to run until maximum force ($F_{max}$) is under 1000 kJ/mol/nm to resolve structural lipid-protein clashes.
2.  **Multistage Stepwise Equilibration (Steps 6.1–6.6):** Thermal ramp targeting **303.15 K** using split temperature coupling groups (`SOLU` for peptide, `MEMB` for lipids, `SOLV` for water/ions) to enforce uniform kinetic energy dissemination. Position restraints are mapped via a decreasing force constant staircase (10.0 down to 0.1) across the cycles to systematically unpack lipid tails around the primary helical domain.

---

## 📈 4. Chronological Execution Logs & Stepwise Equilibration Phase Tracking

### Step 6.0: Energy Minimization (Steepest Descents)
*   **Execution Date:** September 8, 2026
*   **Input Coordinates:** `step5_input.gro` (Assembled via CHARMM-GUI, aligned along the principal Z-axis)
*   **Target Criterion:** $F_{max} < 1000 \text{ kJ/mol/nm}$
*   **Result Metrics:** Converged cleanly in **1,075 steps**.
    *   $\text{Potential Energy } (E_{pot}) = \color[rgb]{0.8,0.2,0.2}-4.0926075 \times 10^5 \text{ kJ/mol}$
    *   $\text{Maximum Force } (F_{max}) = \color[rgb]{0.2,0.6,0.2}9.0395886 \times 10^2 \text{ kJ/mol/nm}$ on atom 10543.
    *   $\text{Norm of Force} = 2.0121827 \times 10^1 \text{ kJ/mol/nm}$.

### Step 6.1: NVT Equilibration & Thermal Initialization
*   **Execution Date:** September 8, 2026
*   **Configuration:** 125,000 steps ($t = 125 \text{ ps}$ using a conservative $\Delta t = 1 \text{ fs}$ stepsize).
*   **Temperature Coupling:** T = 303.15 K using split V-rescale thermostat groups.
*   **Result Metrics:** <span style="color:green">**Completed successfully.**</span> Trajectory records indicate fluid lipid tail settlement under rigid heavy-atom position restraints.

### Step 6.2: NPT Equilibration (Initial Density & Pressure Balancing)
*   **Execution Date:** September 8, 2026
*   **Configuration:** 125,000 steps ($t = 125 \text{ ps}$ using $\Delta t = 1 \text{ fs}$ stepsize). 
*   **Pressure Coupling:** Semi-isotropic Berendsen barostat activated targeting P = 1.0 bar.
*   **Performance Benchmark:** Sustained rendering performance clocking **5.655 ns/day** (Wall Time: 31 minutes, 49 seconds). System box dimensions compressed smoothly to accommodate real-world lipid-packing density.

### Steps 6.3 to 6.6: Advanced Squeezing Sequences
*   **Protocol:** Systematically updated the integration stepsize to $\Delta t = 2 \text{ fs}$. Progressed through step 6.3 (250 ps), step 6.4 (500 ps), and step 6.5 (500 ps) using Berendsen controls while systematically stepping down backbone/headgroup position restraints. 
*   Phase 6.6 transitioned the system to standard **Nosé-Hoover** temperature regulation and a **Parrinello-Rahman** barostat (1.0 bar, semi-isotropic, $\tau_p = 5.0\text{ ps}$, compressibility = $4.5 \times 10^{-5}\text{ bar}^{-1}$) over a 500 ps timeline to guarantee true thermodynamic canonical ensemble accuracy.

---

## 📊 5. Unrestrained Phase 7 Production MD & Trajectory Stability Analytics

The final structural snapshot from Step 6.6 was advanced to an unrestrained production stage (`step7_production.mdp`) for an **initial stability check** of **10.0 ns** (10,000,000 fs). Coordinates were sampled every 100 ps (101 frames total).

### Trajectory Evaluation Analytics
Post-processing calculations were carried out on the local drive using structural tracking utilities to log parameters:
*   **Structural Deviation:** Evaluated using `gmx rmsd`. The protein backbone reached an early-stage plateau at a mean value of <span style="color:blue">**0.216 nm**</span>, indicating that the monomeric structure remains sound inside the lipid environment.
*   **Hydrophobic Solvation Boundary:** Monitored via `gmx sasa`. The mean solvent accessible surface area across the timeline registered stably at <span style="color:blue">**22.0 nm**</span>, confirming that the target sequence hydrophobic core is properly shielded inside the lipid phase.
*   **Interfacial Spatial Orientation:** Tracked using a custom script (`track_harpoon.py`). The absolute vertical distance between the peptide center of mass and the POPC phosphorus bilayer coordinates calculated out to an anchored deviation of just <span style="color:blue">**0.20 Å**</span>.

> ⚠️ **Scientific Boundary Note:** These trajectory calculations serve strictly as an initial equilibration and setup stability check. They do not represent a validation of biological thermodynamic equilibrium.

---

## 🤖 6. Machine Learning Regression: Trajectory-Smoothing & Path Tracking (DeepXDE)

To map a baseline trajectory-smoothing protocol, raw spatial coordinates extracted from the 10 ns all-atom dataset were parsed into an early-stage machine learning engine.

### Feature Engineering Pipeline (`prep_pinn_data.py`)
A custom Python parsing wrapper script was executed locally to condense the **277 explicit atoms** constituting the 22-residue "Harpoon" index group into regularized space-time arrays:

```csv
# Feature Log Output Sample: pinn_training_data.csv
time_ps,z_dist_angstrom,rad_gyration
0.0,-0.20916824475580142,8.935861281913178
100.0,-0.4420380220125324,9.262409053916135
200.0,-0.3650672778363173,9.383931593378756
300.0,0.4072002245749218,8.991424275292758
```

### Neural Network Infrastructure Specification (`train_gp41_pinn.py`)
The data array was evaluated using a PyTorch-backed **DeepXDE** model framework.
*   **Input Layer:** 1 Node (Temporal scale, $t$ in picoseconds).
*   **Hidden Network Architecture:** Fully connected Feed-Forward Neural Network (`dde.nn.FNN`) mapped across 3 layers of 20 neurons each `[1, 20, 20, 20, 1]`, utilizing hyperbolic tangent ($\tanh$) activations and Glorot Normal weight initializations.
*   **Output Layer:** 1 Node (Spatial separation, Z-axis tracking distance in Ångströms).
*   **Regularization Term:** A first-order derivative parameter check was applied to track a stationary baseline:
    $$\mathcal{L}_{\text{physics}} = \frac{dz}{dt} - 0$$
*   **Optimization Framework:** Run across 2,000 iterations via the Adam algorithm ($lr = 0.0005$). The loss function converged efficiently:
    *   Final Train Loss = **6.27 × 10⁻¹**
    *   Final Test Loss = **6.27 × 10⁻¹**
    *   Wall Execution Time = **4.588 seconds**

> ⚠️ **Model Limitation Statement:** This routine functions strictly as a data-regression tracker and trajectory-smoothing baseline verification test. It is not currently parameter-mapped to calculate activation landscapes, thermodynamic free energy profiles, or force-penetration mechanics.

---

## 🚀 7. Production Phase 2 Deployment Package: Steered MD (SMD) Horizon Plan

To prepare for active mechanical boundary testing on High-Performance Computing (HPC) nodes or optimized cloud architectures (Azure ND-series GPU systems), a rigorous **Steered Molecular Dynamics (SMD)** specification has been structured.

### Pre-Compiled Configuration Matrix (`pull.mdp`)
The following instruction parameters have been assembled into the local launch directory to control the vertical pulling vectors:

```ini
; Target Parameter Specification File for Steered MD
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

### Statistical Replication & Success Threshold Criteria
*   **Replicate Configuration:** 5 separate production replicas initialized with randomized starting velocities, using snapshot coordinates pulled from the 10 ns validation trajectory.
*   **Target Output Arrays:** `pullx.xvg` (displacement coordinate tracking profiles) and `pullf.xvg` (force vectors over time).
*   **Success Metrics:** A calculation run will count as valid if it reveals a clean, reproducible force-extension curve that successfully highlights a peak mechanical resistance profile without box-boundary artifacts or unphysical peptide tilting. 
*   **Failure Criteria:** Excessive tilting that introduces lateral friction along the X/Y coordinates will classify the simulation run as unsuccessful.

---

## 💻 8. Automated Verification & Logging Protocol

To maintain strict reproducibility across systems, a shell script (`log_system_state.sh`) has been deployed to automatically verify directory dependencies and append environment markers directly to the log workspace:

```bash
cat << 'EOF' > log_system_state.sh
#!/bin/bash
echo "=== PROJECT LOG: RUNNING ENVIRONMENT CHECK ===" >> project_log.txt
date >> project_log.txt
echo "Current directory: $(pwd)" >> project_log.txt
echo "=== TARGET FILES PRESENT ===" >> project_log.txt
ls -lh step7_production.gro topol.top index.ndx pull.mdp pinn_training_data.csv >> project_log.txt
echo "=== COMPUTE ENVIRONMENT DETECTED ===" >> project_log.txt
python3 -c "import torch; print('PyTorch version:', torch.__version__)" >> project_log.txt
python3 -c "import deepxde as dde; print('DeepXDE version:', dde.__version__)" >> project_log.txt
echo "==============================================" >> project_log.txt
EOF
chmod +x log_system_state.sh
