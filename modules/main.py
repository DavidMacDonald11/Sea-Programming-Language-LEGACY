import os
import sys
import curses
from interfaces import terminal, file

def main():
    mode, debug, *file_data = sys.argv[1:]
    debug = (debug == "True")

    if mode == "None":
        os.environ.setdefault("ESCDELAY", "25")
        curses.wrapper(terminal.interface, debug)
    else:
        file.interface(mode, debug, *file_data)

if __name__ == "__main__":
    main()
