import RPi.GPIO as GPIO
import time
import pigpio #importing GPIO library
import os 

ESC=4  #Connect the ESC in this GPIO pin 
pi = pigpio.pi()
pi.set_servo_pulsewidth(ESC, 0) 

max_value = 2000 #change this if your ESC's max value is different or leave it be
min_value = 700  #change this if your ESC's min value is different or leave it be

def arm(): #This is the arming procedure of an ESC 
    pi.set_servo_pulsewidth(ESC, 0)
    time.sleep(1)
    pi.set_servo_pulsewidth(ESC, max_value)
    time.sleep(1)
    pi.set_servo_pulsewidth(ESC, min_value)

arm()