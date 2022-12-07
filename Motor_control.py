# Script for only reading the angle of the exoskeleton through the encoder
# Can NOT control the motor
# Works without the Adafruit Raspberry Pi stepper hat

import time
import board
import busio
#import adafruit_ads1x15.ads1115 as ADS
#from adafruit_ads1x15.analog_in import AnalogIn
#from adafruit_motorkit import MotorKit
#from adafruit_motor import stepper
from gpiozero import RotaryEncoder

# Pulses Per Revolution of the encoder
ppr = 101       # Standard gear DC motor
#ppr = 1800      # Worm gear DC motor

# Creating motor kit  object
#kit = MotorKit()

# Creating encoder object using GPIO pins 23 and 24
encoder = RotaryEncoder(23, 24, max_steps=0)

# Creating an I2C object using the board SCL and SDA pins
#I2C = busio.I2C(board.SCL, board.SDA)

# Creating an ADC object and ADC channels
#ADC = ADS.ADS1115(I2C)
#ADC_0 = AnalogIn(ADC, ADS.P0)
#ADC_1 = AnalogIn(ADC, ADS.P1)

def set_DC_motor_position(angle):
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
        The offset is given by half of the ACS supply voltage. Here we measure the current supply voltage using the ADC_1 channe>
        The ACS_voltage is measured with the ADC_0 channel.
        The sensitivity comes from the ACS_172 datasheet. As this is the 5A version, the sensitivity is 185mV/A
        """
        current = (ADC_0.voltage-0.045)/0.185 #abs((ADC_1.voltage/2 - ADC_0.voltage)/0.185)
        return ADC_0.voltage

def move_stepper(angle):
        steps = int(angle/(360/200)) # The Nema14 stepper motor has 200 steps pr revolution = 1.8 degrees pr step
        for i in range(steps):
                kit.stepper1.onestep(style=stepper.DOUBLE)
                time.sleep(0.01)
        kit.stepper1.release()

def release():
        # Releasing motor and GPIO pins
        #kit.motor4.throttle = None
        encoder.close()
        #kit.stepper1.release()
# Test section
"""
try:
        while(True):
                msg = input("Desired angle: ")
                set_DC_motor_position(int(msg))

except KeyboardInterrupt:
        release()
"""
