from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math
import signal
import sys


currentLimit = 100 #(amps) max current per motor
encoderCPR = 4000 # counts per revolution of the encoder

# counts are encoder values. 4000 is 1 motor revolution
# configurations for the tragectory control
acceleration = 1000000/100 # (counts/seconds^2) for the trajectory control
deceleration = 1000000/100 # (counts/seconds^2) for the trajectory control
speed = 600000/1


print("finding an odrive...")
my_drive = odrive.find_any() # find ODrive Controller Board


def signal_handler(sig, frame):
	print("CTRL C")
	my_drive.axis0.requested_state = AXIS_STATE_IDLE
	my_drive.axis1.requested_state = AXIS_STATE_IDLE
signal.signal(signal.SIGINT, signal_handler)
signal.pause

#Configure Motors and Encoders
#odrv0.axis0.motor.config.requested_current_range = 120
#odrv0.axis0.motor.config.requested_current_range = 120


my_drive.axis0.motor.config.current_lim = currentLimit # current limit
my_drive.axis1.motor.config.current_lim = currentLimit

my_drive.axis0.encoder.config.cpr = encoderCPR # encoder counts
my_drive.axis1.encoder.config.cpr = encoderCPR

my_drive.axis0.controller.config.vel_limit = speed*1.2 # set speeds
my_drive.axis1.controller.config.vel_limit = speed*1.2

my_drive.axis0.trap_traj.config.vel_limit = speed # set tragector control speeds
my_drive.axis1.trap_traj.config.vel_limit = speed

my_drive.axis0.trap_traj.config.accel_limit = acceleration # acceleration limit
my_drive.axis1.trap_traj.config.accel_limit = acceleration

my_drive.axis0.trap_traj.config.decel_limit = deceleration # deceleration limit
my_drive.axis1.trap_traj.config.decel_limit = deceleration


print("Board Voltage: " + str(my_drive.vbus_voltage) + "V") # Check Voltage

# Calibrate motor and wait for it to finish
print("starting calibration...for both motors")
#my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
#my_drive.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
#while (my_drive.axis0.current_state != AXIS_STATE_IDLE) or (my_drive.axis1.current_state != AXIS_STATE_IDLE) :
#    time.sleep(0.1)

my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
my_drive.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL


my_drive.axis0.controller.move_to_pos(0)
my_drive.axis1.controller.move_to_pos(0)

#print("M0 POS, " + str(my_drive.axis0.encoder.pos_estimate))
#print("M1 POS, " + str(my_drive.axis1.encoder.pos_estimate))




time.sleep(3)

start_time = int(round(time.time()*1000))
milliseconds = int(round(time.time()*1000)) - start_time

print("Time, " + str(milliseconds))

#while True:
for i in range(2):
    my_drive.axis0.controller.move_to_pos(1000)
    my_drive.axis1.controller.move_to_pos(1000)
    #time.sleep(0.5)
    for i in range(150):
        milliseconds = int(round(time.time()*1000)) - start_time
        #print(str(milliseconds) +" , " + str(my_drive.axis0.encoder.pos_estimate*(360/4000)))
        #print("M1 POS, " + str(my_drive.axis1.encoder.pos_estimate))
        time.sleep(0.005)


    my_drive.axis0.controller.move_to_pos(0)
    my_drive.axis1.controller.move_to_pos(0)
    time.sleep(0.5)
    for i in range(150):
        milliseconds = int(round(time.time()*1000)) - start_time
        #print(str(milliseconds) +" , " + str(my_drive.axis0.encoder.pos_estimate*(360/4000)))
        #print("M1 POS, " + str(my_drive.axis1.encoder.pos_estimate))
        time.sleep(0.005)


