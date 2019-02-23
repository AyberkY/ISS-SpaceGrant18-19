import mpu9250
import time
import sys

IMU1 = mpu9250.MPU9250()

try:
    while True:
        accel = IMU1.readAccel()
        print (" ax = " , ( accel['x'] ))
        print " ay = " , ( accel['y'] )
        print " az = " , ( accel['z'] )

        gyro = IMU1.readGyro()
        print " gx = " , ( gyro['x'] )
        print " gy = " , ( gyro['y'] )
        print " gz = " , ( gyro['z'] )

        time.sleep(0.5)

except KeyboardInterrupt:
    sys.exit()
