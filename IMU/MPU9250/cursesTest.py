import mpu9250
import time
import sys
import curses


def testIMU(stdscr):

    IMU1 = mpu9250.MPU9250()
    IMU1.calGyro()
    time.sleep(2)

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_PINK, curses.COLOR_WHITE)

    while True:
        gyro = IMU1.readGyro()
        heading = IMU1.curHeading()

        stdscr.erase()
        stdscr.addstr(0,0,"GX: " + str(gyro['x']))
        stdscr.addstr(1,0,"GY: " + str(gyro['y']))
        stdscr.addstr(2,0,"GZ: " + str(gyro['z']))
        stdscr.addstr(3,0,"ROLL: " + str(heading['roll']))
        stdscr.addstr(4,0,"PITCH: " + str(heading['pitch']))
        stdscr.addstr(5,0,"YAW: " + str(heading['yaw']), curses.color_pair(1))
        stdscr.addstr(3,50,"geoff gay")
        stdscr.refresh()
        time.sleep(0.1)

def main():
    curses.wrapper(testIMU)

if __name__ == "__main__":
    main()
