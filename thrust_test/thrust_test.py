#!/usr/bin/env python3
import random
import numpy as np
import os 
from datetime import datetime
import time
import sys

# Passing "debug" as an cmd line input argument will print random numbers instead 
# of actually reading load cell. Good for debugging.
FLAG = True
if len(sys.argv) == 2:
    if sys.argv[1] == "debug":
        FLAG = False
    else:
        try:
            throttle_val = float(sys.argv[1])
        except:
            raise ValueError("Input throttle value cannot be converted to float")
elif len(sys.argv) != 1:
    raise ValueError('Invalid number of inputs')



if FLAG:
    # only import RPI.GPIO and pigpio
    import RPi.GPIO as gpio
    import pigpio

    pi = pigpio.pi()
    ESC = 4 # ESC connected to GPIO pin #4
    pi.set_servo_pulsewidth(ESC,0) # initially set pulse width to zero



def read_data(DATA_FLAG):
    '''
    read_data(DATA_FLAG) reads data a single value from the load 
    cell and returns it as a float. If DATA_FLAG == False, then
    instead of reading the load cell, it just returns a random integer
    '''
    if DATA_FLAG:
        # read actual data from load cell 
        DT =27
        SCK=17

        # Divisor for calibration
        divisor=37142
        
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
            time.sleep(0.001)
            if gpio.input(DT) == 0: 
                Count=Count+1
            
        gpio.output(SCK,1)
        Count=Count^0x800000
        Count=Count-8279641.8

        Count=Count/divisor

        gpio.output(SCK,0)
        return Count 

    else:
        # just return random ints for debugging
        return random.randint(-100,100)



def write_to_file(arr):
    '''
    write_to_file(arr) writes the data to a text file and the file
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
    print("\nData saved to "+outfile)



def throttle(val):
    '''
    throttle(val) sets pulse width for PWM signal given a value between 0 and 1
    corresponding to a percentage of max throttle
    '''

    assert(val >= 0 and val <= 1), 'Throttle is a value between 0(min) and 1 (max)'
    pulse_width = 1000 + 1000*val
    pi.set_servo_pulsewidth(ESC,pulse_width)
    




# =================================
# Main program loop
# =================================

data_arr = []       # array to store data 
t0 = time.time()    # start time
freq = 0.01        # measurement frequency
# throttle_val = 1.0 # throttle between 0 (min) and 1 (max)

try:
    while(True): 

        t = round((time.time()-t0),4) # get current time 

        if (t > 5):
            throttle(throttle_val)
        
        val = read_data(DATA_FLAG=FLAG) # read data from load cell
        print("Thrust = {:.4f} N, Time = {:.4f} s".format(val,float(t)))
        t_str = str(t)
        data_arr.append([str(val),t_str]) # append string of load cell value and timestamp to data array
        time.sleep(freq) # delay between each measurement

except KeyboardInterrupt:
    write_to_file(data_arr)
    throttle(0.0)
