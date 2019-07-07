import smbus
import time
import H3LIS331
import sys


# from H3LIS331DL import H3LIS331DL
h3lis331dl = H3LIS331.H3LIS331DL()
h3lis331dl.select_datarate()
h3lis331dl.select_data_config()
time.sleep(0.2)
prev_time = 0

while True:
	accl = h3lis331dl.read_accl()
	print ("Acceleration in X-Axis : %f" %(accl['x']))
	print ("Acceleration in Y-Axis : %f" %(accl['y']))
	print ("Acceleration in Z-Axis : %f" %(accl['z']))
	print (" ************************************ ")
	current_time = time.time()
	print ("Rate: %f" %(1/(current_time - prev_time)))
	prev_time = current_time
