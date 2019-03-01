import mpu9250
import time
import sys

IMU1 = mpu9250.MPU9250()

try:

    IMU1.calGyro()
    time.sleep(2)
    while True:
        accel = IMU1.readAccel()
        print('')
        #print ("ax = " , ( accel['x'] ))
        #print " ay = " , ( accel['y'] )
        #print " az = " , ( accel['z'] )

        print('TIME ELAPSED: ' + str(IMU1.timeElapsed(time.time())))
        gyro = IMU1.readGyro()
        heading = IMU1.curHeading()
        print('')
        #print " [PRE] gx = " , ( gyro['xPre'] )
        print " [PST] gx = " , ( gyro['x'] )
        print('')
        #print " [PRE] gy = " , ( gyro['yPre'] )
        print " [PST] gy = " , ( gyro['y'] )
        print('')
        #print " [PRE] gz = " , ( gyro['zPre'] )
        print " [PST] gz = " , ( gyro['z'] )

        print('')
        print "ROLL IS: ", (heading['roll'])
        print "PITCH IS: ", (heading['pitch'])
        print "YAW IS: ", (heading['yaw'])
        time.sleep(0.1)

except KeyboardInterrupt:
    sys.exit()
