from matplotlib import pyplot as plt

amag = []
t = []
with open("data/imu_data_1.txt","r") as f:
    for row in f:
        row = row.split(',')
        amag.append(float(row[3]))
        t.append(float(row[4]))

fig, ax = plt.subplots()
ax.plot(t,amag)
plt.show()
        
