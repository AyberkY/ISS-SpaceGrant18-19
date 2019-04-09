import time
import sys
import curses

def testGUI(stdscr):
    for i in range(100):
        while True:
            stdscr.erase()
            stdscr.addstr(0,10,"more sensors",curses.color_pair(color))
            stdscr.refresh()

            time.sleep(0.1)

curses.wrapper(testGUI)
