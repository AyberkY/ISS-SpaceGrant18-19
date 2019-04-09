import curses

stdscr = curses.initscr()
#stdscr is a window object representing the entire screen

curses.noecho()
#turns off automatic echoing of keys to the screen

curses.cbreak()
#react to keys instantly (without pressing enter)

stdscr.keypad(True)
#makes curses expect cursor keys, navigation keys (Page Up, Home)

#reverse the above w/ nocbreak, echo, keypad(False)

stdscr.addstr(0,0,"Count: ",curses.A_BOLD)

for i in range(100):
    try:
        stdscr.refresh()
        stdscr.addstr(0,10,str(i))
    except:
        break
