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
    color = 1

    while True:
        gyro = IMU1.readGyro()
        heading = IMU1.curHeading()

        color += 1
        if color == 4:
            color = 1

        stdscr.erase()
        stdscr.addstr(0,0,"GX: " + str(gyro['x']))
        stdscr.addstr(1,0,"GY: " + str(gyro['y']))
        stdscr.addstr(2,0,"GZ: " + str(gyro['z']))
        stdscr.addstr(3,0,"ROLL: " + str(heading['roll']))
        stdscr.addstr(4,0,"PITCH: " + str(heading['pitch']))
        stdscr.addstr(5,0,"YAW: " + str(heading['yaw']))
        stdscr.addstr(3,50,"geoff gay", curses.color_pair(color))
        stdscr.addstr(4,50,"geoff gay", curses.color_pair(color))
        stdscr.addstr(5,50,"geoff gay", curses.color_pair(color))
        stdscr.addstr(6,50,"geoff gay", curses.color_pair(color))
        stdscr.addstr(7,50,"geoff gay", curses.color_pair(color))
        stdscr.addstr(8,50,"geoff gay", curses.color_pair(color))
        stdscr.addstr(9,50,"geoff gay", curses.color_pair(color))
        stdscr.addstr(6,0,'TIME ELAPSED: ' + str(IMU1.timeElapsed(time.time())))
        stdscr.refresh()
        time.sleep(0.1)
#>>>>>>> 596fa30b72b57fc483e3da8d0fff764c917f38d8

def main():
    curses.wrapper(testIMU)

if __name__ == "__main__":
    main()
