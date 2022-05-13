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
    
    outfile = "data/out.txt"

    # Create a data folder if it doesn't exist
    if not os.path.isdir("./data/"):
        os.system("mkdir data")

    # write the data to a file saved in ./data/
    # each file is a csv .txt file with format DATA, TIMESTAMP
    with open(outfile,"w+") as of:
        for line in arr:      
            of.write("".join([str(line[0][0]),",",str(line[0][1]),",",str(line[0][2]),",",str(line[1]),"\n"]))
    print("\nData saved to "+outfile)

def debug():
    data = [] 
    for i in range(100):
        a1 = random.randint(-100, 100)
        a = (a1,a1,a1)
        t = random.randint(-100,100)
        data.append([a,t])
    return data 
