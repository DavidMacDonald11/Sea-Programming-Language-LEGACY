import re
import curses
from .streams.holder import StreamHolder
from .streams.terminal import TerminalInStream, TerminalOutStream, TerminalErrorStream
from . import general

def interface(debug):
    streams = StreamHolder(
        TerminalInStream(),
        TerminalOutStream(),
        TerminalErrorStream(),
        TerminalOutStream()
    )

    curses_input()

@curses.wrapper
def curses_input(screen):
    title = "Sea Programming Language"
    prompt = "\nsea > "

    lines = title + prompt
    in_lines = ["", ""]
    working_in_line = ""
    in_line = ""
    position = 0
    cursor = 0

    screen.addstr(lines)
    screen.refresh()

    while True:
        y, x = screen.getyx()
        char = screen.getkey()

        if char == "KEY_DOWN":
            position -= 1 if position > 0 else 0
            in_line = in_lines[-position] if position > 0 else working_in_line
        elif char == "KEY_LEFT":
            result = 1 if cursor > 0 else 0
            cursor -= result
            screen.move(y, x - result)
        elif char == "KEY_RIGHT":
            result = 1 if cursor < len(in_line) else 0
            cursor += result
            screen.move(y, x + result)
        elif char == "KEY_UP":
            working_in_line = in_line if position == 0 else working_in_line
            position += 1 if position < len(in_lines)  - 1 else 0
            in_line = in_lines[-position]
        elif ord(char) == 127:
            if in_line != "":
                in_line += "\b"
                cursor -= 1
                screen.move(y, x - 1)
        elif char == "\n":
            cursor = 0
            screen.move(y + 1, len(prompt) - 1)
            lines += in_line + prompt
            in_lines.append(in_line)
            position = 0
            working_in_line = ""
            in_line = ""
        else:
            cursor += 1
            screen.move(y, x + 1)
            in_line += char

        in_line = re.sub(".\b", "", in_line)

        y, x = screen.getyx()
        screen.clear()
        screen.addstr(lines + in_line)
        screen.move(y, x)
        screen.refresh()


class Exit(Exception):
    pass
