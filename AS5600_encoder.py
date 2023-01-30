import time
from smbus import SMBus

class AS5600:
    # Setting up I2C communication
    #self.i2c_bus = SMBus(1)
    #time.sleep(1)

    def __init__(self):
        self.prev_quadrant = 1
        self.start_angle = 0
        self.i2c_bus = SMBus(1)
        time.sleep(1)
        self.i2c_address = 0x36 # Address of AS5600 device
        magnet_status = 0
        while((magnet_status & 32) != 32):
            print("Checking magnet distance")
            magnet_status = 0
            magnet_status = self.i2c_bus.read_byte_data(self.i2c_address, 0x0B) #Status command to device
            time.sleep(0.5)

    def read_raw_angle(self):
        lowbyte  = self.i2c_bus.read_byte_data(self.i2c_address, 0x0D)
        highbyte = self.i2c_bus.read_byte_data(self.i2c_address, 0x0C)
        # Bitwise operations
        highbyte = highbyte << 8
        raw = highbyte|lowbyte
        return raw*(360/4096)

    def get_start_angle(self):
        self.start_angle = self.read_raw_angle()

    def corrected_angle(self):
        correct_angle = self.read_raw_angle() - self.start_angle
        correct_angle = (-correct_angle)*(25/23) #25/23 is the gear ratio between encoder an motor shaft
        return correct_angle

    def check_quadrant(self):
        """
        Quadrants:
        4 | 1
        -----
        3 | 2
        """
        quadrant = 1
        angle = self.corrected_angle()
        # Check what quadrant we are in
        if(angle >= 0 and angle <= 90):
            quadrant = 1
        if(angle > 90 and angle <= 180):
            quadrant = 2
        if(angle > 180 and angle <= 270):
            quadrant = 3
        if(angle > 270 and angle < 360):
            quadrant = 4

        # Check if we have turned more than one rotation
        turns = 0
        if(quadrant != self.prev_quadrant):
            if(quadrant == 1 and self.prev_quadrant == 4):
                turns = turns + 1
                if(quadrant == 4 and self.prev_quadrant == 1):
                    turns = turns - 1

        # Calculate the total angle from the number of turns
        total_angle = (turns*360) + angle
        return (total_angle, quadrant)   # Returns the total angle and the "new" previous quadrant

    def get_angle(self):
        (angle, self.prev_quadrant) = self.check_quadrant()
        print(angle)
        return angle