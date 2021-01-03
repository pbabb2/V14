#V14 Compass
#rotate device duing calibration
import sys
sys.path.append("")

import time
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

import math

##################################################
# Create                                         #
##################################################

mpu = MPU9250(
    address_ak=AK8963_ADDRESS, 
    address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
    address_mpu_slave=None, 
    bus=1, 
    gfs=GFS_1000, 
    afs=AFS_8G, 
    mfs=AK8963_BIT_16, 
    mode=AK8963_MODE_C100HZ)

##################################################
# Configure                                      #
##################################################
mpu.reset() # Reset sensors
mpu.configure() # Apply the settings to the registers.

##################################################
# Calibrate                                      #
##################################################
mpu.calibrateAK8963() # Calibrate Magnetometer sensor
#mpu.calibrateMPU6500() # Calibrate Gyroscope and Accelerometer
mpu.configure() # The calibration function resets the sensors, so you need to reconfigure them

##################################################
# Get Calibration                                #
##################################################
abias = mpu.abias # Get the master accelerometer biases
gbias = mpu.gbias # Get the master gyroscope biases
magScale = mpu.magScale # Get magnetometer soft iron distortion
mbias = mpu.mbias # Get magnetometer hard iron distortion

#print("|.....MPU9250 in 0x68 Biases.....|")

print("Magnetometer SID", magScale)
print("Magnetometer HID", mbias)
print("\n")

##################################################
# Set Calibration                                #
##################################################
# mpu.magScale = [1.0104166666666667, 0.9797979797979799, 1.0104166666666667]
# mpu.mbias = [2.6989010989010986, 2.7832417582417586, 2.6989010989010986]

##################################################
# Show Values                                    #
##################################################

def mag(B): 
    return math.sqrt(sum(i**2 for i in B))
    
while True:
	
	
	print("|.....MPU9250 in 0x68 Address.....|")
	print("Magnetometer", mpu.readMagnetometerMaster())
	#print("Temperature", mpu.readTemperatureMaster())
	print("\n")
	B=mpu.readMagnetometerMaster()
	print('x component of Magnetic field is', B[0], 'microTesla') #iterate over Magnetometer Data 
	B_magnitude = mag(B)
	print('Magnitude of Magnetic field is', B_magnitude,'microTesla')
    
    #compass heading
    
	if B[0] == 0: #heading is west
		print("avoiding division by zero")
	else:
		theta=math.atan(B[1]/B[0])
		theta=theta*(180/math.pi)
		print('Heading is',theta,'degrees') 
		time.sleep(1)
