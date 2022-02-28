import random
import numpy as np
import os 
from datetime import datetime
import time


def read_data():
    '''
    TODO: Replace this function with whatever function is used to
    read from the load cell
    '''
    
    # instead of returing random int, return value from load cell
    return random.randint(1,100)


def write_to_file(arr):
    # assert(np.shape(data_arr[0])[1] == 2), 'Input must be be an array of 1x2 arrays'    
    now = datetime.now()
    dt_str = now.strftime("%b-%d_%Hhr-%Mmin-%Ssec")
    outfile = "".join(["./data/",dt_str,'.txt'])
    
    # Create a data folder if it doesn't exist
    if not os.path.isdir("./data/"):
        os.system("mkdir data")

    # write the data to a file saved in ./data/
    # each file is a csv .txt file with format DATA, TIMESTAMP
    with open(outfile,"w+") as of:
        for line in arr:      
            of.write("".join([line[0],",",line[1],"\n"]))



i = 0
data_arr = [] # array to store data 
t0 = time.time() # start time
while(i < 50): # probably make while(True)

    val = read_data() # read data from load cell
    print(val)
    t = str(round((time.time()-t0),4)) # get current time 
    data_arr.append([str(val),t]) # append string of load cell value and timestamp to data array
    i += 1
    time.sleep(0.1) # delay between each measurement

# Write the data to a file
write_to_file(data_arr)
