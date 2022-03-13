#!/usr/bin/env python3
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import filedialog
import sys
import glob
import os
import scipy.signal as sig


if len(sys.argv) == 1:
    # Import data with file dialog if needed
    root = tk.Tk()
    root.withdraw()
    dataPath = filedialog.askopenfilename() # Ask user to select data
    print('\n\nPath to data: %s\n' % dataPath)

# If user enters "last" as cmd line arg, plot the most recent data file
elif len(sys.argv) == 2:
    if sys.argv[1] == "last":
        list_of_files = glob.glob('./data/*') # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        dataPath = latest_file
    else:
        dataPath = sys.argv[1]
else:
    raise ValueError('Invalid Input')

force = []
time = []
with open(dataPath,"r") as f:
    for line in f:
        line = line.rstrip().split(",")
        force.append(float(line[0]))
        time.append(float(line[1]))
        
force = sig.medfilt(force,5)
force = sig.medfilt(force,5)

plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(10,7))
ax.plot(time,force,"-ro")
ax.set(xlabel="Time(s)", ylabel="Thrust(N)", title="Thrust vs. Time")
plt.show()




