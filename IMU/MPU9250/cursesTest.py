import mpu9250
import time
import sys
import curses


def testIMU(stdscr):

    IMU1 = mpu9250.MPU9250()
    IMU1.calGyro()
    time.sleep(2)

    while True:
        gyro = IMU1.readGyro()
        stdscr.erase()
        stdscr.addstr(0,2,"GX: " + str(gyro['x']))
        stdscr.addstr(0,1,"GY: " + str(gyro['y']))
        stdscr.addstr(0,0,"GZ: " + str(gyro['z']))


def main():
    curses.wrapper(testIMU)

if __name__ == "__main__":
    main()
