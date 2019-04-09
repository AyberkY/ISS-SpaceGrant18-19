# import serial
# import pynmea2
# import math
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
        # distance = GPS1.distanceFromHome()
        print('CURRENT LAT: ' + '{:.5f}'.format((location['lat'])))
        print('CURRENT LON: ' + '{:.5f}'.format((location['lon'])))
        # print('CURRENT DISTANCE:  ' + str(distance))
        print()
        sleep(0.5)

        distance = GPS1.distanceFromHome()

        print(distance)

except KeyboardInterrupt:
    sys.exit()
