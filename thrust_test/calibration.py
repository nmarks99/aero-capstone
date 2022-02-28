
#!/usr/bin/env python3
from hx711 import HX711
import time
import RPi.GPIO as GPIO

try:
    hx711 = HX711(
        dout_pin=5,
        pd_sck_pin=6,
        channel='A',
        gain=64
    )

    hx711.reset()   # reset the HX711 before starting
    
    calibration_factor = 1
    while(True):
        print( calibration_factor * hx711.get_raw_data(num_measures=1)[0] )
        time.sleep(0.05)

finally:
    GPIO.cleanup()  # resets pins to inputs for safety







# https://pypi.org/project/hx711/
# #!/usr/bin/env python3
# from hx711 import HX711
# import RPi.GPIO as GPIO

# try:
#     hx711 = HX711(
#         dout_pin=5,
#         pd_sck_pin=6,
#         channel='A',
#         gain=64
#     )

#     hx711.reset()   # Before we start, reset the HX711 (not obligate)
#     measures = hx711.get_raw_data(num_measures=3)
# finally:
#     GPIO.cleanup()  # always do a GPIO cleanup in your scripts!

# print("\n".join(measures))
