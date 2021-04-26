import sys
from interfaces import files, terminal

def main():
    mode, debug, *file_data = sys.argv[1:]

    if mode == "None":
        terminal.main(debug)
    else:
        files.main(mode, debug, *file_data)

if __name__ == "__main__":
    main()
