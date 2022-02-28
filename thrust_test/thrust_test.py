#!/usr/bin/env python3
import random
import numpy as np
import os 
from datetime import datetime
import time
import sys

# Passing "debug" as an cmd line input argument will print random numbers instead 
# of actually reading load cell. Good for debugging.
_FLAG = True
if len(sys.argv) == 2:
    if sys.argv[1] == "debug":
        _FLAG = False
elif len(sys.argv) != 1:
    raise ValueError('Invalid number of inputs')


def read_data(DATA_FLAG):

    if DATA_FLAG:
        # read actual data from load cell 

        import RPi.GPIO as gpio
        # Define pins
        RS =18
        EN =23
        D4 =24
        D5 =25
        D6 =8
        D7 =7
        DT =27
        SCK=17
        m1=12
        m2=1

        # Divisor for calibration
        divisor=37142;
        
        gpio.setmode(gpio.BCM) 
        i=0
        Count=0
        gpio.setup(DT, gpio.OUT)
        gpio.setup(SCK, gpio.OUT)
        gpio.output(DT,1)
        gpio.output(SCK,0)
        gpio.setup(DT, gpio.IN)


        while gpio.input(DT) == 1:
            i=0
        for i in range(24):
            gpio.output(SCK,1)
            Count=Count<<1 # a << b = a * 2**b

            gpio.output(SCK,0)
            #time.sleep(0.001)
            if gpio.input(DT) == 0: 
                Count=Count+1
            
        gpio.output(SCK,1)
        Count=Count^0x800000
        Count=Count-8446300
        Count=Count/divisor

        gpio.output(SCK,0)
        return Count 

    else:
        # just return random ints for debugging
        return random.randint(-100,100)


def write_to_file(arr):
    '''
    this function writes the data to a text file and the file
    name will be the current date and time and it will be stored
    in a folder in the current directory called "data"
    '''

    now = datetime.now()
    dt_str = now.strftime("%b-%d_%Hhr-%Mmin-%Ssec")
    outfile = "".join(["data/",dt_str,'.txt'])
    
    # Create a data folder if it doesn't exist
    if not os.path.isdir("./data/"):
        os.system("mkdir data")

    # write the data to a file saved in ./data/
    # each file is a csv .txt file with format DATA, TIMESTAMP
    with open(outfile,"w+") as of:
        for line in arr:      
            of.write("".join([line[0],",",line[1],"\n"]))
    print("Data saved to "+outfile)



data_arr = [] # array to store data 
t0 = time.time() # start time
freq = 0.1 # measurement frequency
try:
    while(True): # probably make while(True)

        val = read_data(DATA_FLAG=_FLAG) # read data from load cell
        t = str(round((time.time()-t0),4)) # get current time 
        print("Thrust = {:.4f} N, Time = {:.4f} s".format(val,float(t)))
        data_arr.append([str(val),t]) # append string of load cell value and timestamp to data array
        time.sleep(freq) # delay between each measurement
finally:
    # Write the data to a file
    write_to_file(data_arr)
