# PhD Project Log: HIV-1 gp41 & PINN Dynamics

## [2026-07-08] Entry 01: Environment Benchmarking and System Validation Pipeline

### 1. Objective
- Implement an evidence-led workflow registry for the multi-stage molecular dynamics and machine learning pipeline.
- Establish baseline control metrics for compiler optimizations and topological handling.

### 2. Computational Workflow Architecture
1. **Phase 1: Reference Control Run (HEWL)**
   - Target System: Hen Egg White Lysozyme (HEWL) in a standard aqueous environment.
   - Force Field: OPLS-AA/L all-atom registry.
   - Purpose: Calibration of long-range electrostatics (PME), thermodynamic ensembles (NVT/NPT), and local GROMACS engine benchmarking.

2. **Phase 2: Advanced Biomembrane Assembly (HIV-1 gp41)**
   - Target System: HIV-1 gp41 transmembrane domain fully embedded in an explicit POPC lipid bilayer.
   - Force Field: CHARMM36m parameter registry.
   - Purpose: Evaluation of lipid-protein boundary chemistry, headgroup tilting, and steady-state equilibrium.

3. **Phase 3: Physics-Informed Neural Network (PINN) Trajectory Analysis**
   - Framework: DeepXDE with a PyTorch backend.
   - Purpose: Mapping spatial-temporal coordinates ($Z$-axis distance over time $t$) under explicit first-order differential constraints ($\frac{dz}{dt} \approx 0$) for trajectory smoothing.

### 3. Current Status
- Version control environment successfully initialized.
- Proceeding to Phase 1 data generation.
- markdown
- ## [2026-07-09] Phase 1: HEWL Control Topology Generation

### 1. Technical Actions
- Initialized the reference control run environment inside the local Ubuntu terminal environment.
- Filtered crystal water coordinates (`HOH` residues) from the raw X-ray structure file using `grep`.
- Generated the all-atom system topology mapping.

### 2. Simulation Settings & Provenance
- **Source Structure**: Hen Egg White Lysozyme (HEWL), PDB ID: `1AKI` (Legacy PDB format).
- **Force Field Registry**: OPLS-AA/L all-atom force field (GROMACS Selection Index: `15`).
- **Water Model**: SPC/E explicit water topology (`-water spce`).

### 3. Outputs Generated
- `1aki_clean.pdb`: Solvent-stripped structural coordinates.
- `topol.top`: Core system topology mapping force field atom types, partial charges, and bonding networks.
- `posre.itp`: Heavy-atom position restraint array (force constant = $1000 \text{ kJ}\cdot\text{mol}^{-1}\cdot\text{nm}^{-2}$).

### 4. Next Technical Step
- Execute `gmx editconf` to define cubic boundary dimensions ($1.0\text{ nm}$ envelope) and proceed to explicit box solvation.
