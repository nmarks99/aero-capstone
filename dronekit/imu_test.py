#!/usr/bin/env python3
import os
import sys
sys.path.append("../")
import utils
import imu
import time
from math import sqrt
import threading


stop_thread = threading.Event()
acc_data = []
imu_thread = threading.Thread(target=imu.imu_thread_func,args=(acc_data,stop_thread,))
imu_thread.start()

try:
    while True:
        time.sleep(0.075)
        if len(acc_data) > 0:
            os.system("clear")
            try:
                ax = round(acc_data[-1][0],3)
                ay = round(acc_data[-1][1],3)
                az = round(acc_data[-1][2],3)
            except:
                utils.brint("Missed data point",color="BOLD_RED")
            print(ax,ay,az)


except KeyboardInterrupt:
    imu.write_to_file(acc_data)
    stop_thread.set()





