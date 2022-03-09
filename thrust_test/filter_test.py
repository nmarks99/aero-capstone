import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as s

F = []
t = []

with open("data/Feb-23_17hr-44min-41sec.txt",'r') as f:
    for row in f:
        row = row.split(",")
        F.append(float(row[0]))   
        t.append(float(row[1]))


F = np.array(F)
t = np.array(t)

F_filt = s.medfilt(F,3)

fig, ax = plt.subplots()

# ax.plot(t,F,'-b')
ax.plot(t,F_filt,'-r')
plt.show()