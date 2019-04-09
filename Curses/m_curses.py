import time
import sys
import curses

def testGUI(stdscr):
    for i in range(10):
        while True:
            stdscr.erase()
            stdscr.addstr(0,0,str(i))
            stdscr.refresh()

            time.sleep(1)

curses.wrapper(testGUI)
