from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import filedialog


# Import data with file dialog
root = tk.Tk()
root.withdraw()
dataPath = filedialog.askopenfilename() # Ask user to select data
print('\n\nPath to data: %s\n' % dataPath)
root.destroy()

force = []
time = []
with open(dataPath,"r") as f:
    for line in f:
        line = line.rstrip().split(",")
        force.append(float(line[0]))
        time.append(float(line[1]))

plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(10,7))
ax.plot(time,force)
ax.set(xlabel="Time(s)", ylabel="Thrust(N)", title="Thrust vs. Time")
plt.show()




