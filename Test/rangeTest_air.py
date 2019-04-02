'''
Air side range testing code.
'''

import sys
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/GPS')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Telemetry')
import RFM9X
import GPS
import time
import datetime

GPS1 = GPS.GPS()

Telem = RFM9X.RFM9X()

try:
    while True:
        location = GPS1.readLocation()
        lat = str(location['lat'])
        lon = str(location['lon'])
        alt = str(location['alt'])
        sats = str(location['sats'])

        distance = str(GPS1.distanceFromHome())

        data = lat + ',' + lon + ',' + distance + ',' + alt + ',' + sats

        Telem.send(data.encode('utf-8'))

        print("AIR SIDE:    " + data + '\n')

        time.sleep(0.2)

except KeyboardInterrupt:
    print('\nending program')
