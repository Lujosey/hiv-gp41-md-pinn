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
