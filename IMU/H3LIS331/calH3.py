import smbus
import time
import H3LIS331
import sys


# from H3LIS331DL import H3LIS331DL
h3lis331dl = H3LIS331.H3LIS331DL()
h3lis331dl.select_datarate()
h3lis331dl.select_data_config()
time.sleep(0.2)
xSum = 0
ySum = 0
zSum = 0

for i in range(1000):
	accl = h3lis331dl.read_accl()
	xSum += accl['x']
	ySum += accl['y']
	zSum += accl['z']

print("X Offset: " + str(xSum / 1000))
print("Y Offset: " + str(ySum / 1000))
print("Z Offset: " + str(zSum / 1000))
