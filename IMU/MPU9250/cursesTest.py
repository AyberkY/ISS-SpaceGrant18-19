import mpu9250
import time
import sys
import curses


def testIMU(window):

    IMU1 = mpu9250.MPU9250()
    IMU1.calGyro()
    time.sleep(2)

    while True:
        gyro = IMU1.readGyro()

        window.addstr("GX: " + str(gyro['x']))


def main():
    curses.wrapper(testIMU)

if __name__ == "__main__":
    main()
