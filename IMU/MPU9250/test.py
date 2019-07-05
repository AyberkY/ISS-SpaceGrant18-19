import mpu9250
import time
import sys

IMU1 = mpu9250.MPU9250()

try:
    IMU1.calGyro()
    time.sleep(2)
    IMU1.timeElapsed(time.time())
    while True:
        accel = IMU1.readAccel()
        print('')
        print("ax = " + str(accel['x']))
        print("ay = " + str(accel['y']))
        print("az = " + str(accel['z']))

        #t = IMU1.timeElapsed(time.time())
        #print('TIME ELAPSED: ' + str(t)
        gyro = IMU1.readGyro()
        heading = IMU1.curHeading()
        magnet = IMU1.readMagnet()

        counter = 0

        if counter % 100 == 0:
            print("MagnetX: " + str(magnet['x']))
            print("MagnetY: " + str(magnet['y']))
            print("MagnetZ: " + str(magnet['z']))
            print('')
            #print " [PRE] gx = " , ( gyro['xPre'] )
            print(" [PST] gx = " , ( gyro['x'] ))
            print('')
            #print " [PRE] gy = " , ( gyro['yPre'] )
            print(" [PST] gy = " , ( gyro['y'] ))
            print('')
            #print " [PRE] gz = " , ( gyro['zPre'] )
            print(" [PST] gz = " , ( gyro['z'] ))

            print('')
            print("ROLL IS: ", (heading['roll']))
            print("PITCH IS: ", (heading['pitch']))
            print("YAW IS: ", (heading['yaw']))
            print('temp: ', IMU1.readTemperature())
            print('compass: ', IMU1.readCompass())
        counter = counter + 1
        time.sleep(0.1)

except KeyboardInterrupt:
    sys.exit()
