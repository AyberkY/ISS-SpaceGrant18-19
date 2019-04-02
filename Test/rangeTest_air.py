'''
Air side range testing code.
'''

import sys
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/GPS')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Telemetry')
import RFM9X
import GPS
from time import sleep

GPS1 = GPS.GPS()

Telem = RFM9X.RFM9X()

try:
    while True:
        location = GPS1.readLocation()
        lat = location['lat']
        lon = location['lon']

        distance = GPS1.distanceFromHome()


except KeyboardInterrupt:
