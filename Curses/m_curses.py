import curses

stdscr = curses.initscr()
#stdscr is a window object representing the entire screen
print("initscr")

curses.noecho()
#turns off automatic echoing of keys to the screen
print("noecho")

curses.cbreak()
#react to keys instantly (without pressing enter)
print("cbreak")

stdscr.keypad(1)
#makes curses expect cursor keys, navigation keys (Page Up, Home)
print("keypad")

#reverse the above w/ nocbreak, echo, keypad(0)

for i in range(100):
    stdscr.addstr(0,0,"Count: " + str(i))
