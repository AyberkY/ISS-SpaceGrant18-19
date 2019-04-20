import curses
import time

def cursesTest(stdscr):

    curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_CYAN)
    #second color is background color

    stdscr.addstr(0,0,"Hour: ",curses.A_BOLD)
    stdscr.addstr(1,0,"Min: ")

    while True:
        try:
            stdscr.refresh()
            stdscr.addstr(0,10,"13",)
            stdscr.addstr(1,10,"42")
            time.sleep(0.5)

        except:
            print("there was an error")
            break

wrapper(cursesTest)
