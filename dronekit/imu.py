import board
import time
import busio
import adafruit_bno055
import os
from math import sqrt

def connect():
    '''
    Connects to the BNO055 IMU over the Pi's I2C port
    using Adafruit CicuitPython
    '''
    i2c = busio.I2C(board.SCL, board.SDA)
    imu = adafruit_bno055.BNO055_I2C(i2c)
    return imu

def read_acc(IMU):
    '''
    Reads from the accelerometer on the IMU and 
    returns the x, y, z accelerations as well as 
    the acceleration magnitude
    '''
    ax = IMU.acceleration[0]
    ay = IMU.acceleration[1]
    az = IMU.acceleration[2]
    amag = sqrt(ax**2 + ay**2 + az**2)
    return (ax, ay, az, amag) 


def imu_thread_func(data_arr,stop_thread):
    '''
    Used to poll IMU data concurently as a separate thread
    '''
    assert(isinstance(data_arr,list)),"data_arr must be a list"

    IMU = connect() 
    t0 = time.time() # start time 
    FREQ = 0.05 # measurement frequency
    while True:
        t = time.time() - t0 # current time 
        ax,ay,az,amag = read_acc(IMU) # current accelerations
        
        # Print out acceleration data
        print(
            "ax = {:.3f}\tay = {:.3f}\taz = {:.3f}\tamag = {:.3f}\tt = {:.3f} s"
            .format(ax,ay,az,amag,t)
        )
        
        # Save data to the array
        data_arr.append([ax,ay,az,amag,t])
        
        # Kill the thread if stop_thread is set to true
        if stop_thread():
            break

        time.sleep(FREQ)


def write_to_file(arr):
    '''
    write_to_file(arr) writes the data to a text file and the file
    name will be the current date and time and it will be stored
    in a folder in the current directory called "data"
    '''
    assert(len(arr[0]) == 4), "Length of input data [0] is {} but should be 4".format(len(arr[0]))
    
    # Create a data folder if it doesn't exist
    if not os.path.isdir("./data/"):
        os.system("mkdir data")
    
    outfile = "data/out.txt"

    # write the data to a file saved in ./data/
    # each file is a csv .txt file with format (ax,ay,az,time)
    with open(outfile,"w+") as of:
        for line in arr:
            ax = str(line[0])
            ay = str(line[1])
            az = str(line[2])
            amag = str(line[3])
            t = str(line[4])
            of.write("".join(
                [ax,",",ay,",",az,",",amag,",",t,"\n"]
            ))
    print("\nData saved to "+outfile)
