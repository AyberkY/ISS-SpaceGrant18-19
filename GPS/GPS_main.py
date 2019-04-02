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
        location = GPS1.readLocation()

        if (location['lat'] == None):
            continue
        else:
            print('CURRENT LAT: ' + location['lat'])
            print('CURRENT LON: ' + location['lon'])
            time.sleep(0.5)

except KeyboardInterrupt:
    sys.exit()
