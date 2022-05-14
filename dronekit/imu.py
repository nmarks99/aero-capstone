#  import board
#  import busio
#  import adafruit_bno055
import os
import random

def connect_imu():
    i2c = busio.I2C(board.SCL, board.SDA)
    imu = adafruit_bno055.BNO055_I2C(i2c)
    return imu

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
            t = str(line[3])
            of.write("".join(
                [ax,",",ay,",",az,",",t,"\n"]
            ))
    print("\nData saved to "+outfile)

def debug():
    a = [1,1,1]
    return a
