'''
Ground side range testing code.
'''

import sys
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/GPS')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Telemetry')
import RFM9X
import time

GPS1 = GPS.GPS()

Telem = RFM9X.RFM9X()

try:
    while True:
        data, rssi = Telem.receive()

        if(data != None):
            print(str(data, 'ascii'))
            print('RSSI: ' + str(data[1]))

        time.sleep(0.1)


except KeyboardInterrupt:
    print('\nending program.')
