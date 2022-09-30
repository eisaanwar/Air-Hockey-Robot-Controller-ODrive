from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math

print("finding an odrive...")
my_drive = odrive.find_any() # find ODrive Controller Board



#Configure Motors and Encoders
#odrv0.axis0.motor.config.requested_current_range = 120
#odrv0.axis0.motor.config.requested_current_range = 120

my_drive.axis0.motor.config.current_lim = 100 # current limit
my_drive.axis1.motor.config.current_lim = 100

my_drive.axis0.encoder.config.cpr = 4000 # encoder counts
my_drive.axis1.encoder.config.cpr = 4000

my_drive.axis0.controller.config.vel_limit = 250000 # set speeds
my_drive.axis1.controller.config.vel_limit = 250000

my_drive.axis0.controller.config.control_mode = CTRL_MODE_VELOCITY_CONTROL
my_drive.axis1.controller.config.control_mode = CTRL_MODE_VELOCITY_CONTROL

my_drive.axis0.controller.config.vel_ramp_rate = 100000 # acceleration
my_drive.axis1.controller.config.vel_ramp_rate = 100000

my_drive.axis0.controller.vel_ramp_enable = True # enable ramped velocity control
my_drive.axis1.controller.vel_ramp_enable = True

print("Board Voltage: " + str(my_drive.vbus_voltage) + "V") # Check Voltage

# Calibrate motor and wait for it to finish
print("starting calibration...for both motors")
my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
my_drive.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while (my_drive.axis0.current_state != AXIS_STATE_IDLE) or (my_drive.axis1.current_state != AXIS_STATE_IDLE) :
    time.sleep(0.1)

my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
my_drive.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL




#while True:
for i in range(4):
    my_drive.axis0.controller.move_to_pos = 0
    my_drive.axis1.controller.move_to_pos = 0
    time.sleep(2)

    my_drive.axis0.controller.move_to_pos = 12000
    my_drive.axis1.controller.move_to_pos = 0
    time.sleep(2)

    my_drive.axis0.controller.move_to_pos = 12000
    my_drive.axis1.controller.move_to_pos = 12000
    time.sleep(2)
