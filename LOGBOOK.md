markdown# Technical Lab-Book: GROMACS Deployment, Baseline Verification, and HIV-1 gp41 Fusion Peptide System Specification

**Date:** September 8, 2026  
**Author:** E. Matare  
**Category:** Molecular Dynamics Workflow / Environment Setup  
**Tags:** WSL, Ubuntu, GROMACS-2023, HEWL, HIV-1 gp41, Fusion Peptide, CHARMM36m, POPC, DeepXDE, PyTorch

---

## 1. Environment Build & Core Engine Configuration

To establish a stable high-performance computing baseline on Windows 11 without native compilation conflicts, a sandboxed Linux subsystem environment was deployed.

### Environment Specification
*   **Subsystem Layer:** Windows Subsystem for Linux (WSL2)
*   **Linux Distribution:** Ubuntu Linux via Windows Terminal (`Admin` elevation)
*   **MD Engine Package:** GROMACS Version `2023.3-Ubuntu_2023.3_1ubuntu3`
*   **Python Engine Stack:** Python version `3.12.x` configured with `PyTorch (v2.11.0)` and `DeepXDE (v1.15.0+)`

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

*   **Result:** GROMACS environment and PyTorch machine learning dependencies confirmed active. The system successfully returned the operational syntax manual and the Rosalind Franklin quote block, verifying package integrity.

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

## 3. Targeted Simulation Framework: HIV-1 gp41 Fusion Peptide System Architecture

### 3.1 Molecular System Parameters
*   **Simulated Construct:** HIV-1 gp41 **Fusion Peptide (FP)** segment.
*   **Source Structure:** Solution NMR structure (**PDB ID: 2PJV**, originally bound to DPC micelles).
*   **Residue Range & Sequence:** Residues 1–22; Primary Sequence: `AVGIGALFLGFGAAGSTMGARS`.
*   **Oligomeric State:** Monomer (configured for local exploratory baseline stability testing).
*   **Initial Membrane Orientation:** The longitudinal helical axis of the peptide was oriented parallel to the membrane normal ($Z$-axis).
*   **Peptide Placement:** The construct was **pre-inserted** symmetrically into the center of the hydrophobic core of the lipid bilayer during coordinate generation via CHARMM-GUI.

### 3.2 Membrane & Force-Field Specification
*   **Preparation Tool:** CHARMM-GUI Membrane Builder.
*   **Force Field Registry:** **CHARMM36m** (explicitly port-optimized for coupled lipid-protein interfacial boundaries).
*   **Lipid Matrix Composition:** Pure, symmetrical **1-palmitoyl-2-oleoyl-sn-glycero-3-phosphocholine (POPC)** bilayer matrix.
*   **Lipid Allocation:** 64 lipids in the upper leaflet, 64 lipids in the lower leaflet (**128 POPC molecules total**).
*   **Solvation Phase:** Explicit **CHARMM-modified TIP3P** water model (**8,135 water molecules**).
*   **Ion Concentration:** Neutralized with explicit counter-ions to achieve a **0.15 M NaCl** physiological concentration (20 $Na^+$ [`POT`] / 20 $Cl^-$ [`CLA`]).
*   **Initial Box Dimensions:** Orthorhombic cell geometry ($X \times Y \times Z \approx 7.2\text{ nm} \times 7.2\text{ nm} \times 10.1\text{ nm}$).
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

## 4. Chronological Execution Logs & Stepwise Equilibration Phase Tracking

The system was relaxed through a rigorous multi-stage minimization and equilibration sequence prior to the production stage to allow the lipid tails to pack around the newly introduced peptide helix.

### Table 4.1: Technical MD Protocol Breakdown

| Protocol Step | Input Coordinates / Script | Ensemble | Timestep | Duration | Thermostat / Barostat Settings | Position Restraints ($k$ in $\text{kJ}\cdot\text{mol}^{-1}\cdot\text{nm}^{-2}$) | Output Frequency (`.trr` / `.xtc`) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Step 6.0: EM** | `step5_input.gro` / `step6.0_minimization.mdp` | N/A | N/A | Max 5000 steps | Steepest Descent ($F_{\text{max}} < 1000$) | Protein BB: 4000, SC: 2000; Lipid Headgroups: 1000 | N/A |
| **Step 6.1: NVT** | `step6.0.gro` / `step6.1_equilibration.mdp` | NVT | 1 fs | 125 ps | Berendsen ($303.15\text{ K}$, $\tau_t = 1.0\text{ ps}$) | Protein BB: 4000, SC: 2000; Lipid Headgroups: 1000 | 50,000 steps |
| **Step 6.2: NPT 1**| `step6.1.gro` / `step6.2_equilibration.mdp` | NPT | 1 fs | 125 ps | Berendsen ($303.15\text{ K}$) / Berendsen semi-isotropic ($1.0\text{ bar}$, $\tau_p = 5.0\text{ ps}$) | Protein BB: 2000, SC: 1000; Lipid Headgroups: 400 | 50,000 steps |
| **Step 6.3: NPT 2**| `step6.2.gro` / `step6.3_equilibration.mdp` | NPT | 2 fs | 250 ps | Berendsen ($303.15\text{ K}$) / Berendsen semi-isotropic ($1.0\text{ bar}$) | Protein BB: 1000, SC: 500; Lipid Headgroups: 400 | 50,000 steps |
| **Step 6.4: NPT 3**| `step6.3.gro` / `step6.4_equilibration.mdp` | NPT | 2 fs | 500 ps | Berendsen ($303.15\text{ K}$) / Berendsen semi-isotropic ($1.0\text{ bar}$) | Protein BB: 500, SC: 200; Lipid Headgroups: 200 | 50,000 steps |
| **Step 6.5: NPT 4**| `step6.4.gro` / `step6.5_equilibration.mdp` | NPT | 2 fs | 500 ps | Berendsen ($303.15\text{ K}$) / Berendsen semi-isotropic ($1.0\text{ bar}$) | Protein BB: 200, SC: 50; Lipid Headgroups: 40 | 50,000 steps |
| **Step 6.6: NPT 5**| `step6.5.gro` / `step6.6_equilibration.mdp` | NPT | 2 fs | 500 ps | **Nosé-Hoover** ($303.15\text{ K}$, split groups) / **Parrinello-Rahman** semi-isotropic ($1.0\text{ bar}$) | Protein BB: 50, SC: 0; Lipid Headgroups: 0 | 50,000 steps |
| **Step 7: Prod**   | `step6.6.gro` / `step7_production.mdp` | NPT | 2 fs | **10.0 ns** | **Nosé-Hoover** ($303.15\text{ K}$, split groups) / **Parrinello-Rahman** semi-isotropic ($1.0\text{ bar}$) | **None (Fully Unrestrained)** | 50,000 steps (Every 100 ps) |

#### Step 6.0 Minimization Results Matrix:
*   Converged cleanly in **1,075 steps**.
*   $\text{Potential Energy } (E_{pot}) = -4.0926075 \times 10^5 \text{ kJ/mol}$
*   $\text{Maximum Force } (F_{max}) = 9.0395886 \times 10^2 \text{ kJ/mol/nm}$ on atom 10543.
*   $\text{Norm of Force} = 2.0121827 \times 10^1 \text{ kJ/mol/nm}$.

#### Step 6.2 Benchmarking Performance:
*   Sustained rendering performance clocking **5.655 ns/day** (Wall Time: 31 minutes, 49 seconds). System box dimensions compressed smoothly to accommodate real-world lipid-packing density.

---

## 5. Unrestrained Trajectory Performance (10 ns Initial Stability Check)
