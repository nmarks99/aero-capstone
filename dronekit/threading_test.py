import threading
import time 
import os

def func(arr):
    t0 = time.time()
    while True:
        elap = time.time() - t0
        
        arr.append(elap)
        time.sleep(0.1)
        global stop_thread
        if stop_thread:
            break


# Define thread

stop_thread = False
arr = []
x = threading.Thread(target=func,args=(arr,))
x.start() # run the thread

try:
    while True:
        print("running")
        time.sleep(1)
        print(len(arr))

except KeyboardInterrupt:
   print("out = ",arr)
   stop_thread = True
   #  x.join()
#  print(threading.activeCount())
#  print("\x1B[0m")


