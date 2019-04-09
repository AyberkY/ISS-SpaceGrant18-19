import curses
import time

def a_curses(stdscr):

    curses.init_pair(1,curses.COLOR_RED,curses.COLOR_GREEN)

    stdscr.addstr(0,0,"Count: ",curses.A_BOLD)

    for i in range(100):
        try:
            stdscr.refresh()
            stdscr.addstr(0,10,str(i))
            time.sleep(0.25)

            if i == 20:
                stdscr.addstr(2,2,"woot woot",curses.A_BLINK,curses.color_pair(1))
        except:
            print("there was an error")
            break

curses.wrapper(a_curses)
