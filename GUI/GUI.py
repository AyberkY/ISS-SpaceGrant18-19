import curses
import time
import random

def cursesTest(stdscr):



    stdscr.addstr(0,0,"GPS: ",curses.A_BOLD)
    stdscr.addstr(1,0,"ADC: ",curses.A_BOLD)
    stdscr.addstr(2,0,"Barometer: ",curses.A_BOLD)
    stdscr.addstr(3,0,"IMU: ",curses.A_BOLD)
    stdscr.addstr(4,0,"Telemetry: ",curses.A_BOLD)
    stdscr.addstr(5,0,"Camera: ",curses.A_BOLD)


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


    stdscr.addstr(0,60,"baro_pressure: ")
    stdscr.addstr(1,60,"baro_altitude: ")
    stdscr.addstr(2,60,"Temp (C): ")

    stdscr.addstr(4,60,"Accel x: ")
    stdscr.addstr(5,60,"Accel y: ")
    stdscr.addstr(6,60,"Accel z: ")
    stdscr.addstr(7,60,"Gyro x: ")
    stdscr.addstr(8,60,"Gyro y: ")
    stdscr.addstr(9,60,"Gyro z: ")

    while True:
        stdscr.refresh()
        stdscr.start_color()

        stdscr.addstr(0,11,"GO",curses.A_BOLD)

        stdscr.addstr(0,45,str(random.randint(0,100))+"   ")
        stdscr.addstr(1,45,str(random.randint(0,100))+"   ")
        stdscr.addstr(2,45,str(random.randint(0,100))+"   ")
        stdscr.addstr(3,45,str(random.randint(0,100))+"   ")

        stdscr.addstr(5,45,str(random.randint(0,100))+"   ")
        stdscr.addstr(6,45,str(random.randint(0,100))+"   ")
        stdscr.addstr(7,45,str(random.randint(0,100))+"   ")
        stdscr.addstr(8,45,str(random.randint(0,100))+"   ")

        stdscr.addstr(10,45,str(random.randint(0,100))+"   ")
        stdscr.addstr(11,45,str(random.randint(0,100))+"   ")
        stdscr.addstr(12,45,str(random.randint(0,100))+"   ")


        stdscr.addstr(0,75,str(random.randint(0,100))+"   ")
        stdscr.addstr(1,75,str(random.randint(0,100))+"   ")
        stdscr.addstr(2,75,str(random.randint(0,100))+"   ")

        stdscr.addstr(4,75,str(random.randint(0,100))+"   ")
        stdscr.addstr(5,75,str(random.randint(0,100))+"   ")
        stdscr.addstr(6,75,str(random.randint(0,100))+"   ")
        stdscr.addstr(7,75,str(random.randint(0,100))+"   ")
        stdscr.addstr(8,75,str(random.randint(0,100))+"   ")
        stdscr.addstr(9,75,str(random.randint(0,100))+"   ")

        time.sleep(0.5)

curses.wrapper(cursesTest)
