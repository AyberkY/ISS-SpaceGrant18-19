import sys
import curses
import time
import datetime
import random

sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Telemetry')

import RFM9X

filename = str(datetime.datetime.now()) + ".txt"
filehandle = open(filename, 'w')

def cursesTest(stdscr):

    TELEM1 = RFM9X.RFM9X()

    curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_MAGENTA,curses.COLOR_BLACK)
    curses.init_pair(4,curses.COLOR_CYAN,curses.COLOR_BLACK)

    #Column 2
    stdscr.addstr(0,0,"Timestamp: ")

    stdscr.addstr(2,0,"MAX_ACCEL: ")
    stdscr.addstr(3,0,"BOOST_DUR: ")
    stdscr.addstr(4,0,"MAX_VELO: ")
    stdscr.addstr(5,0,"COAST_DUR: ")
    stdscr.addstr(6,0,"MAX_ALT: ")

    stdscr.addstr(8,0,"DROGUE_DESCENT_VEL: ")
    stdscr.addstr(9,0,"MAIN_DEPLOYMENT_ALT: ")
    stdscr.addstr(10,0,"MAIN_DESCENT_VEL: ")
    stdscr.addstr(11,0,"SUCCESSFULL_CHARGE: ",curses.A_BOLD)

    stdscr.addstr(13,0,"Latitude: ")
    stdscr.addstr(14,0,"Longitude: ")
    stdscr.addstr(15,0,"Altitude: ")

    stdscr.addstr(17,5,"MORE SENSORS.",curses.color_pair(4) | curses.A_BOLD)

    while True:
        try:
            [data, rssi] = TELEM1.receive()

            if len(data) != 0:
                dataStr = ""
                for i in range(len(data)):
                    dataStr += data[i]

                data = dataStr[13:-1].split(', ')

                stdscr.refresh()
                curses.start_color()

                stdscr.addstr(0,15,str(datetime.datetime.now())

                stdscr.addstr(2,15,str(data[0])+"   ")
                stdscr.addstr(3,15,str(data[1])+"   ")
                stdscr.addstr(4,15,str(data[2])+"   ")
                stdscr.addstr(5,15,str(data[3])+"   ")
                stdscr.addstr(6,15,str(data[4])+"   ")

                stdscr.addstr(8,15,str(data[6])+"   ")
                stdscr.addstr(9,15,str(data[7])+"   ")
                stdscr.addstr(10,15,str(data[8])+"   ")

                if data[5] == 1:
                    stdscr.addstr(11,15,"PRIMARY")
                elif data[5] == 2:
                    stdscr.addstr(11,15,"BACKUP")
                else:
                    stdscr.addstr(11,15,"NONE")

                stdscr.addstr(11,15,str(data[9])+"   ")
                stdscr.addstr(12,15,str(data[10])+"   ")
                stdscr.addstr(13,15,str(data[11])+"   ")

                filehandle.write(str(data))

            else:
                pass

        except KeyboardInterrupt:
            filehandle.close()

        except:
            filehandle.close()

def main():
    curses.wrapper(cursesTest)

if __name__ == "__main__":
    main()
