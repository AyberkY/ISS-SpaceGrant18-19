import mpu9250
import time
import sys
import curses


def testIMU(stdscr):

    IMU1 = mpu9250.MPU9250()
    IMU1.calGyro()
    time.sleep(2)

    stdscr.addstr(10,10,"geoff gay")

    while True:
        gyro = IMU1.readGyro()
        heading = IMU1.curHeading()

        stdscr.erase()
        stdscr.addstr(0,0,"GX: " + str(gyro['x']))
        stdscr.addstr(1,0,"GY: " + str(gyro['y']))
        stdscr.addstr(2,0,"GZ: " + str(gyro['z']))
        stdscr.addstr(3,0,"ROLL: " + str(heading['roll']))
        stdscr.addstr(4,0,"PITCH: " + str(heading['pitch']))
        stdscr.addstr(5,0,"YAW: " + str(heading['yaw']))
        stdscr.refresh()
        time.sleep(0.1)

def main():
    curses.wrapper(testIMU)

if __name__ == "__main__":
    main()
