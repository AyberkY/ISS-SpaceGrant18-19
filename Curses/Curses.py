import curses
import time

def a_curses(stdscr):

    curses.init_pair(1,curses.COLOR_RED,curses.COLOR_GREEN)
    #second color is background color

    stdscr.addstr(0,0,"Count: ",curses.A_BOLD)

    for i in range(100):
        try:
            stdscr.refresh()
            stdscr.addstr(0,10,str(i),curses.color_pair(1))
            time.sleep(0.25)

            #if i == 20:
            #    stdscr.addstr(2,2,"woot woot",curses.A_BLINK,curses.color_pair(1))
            #    continue
        except:
            print("there was an error")
            break

    for i in range(100, 200):
        stdscr.refresh()
        item = 100 - i%100
        stdscr.addstr(0,10,str(i),curses.A_BLINK)
        time.sleep(0.25)

curses.wrapper(a_curses)
