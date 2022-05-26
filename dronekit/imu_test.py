#!/usr/bin/env python3
import os
import utils
import imu
import time
from math import sqrt
import threading
import utils


#
#  IMU = imu.connect_imu()
#
#  data = []
#  t0 = time.time()
#  try:
    #  while True:
        #  t_now = time.time() - t0
        #  ax = IMU.acceleration[0]
        #  ay = IMU.acceleration[1]
        #  az = IMU.acceleration[3]
        #  amag = sqrt(ax**2 + ay**2 + az**2)
        #  data.append([ax,ay,az,amag,t_now])
        #  print(ax, ay, az,amag,t_now)
        #  time.sleep(0.05)
#  except KeyboardInterrupt:
    #  imu.write_to_file(data)
    #  exit()
#
#

stop_thread = threading.Event()
acc_data = []
imu_thread = threading.Thread(target=imu.imu_thread_func,args=(acc_data,stop_thread,))
imu_thread.start()

try:
    while True:
        time.sleep(0.075)
        if len(acc_data) > 0:
            os.system("clear")
            print(acc_data[-1])


except KeyboardInterrupt:
    stop_thread.set()





