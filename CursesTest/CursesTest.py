import curses

stdscr = curses.initscr()
#stdscr is a window object representing the entire screen

curses.noecho()
#turns off automatic echoing of keys to the screen

curses.cbreak()
#react to keys instantly (without pressing enter)

stdscr.keypad(1)
#makes curses expect cursor keys, navigation keys (Page Up, Home)

#reverse the above w/ nocbreak, echo, keypad(0)

for i in range(100):
    try:
        stdscr.addstr(0,0,"Count: " + str(i))
    except curses.error:
        pass
