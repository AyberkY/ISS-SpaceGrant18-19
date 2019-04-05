'''
Ground side range testing code.
'''

import sys
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/GPS')
sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Telemetry')
import RFM9X
import time
import datetime

Telem = RFM9X.RFM9X()

filename = str(datetime.datetime.now()) + '.txt'
fileHandle = open(filename, 'w+')

try:
    while True:
        data, rssi = Telem.receive()

        if(data != None):
            dataStr = str(data, 'ascii')
            dataStr = dataStr + ',' + str(rssi) + '\n'

            fileHandle.write(dataStr)

            print("GROUND SIDE:    " + dataStr)

        time.sleep(0.1)


except KeyboardInterrupt:
    print('\nending program.')
