from picamera import PiCamera
from time import sleep
import datetime
import sys

sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/IMU/MPU9250')
import mpu9250

IMU1 = mpu9250.MPU9250()
cam = PiCamera()

def accelMEASURE():                 #defines a function that takes Ayush function and makes it check
    accel_DICT = IMU1.readAccel()   #if the camera should happen
    x_ACCEL, y_ACCEL, z_ACCEL = accel_DICT['x'], accel_DICT['y'], accel_DICT['z']

    currentACCEL = (x_ACCEL**2 + y_ACCEL**2 + z_ACCEL**2)**0.5
    return currentACCEL

def accelAVERAGE(initial, final):       #function that takes in initial and final acceleration and computes the average
    return ((abs(initial)+abs(final))/2)


def cameraRECORD():                      #function that does the camera
    flightSTATUS = 1                  #flight is happening
    cam.start_recording(f'/home/pi/ISS-SpaceGrant18-19/Camera/flight.{datetime.datetime.now()}.h264')      #starts recording naming the file flight.{timestamp}

    while flightSTATUS == 1:                #checks if rocket is in flight
        accelCHECKinit = accelMEASURE()     #defines the initial acceleration
        sleep(10)
        accelCHECKfin = accelMEASRURE()     #defines the final acceleration
        accelAVG = accelAVERAGE(accelCHECKinit, accelCHECKfin)
        if accelAVG <= 10**-3:      #ends flight if this is true
            flightSTATUS -= 1
        else:
            continue

    cam.stop_recording()                #stops recording

cameraRECORD()
