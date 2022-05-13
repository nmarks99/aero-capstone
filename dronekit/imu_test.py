#!/usr/bin/env python3
import imu
import time

IMU = imu.connect_imu()

data = []
t0 = time.time()
try:
    while True:
        t_now = time.time() - t0
        ax = IMU.acceleration[0]
        ay = IMU.acceleration[1]
        az = IMU.acceleration[3]
        data.append([ax,ay,az],t_now)
        time.sleep(0.05)
except KeyboardInterrupt:
    imu.write_to_file(data)
    exit()



