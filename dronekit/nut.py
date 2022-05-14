#!/usr/bin/env python3

"""
set_attitude_target.py: (Copter Only)
This example shows how to move/direct Copter and send commands
 in GUIDED_NOGPS mode using DroneKit Python.
Caution: A lot of unexpected behaviors may occur in GUIDED_NOGPS mode.
        Always watch the drone movement, and make sure that you are in dangerless environment.
        Land the drone as soon as possible when it shows any unexpected behavior.
Tested in Python 2.7.10
"""

from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions
import time
import math

def arm_and_takeoff_nogps(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude without GPS data.
    """

    ##### CONSTANTS #####
    DEFAULT_TAKEOFF_THRUST = 0.7
    SMOOTH_TAKEOFF_THRUST = 0.6

    #  print("Basic pre-arm checks")
    # Don't let the user try to arm until autopilot is ready
    # If you need to disable the arming check,
    # just comment it with your own responsibility.
    #  while not vehicle.is_armable:
        #  print(" Waiting for vehicle to initialise...")
        #  time.sleep(1)

    #  print("Arming motors")
    # Copter should arm in GUIDED_NOGPS mode
    vehicle.mode = VehicleMode("GUIDED_NOGPS")
    #  vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        vehicle.armed = True
        time.sleep(1)

    print("Taking off!")

    thrust = DEFAULT_TAKEOFF_THRUST
    while True:
        current_altitude = vehicle.location.global_relative_frame.alt
        print(" Altitude: %f  Desired: %f" %
              (current_altitude, aTargetAltitude))
        if current_altitude >= aTargetAltitude*0.95: # Trigger just below target alt.
            print("Reached target altitude")
            break
        elif current_altitude >= aTargetAltitude*0.6:
            thrust = SMOOTH_TAKEOFF_THRUST
        set_attitude(thrust = thrust)
        time.sleep(0.2)





def send_attitude_target(roll_angle = 0.0, pitch_angle = 0.0,
                         yaw_angle = None, yaw_rate = 0.0, use_yaw_rate = False,
                         thrust = 0.5):
    """
    use_yaw_rate: the yaw can be controlled using yaw_angle OR yaw_rate.
                  When one is used, the other is ignored by Ardupilot.
    thrust: 0 <= thrust <= 1, as a fraction of maximum vertical thrust.
            Note that as of Copter 3.5, thrust = 0.5 triggers a special case in
            the code for maintaining current altitude.
    """
    if yaw_angle is None:
        # this value may be unused by the vehicle, depending on use_yaw_rate
        yaw_angle = vehicle.attitude.yaw
    # Thrust >  0.5: Ascend
    # Thrust == 0.5: Hold the altitude
    # Thrust <  0.5: Descend
    msg = vehicle.message_factory.set_attitude_target_encode(
        0, # time_boot_ms
        1, # Target system
        1, # Target component
        0b00000000 if use_yaw_rate else 0b00000100,
        to_quaternion(roll_angle, pitch_angle, yaw_angle), # Quaternion
        0, # Body roll rate in radian
        0, # Body pitch rate in radian
        math.radians(yaw_rate), # Body yaw rate in radian/second
        thrust  # Thrust
    )
    vehicle.send_mavlink(msg)

def set_attitude(roll_angle = 0.0, pitch_angle = 0.0,
                 yaw_angle = None, yaw_rate = 0.0, use_yaw_rate = False,
                 thrust = 0.5, duration = 0):
    """
    Note that from AC3.3 the message should be re-sent more often than every
    second, as an ATTITUDE_TARGET order has a timeout of 1s.
    In AC3.2.1 and earlier the specified attitude persists until it is canceled.
    The code below should work on either version.
    Sending the message multiple times is the recommended way.
    """
    send_attitude_target(roll_angle, pitch_angle,
                         yaw_angle, yaw_rate, False,
                         thrust)
    start = time.time()
    while time.time() - start < duration:
        send_attitude_target(roll_angle, pitch_angle,
                             yaw_angle, yaw_rate, False,
                             thrust)
        time.sleep(0.1)
    # Reset attitude, or it will persist for 1s more due to the timeout
    send_attitude_target(0, 0,
                         0, 0, True,
                         thrust)

def to_quaternion(roll = 0.0, pitch = 0.0, yaw = 0.0):
    """
    Convert degrees to quaternions
    """
    t0 = math.cos(math.radians(yaw * 0.5))
    t1 = math.sin(math.radians(yaw * 0.5))
    t2 = math.cos(math.radians(roll * 0.5))
    t3 = math.sin(math.radians(roll * 0.5))
    t4 = math.cos(math.radians(pitch * 0.5))
    t5 = math.sin(math.radians(pitch * 0.5))

    w = t0 * t2 * t4 + t1 * t3 * t5
    x = t0 * t3 * t4 - t1 * t2 * t5
    y = t0 * t2 * t5 + t1 * t3 * t4
    z = t1 * t2 * t4 - t0 * t3 * t5

    return [w, x, y, z]




import imu

# Connect to pixhawk
vehicle = connect("/dev/serial0",baud=921600,wait_ready=True)

input("Press enter to continue")

# Take off 2.5m in GUIDED_NOGPS mode.
arm_and_takeoff_nogps(7.0)

# Hold the position for 3 seconds.
print("Hold position for 3 seconds")
set_attitude(duration = 3)

IMU = imu.connect_imu()

#  # Set thrust to 0
#  set_attitude(thrust=0.0,duration=0.2)
#  set_attitude(thrust=1.0,duration=0.2)

# Hold altitude at wherever it is at now
#vehicle.mode = VehicleMode("ALT_HOLD")
#  time.sleep(3)



# Define constants
DROPPED = False # Flag for if drop has been detected or not
DROP_THRESHOLD = 8.8 # TODO: update thresholds
HOVER_THRESHOLD = 8.8
ARM_SERVO = 9
LEG_SERVO = 10 # TODO: check servo number

t0 = time.time() # time = 0 here
acc_data = [] # array to store acceleration data 
try:
    while True:
        
        # Get current time and acceleration
        t_now = time.time() - t0
        (ax, ay, az, amag) = imu.read_acc(IMU)
        #  acc_data.append([ax, ay, az, amag, t_now])

        # Print out acceleration data
        #  print(
            #  "ax = {:.3f}\tay = {:.3f}\taz = {:.3f}\tamag = {:.3f}\tt = {:.3f} s"
            #  .format(ax,ay,az,amag,t_now)
        #  )

        print(ax, ay, az, amag, t_now)

        if not DROPPED:
            # Check if drop detected
            if amag >= DROP_THRESHOLD:
                DROPPED = True
                 
                # Deploy arms
                print("Arms deployed")
                # dklib.set_servo(vehicle, ARM_SERVO, "HIGH")
                
                # Set throttle to 100%
                print("Throttle set to 100%")
                set_attitude(thrust=1.0)

            elif vehicle.location.global_relative_frame.alt <= 3.0:
                print("PANIC! ABORT MISSION!")
                set_attitude(thrust=1.0)
                time.sleep(0.5)
                vehicle.mode = VehicleMode("ALT_HOLD")
        
        # Check if hover detected
        elif DROPPED:
            # Keep throttle at max until hover is detected
            set_attitude(thrust=1.0)
            
            if amag <= HOVER_THRESHOLD or vehicle.location.global_relative_frame.alt > 7:
                print("Hover achieved!")

                # Deploy legs
                # Hold position for 2 seconds
                # print("Legs deployed")
                # dklib.set_servo(vehicle, LEG_SERVO, "HIGH")

                # Hold altitude here
                vehicle.mode = VehicleMode("ALT_HOLD")
                time.sleep(5)

                # dklib.set_attitude(duration=2) # TODO: Check if this works
                
                # Set to LAND mode
                vehicle.mode = VehicleMode("LAND")
                break # Break out of the loop when we switch to LAND

        time.sleep(0.05) # TODO: check if this delay is sufficient

    imu.write_to_file(acc_data) # save imu data
    time.sleep(10) # TODO: Check the time here
    print("Mission Complete")
    
    # Close vehicle object
    vehicle.close()

except KeyboardInterrupt:
    # Write the acceleration data to a file
    vehicle.mode = VehicleMode("LAND")
    imu.write_to_file(acc_data)






