#!/usr/bin/env python3
import os
import utils
import imu
import time
from math import sqrt
import threading
import utils

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
                az = round(acc_data[-1][2],2)
            except:
                utils.color_print("Missed data point","BOLD_RED")
            print(ax,ay,az)


except KeyboardInterrupt:
    stop_thread.set()




