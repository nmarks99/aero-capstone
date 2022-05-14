import board
import busio
import adafruit_bno055
import os
from math import sqrt

def connect_imu():
    i2c = busio.I2C(board.SCL, board.SDA)
    imu = adafruit_bno055.BNO055_I2C(i2c)
    return imu

def read_acc(IMU):
    ax = IMU.acceleration[0]
    ay = IMU.acceleration[1]
    az = IMU.acceleration[2]
    amag = sqrt(ax**2 + ay**2 + az**2)
    return (ax, ay, az, amag) 
    

def write_to_file(arr):
    '''
    write_to_file(arr) writes the data to a text file and the file
    name will be the current date and time and it will be stored
    in a folder in the current directory called "data"
    '''
    
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
