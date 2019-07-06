import sys
import curses
import time
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

    stdscr.addstr(2,0,"Latitude: ")
    stdscr.addstr(3,0,"Longitude: ")
    stdscr.addstr(4,0,"Altitude: ")
    stdscr.addstr(5,0,"Satellites: ")

    stdscr.addstr(7,0,"read_ADC(0): ")
    stdscr.addstr(8,0,"read_ADC(1): ")
    stdscr.addstr(9,0,"read_ADC(2): ")

    stdscr.addstr(11,00,"baro_pressure: ")
    stdscr.addstr(12,00,"baro_altitude: ")
    stdscr.addstr(13,00,"Temp (C): ")

    stdscr.addstr(0,40,"Accel x: ")
    stdscr.addstr(1,40,"Accel y: ")
    stdscr.addstr(2,40,"Accel z: ")
    stdscr.addstr(3,40,"Gyro x: ")
    stdscr.addstr(4,40,"Gyro y: ")
    stdscr.addstr(5,40,"Gyro z: ")
    stdscr.addstr(6,50,"(MPU9250)")

    stdscr.addstr(0,80,"Accel x: ")
    stdscr.addstr(1,80,"Accel y: ")
    stdscr.addstr(2,80,"Accel z: ")
    stdscr.addstr(3,90,"(H3LIS331)")

    stdscr.addstr(15,15,"STATE: ",curses.A_BOLD)
    stdscr.addstr(15,80,"MORE SENSORS.",curses.color_pair(4) | curses.A_BOLD)

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

                stdscr.addstr(0,15,str(data[0])+"   ")

                stdscr.addstr(2,15,str(data[2])+"   ")
                stdscr.addstr(3,15,str(data[3])+"   ")
                stdscr.addstr(4,15,str(data[4])+"   ")
                stdscr.addstr(5,15,str(data[5])+"   ")

                stdscr.addstr(7,15,str(data[6])+"   ")
                stdscr.addstr(8,15,str(data[7])+"   ")
                stdscr.addstr(9,15,str(data[8])+"   ")

                stdscr.addstr(11,15,str(data[9])+"   ")
                stdscr.addstr(12,15,str(data[10])+"   ")
                stdscr.addstr(13,15,str(data[11])+"   ")

                stdscr.addstr(0,55,str(data[13])+"   ")
                stdscr.addstr(1,55,str(data[14])+"   ")
                stdscr.addstr(2,55,str(data[15])+"   ")
                stdscr.addstr(3,55,str(data[16])+"   ")
                stdscr.addstr(4,55,str(data[17])+"   ")
                stdscr.addstr(5,55,str(data[18])+"   ")

                if data[1] == "0":
                    stdscr.addstr(15,10,"INITIALIZING",curses.color_pair(2) | curses.A_BOLD)
                elif data[1] == "1"
                    stdscr.addstr(15,10,"PAD / IDLE",curses.color_pair(2) | curses.A_BOLD)
                elif data[1] == "2"
                    stdscr.addstr(15,10,"BOOST",curses.color_pair(2) | curses.A_BOLD)
                elif data[1] == "3"
                    stdscr.addstr(15,10,"COAST",curses.color_pair(2) | curses.A_BOLD)
                elif data[1] == "4"
                    stdscr.addstr(15,10,"APOGEE",curses.color_pair(2) | curses.A_BOLD)
                elif data[1] == "5"
                    stdscr.addstr(15,10,"UNDER DROGUE",curses.color_pair(2) | curses.A_BOLD)
                elif data[1] == "6"
                    stdscr.addstr(15,10,"UNDER MAIN",curses.color_pair(2) | curses.A_BOLD)
                elif data[1] == "7"
                    stdscr.addstr(15,10,"BALLISTIC BALLISTIC BALLISTIC",curses.color_pair(2) | curses.A_BOLD)

                filehandle.write(str(data))

            else:
                pass
                # stdscr.addstr(5,55,str(0)+"   ")
                # stdscr.addstr(6,55,str(0)+"   ")
                # stdscr.addstr(7,55,str(0)+"   ")
                # stdscr.addstr(8,55,str(0)+"   ")
                #
                # stdscr.addstr(10,55,str(0)+"   ")
                # stdscr.addstr(11,55,str(0)+"   ")
                # stdscr.addstr(12,55,str(0)+"   ")
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
            filehandle.close()

        except:
            filehandle.close()

def main():
    curses.wrapper(cursesTest)

if __name__ == "__main__":
    main()
