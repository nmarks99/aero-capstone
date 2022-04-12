from dronekit import connect, VehicleMode
import time 

print('begin')
vehicle = connect("com5", baud=115200, wait_ready=True)
print('connected')


print(vehicle.version)
# print(vehicle.is_armed)

# arm the vehicle
vehicle.armed = True



while not vehicle.armed:
    print("Trying to arm")
    time.sleep(0.2)


# Close vehicle object before exiting script
vehicle.close()
