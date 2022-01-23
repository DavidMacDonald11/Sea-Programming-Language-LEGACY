import sys
from interfaces import terminal

def main():
    mode, debug, *file_data = sys.argv[1:]
    debug = (debug == "True")

    if mode == "None":
        terminal.interface(debug)
    else:
        pass

if __name__ == "__main__":
    main()