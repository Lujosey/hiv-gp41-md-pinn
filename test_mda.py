import MDAnalysis as mda
u = mda.Universe("step7_production.tpr", "step7_production.xtc")
print(f"Digital Twin Online: Found {len(u.trajectory)} frames and {len(u.atoms)} atoms in gp41 system.")

