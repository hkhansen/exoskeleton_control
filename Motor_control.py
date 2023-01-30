#!/usr/bin/env python
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
from gpiozero import RotaryEncoder
import AS5600_encoder

# Pulses Per Revolution of the encoder
ppr = 101       # Standard gear DC motor
%ppr = 1800      # Worm gear DC motor

# Creating motor kit  object
kit = MotorKit()

# Creating encoder object using GPIO pins 24 and 25
encoder = RotaryEncoder(24, 25, max_steps=0)

AS5600 = AS5600_encoder.AS5600()

# Creating an I2C object using the board SCL and SDA pins
I2C = busio.I2C(board.SCL, board.SDA)

# Creating an ADC object and ADC channels
ADC = ADS.ADS1115(I2C)
ADC_0 = AnalogIn(ADC, ADS.P0)
ADC_1 = AnalogIn(ADC, ADS.P1)

AS5600.get_start_angle()

def set_DC_motor_position(angle):
    if (angle > 100):
        angle = 100
    elif (angle < 0):
        angle = 0
    steps = ppr*angle/360
    if (steps > encoder.steps):
        while(encoder.steps < steps):
            kit.motor4.throttle = 1
    elif (steps < encoder.steps):
        while(encoder.steps > steps):
        kit.motor4.throttle = -1
    kit.motor4.throttle = 0
    
def get_DC_motor_angle():
    angle =  360/ppr*encoder.steps
    return angle

def measure_current():
    """
    ACS_current = (offset - ACS_voltage)/sensitivity.
    The offset is given by half of the ACS supply voltage. Here we measure the current supply voltage using the ADC_1 channel.
    The ACS_voltage is measured with the ADC_0 channel.    Here we measure the current supply voltage using the ADC_1
    The sensitivity comes from the ACS_172 datasheet. As this is the 5A version, the sensitivity is 185mV/A the ADC_1
    """
    current = (ADC_1.voltage/2 - ADC_0.voltage)/0.185
    return current

def move_stepper(angle):
    if (angle > 100):
        angle = 100
    elif (angle < 0):
        angle = 0
    if (angle > AS5600.get_angle()):
        while(AS5600.get_angle() < angle):
            kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
            time.sleep(0.01)
    elif (angle > AS5600.get_angle()):
        while(AS5600.get_angle() > angle):
            kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            time.sleep(0.01)

def get_stepper_angle():
    angle = AS5600.get_angle()
    return angle

def release():
    # Releasing motor and GPIO pins
    kit.motor4.throttle = None
    encoder.close()
    kit.stepper1.release()
"""
# Test section. Used during development
try:
    while(True):
        msg = input("Desired angle: ")
        move_stepper(int(msg))

except KeyboardInterrupt:
    release()
"""