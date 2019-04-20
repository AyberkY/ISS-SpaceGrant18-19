import curses
import time

def cursesTest(stdscr):

    curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_CYAN)
    #second color is background color

    stdscr.addstr(0,0,"Hour: ",curses.A_BOLD)
    stdscr.addstr(1,0,"Minutes: ",curses.A_BOLD)
    stdscr.addstr(2,0,"Seconds: ",curses.A_BOLD)
    stdscr.addstr(3,0,"Millisec: ",curses.A_BOLD)

    stdscr.addstr(5,0,"Latitude: ",curses.A_BOLD)
    stdscr.addstr(6,0,"Longitude: ",curses.A_BOLD)
    stdscr.addstr(7,0,"Altitude: ",curses.A_BOLD)
    stdscr.addstr(8,0,"Satellites: ",curses.A_BOLD)

    stdscr.addstr(10,0,"read_ADC(0): ",curses.A_BOLD)
    stdscr.addstr(11,0,"read_ADC(1): ",curses.A_BOLD)
    stdscr.addstr(12,0,"read_ADC(2): ",curses.A_BOLD)

    stdscr.addstr(0,30,"baro_pressure: ",curses.A_BOLD)
    stdscr.addstr(1,30,"baro_altitude: ",curses.A_BOLD)
    stdscr.addstr(2,30,"Temp (C): ",curses.A_BOLD)

    stdscr.addstr(4,30,"Accel x: ",curses.A_BOLD)
    stdscr.addstr(5,30,"Accel y: ",curses.A_BOLD)
    stdscr.addstr(6,30,"Accel z: ",curses.A_BOLD)
    stdscr.addstr(7,30,"Gyro x: ",curses.A_BOLD)
    stdscr.addstr(8,30,"Gyro y: ",curses.A_BOLD)
    stdscr.addstr(9,30,"Gyro z: ",curses.A_BOLD)

    while True:
        try:
            stdscr.refresh()
            stdscr.addstr(0,15,"13",)
            stdscr.addstr(1,15,"42")
            time.sleep(0.5)

        except:
            print("there was an error")
            break

curses.wrapper(cursesTest)
