import smbus2
import time
import H3LIS331
# check if you should use smbus or smbus2

bus = smbus2.SMBus(1)

H3LIS331 test = H3LIS331()

try:
    while True:
        acc = test.read_accl()
        print("X: ", acc['x'])
        print("Y: ", acc['y'])
        print("Z: ", acc['z'])
        time.sleep(0.5)
