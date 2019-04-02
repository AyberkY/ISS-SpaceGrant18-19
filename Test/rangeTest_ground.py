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
        data = str(Telem.receive(), 'ascii')

        print(data)

        time.sleep(0.1)


except KeyboardInterrupt:
