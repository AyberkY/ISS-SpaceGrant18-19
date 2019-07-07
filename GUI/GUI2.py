import sys
import curses
import time
import random

sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Telemetry')

import RFM9X

def cursesTest(stdscr):

    TELEM1 = RFM9X.RFM9X()

    curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_MAGENTA,curses.COLOR_BLACK)
    curses.init_pair(4,curses.COLOR_CYAN,curses.COLOR_BLACK)

    #Column 1: connectivity
    stdscr.addstr(0,0,"GPS: ",curses.A_BOLD)
    stdscr.addstr(1,0,"ADC: ",curses.A_BOLD)
    stdscr.addstr(2,0,"Barometer: ",curses.A_BOLD)
    stdscr.addstr(3,0,"IMU: ",curses.A_BOLD)
    stdscr.addstr(4,0,"Telemetry: ",curses.A_BOLD)
    stdscr.addstr(5,0,"Camera: ",curses.A_BOLD)

    #Column 2
    stdscr.addstr(0,30,"Hour: ")
    stdscr.addstr(1,30,"Minutes: ")
    stdscr.addstr(2,30,"Seconds: ")
    stdscr.addstr(3,30,"Millisec: ")

    stdscr.addstr(5,30,"Latitude: ")
    stdscr.addstr(6,30,"Longitude: ")
    stdscr.addstr(7,30,"Altitude: ")
    stdscr.addstr(8,30,"Satellites: ")

    stdscr.addstr(10,30,"read_ADC(0): ")
    stdscr.addstr(11,30,"read_ADC(1): ")
    stdscr.addstr(12,30,"read_ADC(2): ")

    #Column 3
    stdscr.addstr(0,60,"baro_pressure: ")
    stdscr.addstr(1,60,"baro_altitude: ")
    stdscr.addstr(2,60,"Temp (C): ")

    stdscr.addstr(4,60,"Accel x: ")
    stdscr.addstr(5,60,"Accel y: ")
    stdscr.addstr(6,60,"Accel z: ")
    stdscr.addstr(7,60,"Gyro x: ")
    stdscr.addstr(8,60,"Gyro y: ")
    stdscr.addstr(9,60,"Gyro z: ")

    stdscr.addstr(12,60,"MORE SENSORS.",curses.color_pair(4) | curses.A_BOLD)

    while True:

        [data, rssi] = TELEM1.receive()

        if len(data) != 0:

            stdscr.addstr(5,5,str(data[2])+"   ")
            stdscr.addstr(6,5,str(data[3])+"   ")
            stdscr.addstr(7,5,str(data[4])+"   ")
            stdscr.addstr(8,5,str(data[5])+"   ")

        else:

            stdscr.addstr(0,5,str(random.randint(0,100))+"   ")
            stdscr.addstr(1,5,str(random.randint(0,100))+"   ")
            stdscr.addstr(2,5,str(random.randint(0,100))+"   ")
            stdscr.addstr(3,5,str(random.randint(0,100))+"   ")

def main():
    curses.wrapper(cursesTest)

if __name__ == "__main__":
    main()
