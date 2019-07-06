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
        try:
            [data, rssi] = TELEM1.receive()

            if len(data) != 0:
                dataStr = ""
                for i in range(len(data)):
                    dataStr += data[i]

                data = dataStr[1:-1].split(', ')

                #Fake connectivity data; replace ifs with try/except when real data is available
                GPS_bool = bool(random.getrandbits(1))
                ADC_bool = bool(random.getrandbits(1))
                Baro_bool = bool(random.getrandbits(1))
                IMU_bool = bool(random.getrandbits(1))
                Telem_bool = bool(random.getrandbits(1))
                Cam_bool = bool(random.getrandbits(1))

                stdscr.refresh()
                curses.start_color()

                stdscr.addstr(0,45,str(random.randint(0,100))+"   ")
                stdscr.addstr(1,45,str(random.randint(0,100))+"   ")
                stdscr.addstr(2,45,str(random.randint(0,100))+"   ")
                stdscr.addstr(3,45,str(random.randint(0,100))+"   ")

                stdscr.addstr(5,45,str(data[2])+"   ")
                stdscr.addstr(6,45,str(data[3])+"   ")
                stdscr.addstr(7,45,str(data[4])+"   ")
                stdscr.addstr(8,45,str(data[5])+"   ")

                stdscr.addstr(10,45,str(data[6])+"   ")
                stdscr.addstr(11,45,str(data[7])+"   ")
                stdscr.addstr(12,45,str(data[8])+"   ")

                stdscr.addstr(0,75,str(data[9])+"   ")
                stdscr.addstr(1,75,str(data[10])+"   ")
                stdscr.addstr(2,75,str(data[11])+"   ")

                stdscr.addstr(4,75,str(data[13])+"   ")
                stdscr.addstr(5,75,str(data[14])+"   ")
                stdscr.addstr(6,75,str(data[15])+"   ")
                stdscr.addstr(7,75,str(data[16])+"   ")
                stdscr.addstr(8,75,str(data[17])+"   ")
                stdscr.addstr(9,75,str(data[18])+"   ")

                time.sleep(0.02)

            else:

                stdscr.addstr(5,45,str(0)+"   ")
                stdscr.addstr(6,45,str(0)+"   ")
                stdscr.addstr(7,45,str(0)+"   ")
                stdscr.addstr(8,45,str(0)+"   ")

                stdscr.addstr(10,45,str(0)+"   ")
                stdscr.addstr(11,45,str(0)+"   ")
                stdscr.addstr(12,45,str(0)+"   ")

                stdscr.addstr(0,75,str(0)+"   ")
                stdscr.addstr(1,75,str(0)+"   ")
                stdscr.addstr(2,75,str(0)+"   ")

                stdscr.addstr(4,75,str(0)+"   ")
                stdscr.addstr(5,75,str(0)+"   ")
                stdscr.addstr(6,75,str(0)+"   ")
                stdscr.addstr(7,75,str(0)+"   ")
                stdscr.addstr(8,75,str(0)+"   ")
                stdscr.addstr(9,75,str(0)+"   ")

        except KeyboardInterrupt:
            pass

        except:
            pass

def main():
    curses.wrapper(cursesTest)

if __name__ == "__main__":
    main()
