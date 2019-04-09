import curses
from curses import wrapper

def a_curses(stdscr):
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    stdscr.addstr(0,0,"Count: ",curses.A_BOLD)

    for i in range(100):
        try:
            stdscr.refresh()
            stdscr.addstr(0,10,str(i))
        except:
            print("there was an error")
            break

wrapper(a_curses)
