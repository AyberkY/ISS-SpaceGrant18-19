import sys, time, datetime

sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/ADC')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Barometer')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Camera')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/GPS')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/IMU/MPU9250')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Memory')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Telemetry')

import ADS1x15, mpl3115a2, GPS, mpu9250, RFM9X

filename = datetime.datetime.now()
filehandle = open(filename, 'w+')

print("\n~~~~~~~~~~~INITIALIZING SENSORS~~~~~~~~~~~\n")
filheandle.write("\n~~~~~~~~~~~INITIALIZING SENSORS~~~~~~~~~~~\n")

try:
    GPS1 = GPS.GPS()
except:
    print("COULD NOT CONNECT TO GPS")

try:
    ADC1 = ADS1x15.ADS1115()
except:
    print("COULD NOT CONNECT TO ADC")

try:
    BARO1 = mpl3115a2.Barometer()
except:
    print("COULD NOT CONNECT TO BAROMETER")

try:
    IMU1 = mpu9250.mpu9250()
except:
    print("COULD NOT CONNECT TO MPU9250")

try:
    TELEM1 = RFM9X.RFM9X()
except:
    print("COULD NOT CONNECT TO TELEMETRY")

print("\n~~~~~~~~~~~ALL SENSORS INITIALIZED SUCCESSFULLY~~~~~~~~~~~\n")
filheandle.write("\n~~~~~~~~~~~ALL SENSORS INITIALIZED SUCCESSFULLY~~~~~~~~~~~\n")

dataArray = []
