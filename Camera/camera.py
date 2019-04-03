from picamera import PiCamera
from time import sleep
import sys

sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/IMU/MPU9250')
import mpu9250

IMU1 = mpu9250.MPU9250()
cam = PiCamera()

def accelMEASURE():                 #defines a function that takes Ayush function and makes it check if the camera should happen
    accel_DICT = IMU1.readAccel()
    x_ACCEL, y_ACCEL, z_ACCEL = accel_DICT['x'], accel_DICT['y'], accel_DICT['z']

    currentACCEL = (x_ACCEL**2 + y_ACCEL**2 + z_ACCEL**2)**0.5
    pastACCEL = ayushFUNCTION(-10)

    avgACCEL = (abs(currentACCEL) + abs(pastACCEL))/2
    pastACCEL = currentACCEL
    return avgACCEL


def cameraRECORD():                      #function that does the camera
    flightSTATUS = 1                     #flight is happening
    accelCHECK = accelMEASURE()

    cam.start_recording('path...')      #starts recording

    while flightSTATUS == 1:            #check if rocket is in flight
        sleep(10)
        if accelCHECK <= 10**-2:
            flightSTATUS -= 1
        else:
            continue

    cam.stop_recording()                #stops recording

cameraRECORD()
