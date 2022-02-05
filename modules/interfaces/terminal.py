import re
from .streams.holder import StreamHolder
from .streams.terminal import TerminalInStream, TerminalOutStream, TerminalErrorStream
from . import general

def interface(screen, debug):
    streams = StreamHolder(
        TerminalInStream(),
        TerminalOutStream(),
        TerminalErrorStream(),
        TerminalOutStream()
    )

    terminal = Terminal(screen)
    terminal.input()

class Exit(Exception):
    pass

class Terminal:
    def __init__(self, screen):
        self.title = "Sea Programming Language"
        self.prompt = "\nsea > "
        self.printed = self.title + self.prompt
        self.lines = [""]
        self.line = ""
        self.position = -1
        self.cursor = 0

        self.screen = screen
        self.screen.addstr(self.printed)
        self.screen.refresh()

    def input(self):
        while True:
            key = self.get_key()

            cursor = self.screen.getyx()
            self.screen.clear()
            self.screen.addstr(self.printed + self.line)
            self.screen.move(*cursor)
            self.screen.refresh()

    def get_key(self):
        key = self.screen.getkey()

        match key:
            case "KEY_UP":
                self.up()
            case "KEY_DOWN":
                self.down()
            case "KEY_LEFT":
                self.left()
            case "KEY_RIGHT":
                self.right()
            case "KEY_DC":
                self.delete()
            case "\x7f":
                self.backspace()
            case "\n":
                self.enter()
            case _:
                self.character(key)

        return key

    def up(self):
        if abs(self.position) == len(self.lines):
            return

        if self.position == -1:
            self.lines[-1] = self.line

        self.shift_line(-1)

    def down(self):
        if self.position == -1:
            return

        self.shift_line(1)

    def shift_line(self, direction):
        self.position += direction
        self.line = self.lines[self.position]
        self.cursor = len(self.line)

        y, _ = self.screen.getyx()
        self.screen.move(y, len(self.prompt) - 1 + self.cursor)

    def left(self):
        if self.cursor == 0:
            return

        self.slide_cursor(-1)

    def right(self):
        if self.cursor == len(self.line):
            return

        self.slide_cursor(1)

    def slide_cursor(self, amount):
        self.cursor += amount

        y, x = self.screen.getyx()
        self.screen.move(y, x + amount)

    def delete(self):
        if self.cursor == len(self.line):
            return

        self.line = self.line[:self.cursor] + self.line[self.cursor + 1:]

    def backspace(self):
        if self.cursor == 0:
            return

        self.slide_cursor(-1)
        self.line = self.line[:self.cursor] + self.line[self.cursor + 1:]

    def enter(self):
        self.cursor = 0
        self.position = 0

        y, _ = self.screen.getyx()
        self.screen.move(y + 1, len(self.prompt) - 1)

        self.printed += self.line + self.prompt
        self.lines[-1] = self.line

        self.lines.append("")
        self.line = ""

    def character(self, key):
        self.slide_cursor(1)
        self.line = self.line[:self.cursor - 1] + key + self.line[self.cursor - 1:]
