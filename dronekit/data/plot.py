from matplotlib import pyplot as plt
import numpy as np

amag = []
t = []
with open("imu_data_1.txt","r") as f:
    for row in f:
        row = row.split(',')
        amag.append(float(row[3]))
        t.append(float(row[4]))



fig, ax = plt.subplots()
ax.plot(t,amag,'-b',"Data")
ax.grid()
hline = [8.0 for i in range(len(t))]
ax.plot(t,hline,'--r',label="Threshold")
ax.legend()
plt.show()
        
