#!/usr/bin/env python3
from matplotlib import pyplot as plt
import numpy as np

data_path = "imu_data_3.txt"

amag = []
t = []
with open(data_path,"r") as f:
    for row in f:
        row = row.split(',')
        amag.append(float(row[3]))
        t.append(float(row[4]))


plt.style.use("ggplot")
fig, ax = plt.subplots()
ax.plot(t,amag,'-b',label="Data")
hline = [8.0 for i in range(len(t))]
ax.plot(t,hline,'--r',label="Threshold")
ax.legend()
ax.set(xlabel="Time (s)",ylabel="Acceleration ($m/s^2$)")
#  plt.yticks(np.arange(0,35,2))
plt.show()
fig.savefig("data3.png")        
