import deepxde as dde
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("pinn_training_data.csv")
t_train = df["time_ps"].values.reshape(-1, 1)
z_train = df["z_dist_angstrom"].values.reshape(-1, 1)

def gp41_physics(x, y):
    dz_dt = dde.grad.jacobian(y, x)
    return dz_dt - 0 

geom = dde.geometry.TimeDomain(0, 10000)
observe_z = dde.icbc.PointSetBC(t_train, z_train, component=0)

data = dde.data.PDE(geom, gp41_physics, [observe_z], num_domain=200, anchors=t_train)
net = dde.nn.FNN([1, 20, 20, 20, 1], "tanh", "Glorot normal")
model = dde.Model(data, net)

print("Training the Digital Twin...")
model.compile("adam", lr=0.0005)
model.train(iterations=2000)

y_pred = model.predict(t_train)
plt.figure(figsize=(10, 5))
plt.scatter(t_train, z_train, label="GROMACS Data", alpha=0.4)
plt.plot(t_train, y_pred, color='red', linewidth=2, label="PINN Prediction")
plt.savefig("pinn_physics_baseline.png")
print("Success! Image saved as pinn_physics_baseline.png")
