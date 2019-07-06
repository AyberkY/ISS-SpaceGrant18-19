import sys
import curses
import time
import datetime
import random

sys.path.insert(0, '/home/pi/ISS-SpaceGrant18-19/Telemetry')

import RFM9X

filename = str(datetime.datetime.now()) + ".txt"
filehandle = open(filename, 'w')

max_accel = 0
boost_duration = 0
max_velocity = 0
coast_duration = 0
max_altitude = 0

boost_detected = False
coast_detected = False
apogee_detected = False

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

    stdscr.addstr(9,40,"Vertical Speed: ")

    stdscr.addstr(0,80,"Accel x: ")
    stdscr.addstr(1,80,"Accel y: ")
    stdscr.addstr(2,80,"Accel z: ")
    stdscr.addstr(3,90,"(H3LIS331)")

    stdscr.addstr(15,15,"MAX_ACCEL: ")
    stdscr.addstr(15,45,"MAX_VELOCITY: ")
    stdscr.addstr(15,75,"MAX_ALTITUDE: ")

    stdscr.addstr(17,15,"BOOST_DUR: ")
    stdscr.addstr(17,45,"COAST_DUR: ")

    stdscr.addstr(19,15,"STATE: ",curses.A_BOLD)
    stdscr.addstr(19,50,"SUCCESSFULL_CHARGE: ",curses.A_BOLD)
    stdscr.addstr(19,100,"MORE SENSORS.",curses.color_pair(4) | curses.A_BOLD)

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

                stdscr.addstr(9,55,str(data[22])+"   ")

                stdscr.addstr(0,95,str(data[19])+"   ")
                stdscr.addstr(1,95,str(data[20])+"   ")
                stdscr.addstr(2,95,str(data[21])+"   ")

                stdscr.addstr(15,30,str(max_accel)+"   ")
                stdscr.addstr(15,60,str(max_velocity)+"   ")
                stdscr.addstr(15,90,str(max_altitude)+"   ")

                stdscr.addstr(17,30,str(boost_duration)+"   ")
                stdscr.addstr(17,60,str(coast_duration)+"   ")

                if data[1] == "0":
                    stdscr.addstr(19,25,"INITIALIZING   ",curses.color_pair(2) | curses.A_BOLD)
                elif data[1] == "1":
                    stdscr.addstr(19,25,"PAD / IDLE     ",curses.color_pair(2) | curses.A_BOLD)
                elif data[1] == "2":
                    stdscr.addstr(19,25,"BOOST          ",curses.color_pair(2) | curses.A_BOLD)
                elif data[1] == "3":
                    stdscr.addstr(19,25,"COAST          ",curses.color_pair(2) | curses.A_BOLD)
                elif data[1] == "4":
                    stdscr.addstr(19,25,"APOGEE         ",curses.color_pair(2) | curses.A_BOLD)
                elif data[1] == "5":
                    stdscr.addstr(19,25,"UNDER DROGUE   ",curses.color_pair(2) | curses.A_BOLD)
                elif data[1] == "6":
                    stdscr.addstr(19,25,"UNDER MAIN     ",curses.color_pair(2) | curses.A_BOLD)
                elif data[1] == "7":
                    stdscr.addstr(19,25,"BALLISTIC BALLISTIC BALLISTIC",curses.color_pair(2) | curses.A_BOLD)

                if data[23] == 1:
                    stdscr.addstr(19,70,"MAIN",curses.color_pair(1) | curses.A_BOLD)
                elif data[23] == 2:
                    stdscr.addstr(19,70,"BACKUP",curses.color_pair(1) | curses.A_BOLD)
                else:
                    stdscr.addstr(19,70,"NONE",curses.color_pair(2) | curses.A_BOLD)


                if abs(data[13]) > max_accel:
                    max_accel = data[13]
                if abs(data[22]) > max_velocity:
                    max_velocity = data[22]
                if abs(data[10]) > max_altitude:
                    max_altitude = data[10]

                if data[1] == "2":
                    if not boost_detected:
                        boost_detected = True
                        boost_start = time.time()

                if data[1] == "3":
                    if not coast_detected:
                        coast_detected = True
                        boost_end = time.time()
                        boost_duration = boost_end - boost_start

                if data[1] == "4":
                    if not apogee_detected:
                        apogee_detected = True
                        coast_end = time.time()
                        coast_duration = coast_end - boost_end


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
