'''
dklib.py 

Internal library of functions that use dronekit but are written by us
and taylored for our specific application.
'''

import dronekit
import os 
import time
import math
from pymavlink import mavutil


def set_servo(vehicle, servo_number, pwm_value):
    '''
    set_servo turns a servo to the desired position, which is a value between 1000 and 2000
    '''    
    assert(isinstance(pwm_value,int) or isinstance(pwm_value,str)),'pwm_value must be an integer between 1000 and 2000 or "low", "mid", and "high"'
    values = {
        "low": 1000,
        "mid": 1500,
        "high": 2000
    } 

    if isinstance(pwm_value,str):
        pwm_value = pwm_value.lower()
        pwm_value = values[pwm_value]
    else:
        pwm_value = int(pwm_value)
    
    msg = vehicle.message_factory.command_long_encode(
		0,
        0,
        dronekit.mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
        0,
		servo_number,
		pwm_value,
		0,0,0,0,0 # rest are zero
		)
        
    vehicle.send_mavlink(msg)

def send_attitude_target(vehicle, roll_angle = 0.0, pitch_angle = 0.0,
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


def set_attitude(vehicle,roll_angle = 0.0, pitch_angle = 0.0,
                yaw_angle = None, yaw_rate = 0.0, use_yaw_rate = False,
                thrust = 0.5, duration = 0):
    """
    Note that from AC3.3 the message should be re-sent more often than every
    second, as an ATTITUDE_TARGET order has a timeout of 1s.
    In AC3.2.1 and earlier the specified attitude persists until it is canceled.
    The code below should work on either version.
    Sending the message multiple times is the recommended way.
    """
    send_attitude_target(vehicle, roll_angle, pitch_angle,
                            yaw_angle, yaw_rate, False,
                            thrust)
    start = time.time()
    while time.time() - start < duration:
        send_attitude_target(vehicle, roll_angle, pitch_angle,
                                yaw_angle, yaw_rate, False,
                                thrust)
        time.sleep(0.1)
    # Reset attitude, or it will persist for 1s more due to the timeout
    send_attitude_target(vehicle, 0, 0,
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



def takeoff(vehicle, target_altitude, default_takeoff_thrust=0.7):

    # Set vehicle mode to GUIDED_NOGPS
    vehicle.mode = dronekit.VehicleMode("GUIDED_NOGPS")
    print("Taking off...")

    # Set to takeoff thrust
    set_attitude(vehicle,thrust=default_takeoff_thrust)
    
    # Wait until we reach the target altitude
    while True:
        current_altitude = vehicle.location.global_relative_frame.alt
        # print("Altitude: {:.3f} m\tDesired: {:.3f} m".format(current_altitude, target_altitude))

        # Break when we get within 95% of the target
        if current_altitude >= target_altitude * 0.95:
            print("Target altitude reached!")
            break
        time.sleep(0.2)



def connect():
    vehicle = dronekit.connect("/dev/serial0",baud=921600,wait_ready=True)
    return vehicle

