import curses
import time

def a_curses(stdscr):

    stdscr.addstr(0,0,"Count: ",curses.A_BOLD)

    for i in range(100):
        try:
            stdscr.refresh()
            stdscr.addstr(0,10,str(i))
            time.sleep(1)
        except:
            print("there was an error")
            break

curses.wrapper(a_curses)
