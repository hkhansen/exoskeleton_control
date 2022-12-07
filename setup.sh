#!/bin/sh
# Author: Hans Kristian Bech Hansen
# Email: hkh@hkhsolutions.dk

# Enabling I2C:
# $ sudo raspi-config
# 3 Interface options
# I5 I2C
# Yes

echo "Updating system..."
sudo apt update
sudo apt upgrade -y
echo "Installing pip..."
sudo apt install python3-venv python3-pip -y
echo "Installing Circuit-Python module..." 
sudo pip3 install adafruit-circuitpython-motorkit
echo "Installing ADS1x15 library..."
sudo pip install ADS1x15-ADC
echo "Installing I2C tools..."
sudo apt-get install -y i2c-tools
sudo apt-get install -y python3-smbus
sudo apt-get install -y python3-dev
echo "\n ### Exoskeleton ready ### \n"
