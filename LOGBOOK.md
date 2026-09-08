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
