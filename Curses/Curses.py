import curses
import time

def cursesTest(stdscr):

    curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_CYAN)
    #second color is background color

    stdscr.addstr(0,0,"Count: ",curses.A_BOLD)

    for i in range(20):
        try:
            stdscr.refresh()
            stdscr.addstr(0,10,str(i),curses.color_pair(1))
            time.sleep(2)

        except:
            print("there was an error")
            break

    '''for i in range(20):
        stdscr.refresh()
        item = 20 - i
        stdscr.addstr(0,10,str(item),curses.A_BLINK)
        time.sleep(0.2)
    '''

curses.wrapper(cursesTest)
