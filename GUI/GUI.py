import curses
import time
import random

def cursesTest(stdscr):

    curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_CYAN)
    #second color is background color

    stdscr.addstr(0,30,"Hour: ",curses.A_BOLD)
    stdscr.addstr(1,30,"Minutes: ",curses.A_BOLD)
    stdscr.addstr(2,30,"Seconds: ",curses.A_BOLD)
    stdscr.addstr(3,30,"Millisec: ",curses.A_BOLD)

    stdscr.addstr(5,30,"Latitude: ",curses.A_BOLD)
    stdscr.addstr(6,30,"Longitude: ",curses.A_BOLD)
    stdscr.addstr(7,30,"Altitude: ",curses.A_BOLD)
    stdscr.addstr(8,30,"Satellites: ",curses.A_BOLD)

    stdscr.addstr(10,30,"read_ADC(0): ",curses.A_BOLD)
    stdscr.addstr(11,30,"read_ADC(1): ",curses.A_BOLD)
    stdscr.addstr(12,30,"read_ADC(2): ",curses.A_BOLD)

    stdscr.addstr(0,60,"baro_pressure: ",curses.A_BOLD)
    stdscr.addstr(1,60,"baro_altitude: ",curses.A_BOLD)
    stdscr.addstr(2,60,"Temp (C): ",curses.A_BOLD)

    stdscr.addstr(4,60,"Accel x: ",curses.A_BOLD)
    stdscr.addstr(5,60,"Accel y: ",curses.A_BOLD)
    stdscr.addstr(6,60,"Accel z: ",curses.A_BOLD)
    stdscr.addstr(7,60,"Gyro x: ",curses.A_BOLD)
    stdscr.addstr(8,60,"Gyro y: ",curses.A_BOLD)
    stdscr.addstr(9,60,"Gyro z: ",curses.A_BOLD)

    while True:
        try:
            stdscr.refresh()
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

        except:
            print("there was an error")
            break

curses.wrapper(cursesTest)
