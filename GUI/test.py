import sys
import curses
import time
import random

sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Telemetry')

import RFM9X

TELEM1 = RFM9X.RFM9X()

while True:
    [data, rssi] = TELEM1.receive()

    print(data)
