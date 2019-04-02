import serial
import pynmea2
import math
from time import sleep
import sys
import /home/pi/ISS-SpaceGrant18-19/GPS/GPS.py

GPS1 = GPS.GPS()

try:
    while True:
        location = GPS1.readLocation()

        print('CURRENT LAT: ' + str(location['lat']))
        print('CURRENT LON: ' + str(location['lon']))
        time.sleep(0.5)

except KeyboardInterrupt
    sys.exit()
