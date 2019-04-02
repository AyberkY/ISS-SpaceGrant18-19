import serial
import pynmea2
import math
from time import sleep
import sys
#from /home/pi/ISS-SpaceGrant18-19/GPS/GPS.py import GPS
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/GPS')
import GPS

GPS1 = GPS.GPS()

try:
    while True:
        i = 0
        while i < 10:
            location = GPS1.readLocation()
            i = i + 1

        location = GPS1.readLocation()
        print('CURRENT LAT: ' + str(location['lat']))
        print('CURRENT LON: ' + str(location['lon']))
        time.sleep(0.5)

except KeyboardInterrupt:
    sys.exit()
