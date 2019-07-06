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

    #Column 2
    stdscr.addstr(0,0,"Timestamp: ")

    stdscr.addstr(2,0,"Latitude: ")
    stdscr.addstr(3,0,"Longitude: ")
    stdscr.addstr(4,0,"Altitude: ")
    stdscr.addstr(5,0,"Satellites: ")

    stdscr.addstr(7,0,"read_ADC(0): ")
    stdscr.addstr(8,0,"read_ADC(1): ")
    stdscr.addstr(9,0,"read_ADC(2): ")

    #Column 3
    stdscr.addstr(0,30,"baro_pressure: ")
    stdscr.addstr(1,30,"baro_altitude: ")
    stdscr.addstr(2,30,"Temp (C): ")

    stdscr.addstr(4,30,"Accel x: ")
    stdscr.addstr(5,30,"Accel y: ")
    stdscr.addstr(6,30,"Accel z: ")
    stdscr.addstr(7,30,"Gyro x: ")
    stdscr.addstr(8,30,"Gyro y: ")
    stdscr.addstr(9,30,"Gyro z: ")

    stdscr.addstr(12,30,"MORE SENSORS.",curses.color_pair(4) | curses.A_BOLD)

    while True:
        try:
            [data, rssi] = TELEM1.receive()

            if len(data) != 0:
                dataStr = ""
                for i in range(len(data)):
                    dataStr += data[i]

                data = dataStr[1:-1].split(', ')

                stdscr.refresh()
                curses.start_color()

                stdscr.addstr(0,15,str(data[0])+"   ")

                stdscr.addstr(2,15,str(data[2])+"   ")
                stdscr.addstr(3,15,str(data[3])+"   ")
                stdscr.addstr(4,15,str(data[4])+"   ")
                stdscr.addstr(5,15,str(data[5])+"   ")

                stdscr.addstr(6,15,str(data[6])+"   ")
                stdscr.addstr(7,15,str(data[7])+"   ")
                stdscr.addstr(8,15,str(data[8])+"   ")

                stdscr.addstr(0,45,str(data[9])+"   ")
                stdscr.addstr(1,45,str(data[10])+"   ")
                stdscr.addstr(2,45,str(data[11])+"   ")

                stdscr.addstr(4,45,str(data[13])+"   ")
                stdscr.addstr(5,45,str(data[14])+"   ")
                stdscr.addstr(6,45,str(data[15])+"   ")
                stdscr.addstr(7,45,str(data[16])+"   ")
                stdscr.addstr(8,45,str(data[17])+"   ")
                stdscr.addstr(9,45,str(data[18])+"   ")

            else:
                pass
                # stdscr.addstr(5,45,str(0)+"   ")
                # stdscr.addstr(6,45,str(0)+"   ")
                # stdscr.addstr(7,45,str(0)+"   ")
                # stdscr.addstr(8,45,str(0)+"   ")
                #
                # stdscr.addstr(10,45,str(0)+"   ")
                # stdscr.addstr(11,45,str(0)+"   ")
                # stdscr.addstr(12,45,str(0)+"   ")
                #
                # stdscr.addstr(0,75,str(0)+"   ")
                # stdscr.addstr(1,75,str(0)+"   ")
                # stdscr.addstr(2,75,str(0)+"   ")
                #
                # stdscr.addstr(4,75,str(0)+"   ")
                # stdscr.addstr(5,75,str(0)+"   ")
                # stdscr.addstr(6,75,str(0)+"   ")
                # stdscr.addstr(7,75,str(0)+"   ")
                # stdscr.addstr(8,75,str(0)+"   ")
                # stdscr.addstr(9,75,str(0)+"   ")

        except KeyboardInterrupt:
            pass

        except:
            pass

def main():
    curses.wrapper(cursesTest)

if __name__ == "__main__":
    main()
