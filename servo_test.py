from dronekit import connect, mavutil

print('begin')
vehicle = connect("com5", baud=115200, wait_ready=True)
print('connected')

# print('encoding msg')
# msg = vehicle.message_factory.command_long_encode(
# 0, 0,    # target_system, target_component
# mavutil.mavlink.MAV_CMD_DO_SET_SERVO, #command
# 0, #confirmation
# 12,    # servo number
# 1200,          # servo position between 1000 and 2000
# 0, 0, 0, 0, 0)    # param 3 ~ 7 not used

# # send command to vehicle
# vehicle.send_mavlink(msg)
# print('sent')

def set_servo(vehicle, servo_number, pwm_value):
	pwm_value_int = int(pwm_value)
	msg = vehicle.message_factory.command_long_encode(
		0, 0, 
		mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
		0,
		servo_number,
		pwm_value_int,
		0,0,0,0,0
		)
	vehicle.send_mavlink(msg)

set_servo(vehicle, 9, 1500)
