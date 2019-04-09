import smbus2
import time
import H3LIS331
import sys
# check if you should use smbus or smbus2

bus = smbus2.SMBus(1)

H3  = H3LIS331.H3LIS331()

try:
    while True:
        acc = H3.read_accl()
        print("XM: ", acc['x'])
        print("XU: ", acc['xUM'])
        print("Y: ", acc['y'])
        print("Z: ", acc['z'])
        print("******************")
        time.sleep(1)
except KeyboardInterrupt:
    sys.exit()
