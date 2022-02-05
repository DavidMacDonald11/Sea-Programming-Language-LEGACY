import curses
from .streams.holder import StreamHolder
from .streams.terminal import TerminalInStream, TerminalOutStream, TerminalErrorStream
from . import general

def interface(screen, debug):
    terminal = Terminal(screen)

    streams = StreamHolder(
        TerminalInStream(),
        TerminalOutStream(terminal.write),
        TerminalErrorStream(terminal.write),
        TerminalOutStream(terminal.write)
    )

    try:
        terminal_input = terminal.input()

        for line in terminal_input:
            match line:
                case "":
                    pass
                case "exit":
                    break
                case "clear":
                    terminal.clear()
                    continue
                case ("debug"|"nodebug"):
                    debug = (line == "debug")
                    terminal.write(f"\nShow Debug: {debug}")
                case "debug?":
                    terminal.write(f"\nShow Debug: {debug}")
                case _:
                    streams.in_stream.buffer = line + "\n"

                    if line.rstrip()[-1] == ":":
                        check_for_block(terminal, terminal_input, streams)

                    general.interface(streams, debug, "i")

            terminal.new_prompt(terminal.prompt)
            terminal.update_screen()
    except (KeyboardInterrupt, EOFError):
        pass

def check_for_block(terminal, terminal_input, streams):
    terminal.new_prompt(terminal.block_prompt)
    terminal.update_screen()

    for line in terminal_input:
        if not line:
            terminal.write("\n")
            return

        streams.in_stream.buffer += line + "\n"
        terminal.new_prompt(terminal.block_prompt)
        terminal.update_screen()

# TODO allow window scrolling
# TODO prevent x coordinate crash

class Terminal:
    def __init__(self, screen):
        self.title = "Sea Programming Language"
        self.prompt = "\nsea > "
        self.block_prompt = "\n...   "
        self.printed = self.title + self.prompt
        self.lines = [""]
        self.line = ""
        self.position = -1
        self.cursor = 0

        self.screen = screen
        self.clear()

    def safe_move_vertical(self, amount = 1):
        y, _ = self.screen.getyx()
        max_y, max_x = self.screen.getmaxyx()

        if y + amount == max_y:
            curses.resize_term(y + amount + 1, max_x)
            self.screen.refresh()

        return y

    def clear(self):
        self.printed = self.title + self.prompt
        self.screen.move(1, len(self.prompt) - 1)
        self.update_screen()

    def write(self, text = ""):
        amount = text.count("\n")

        y = self.safe_move_vertical(amount)
        self.screen.move(y + amount, 0)

        self.printed += text
        self.update_screen()

    def update_screen(self):
        cursor = self.screen.getyx()
        self.screen.clear()
        self.screen.addstr(self.printed + self.line)
        self.screen.move(*cursor)
        self.screen.refresh()

    def new_prompt(self, prompt):
        y = self.safe_move_vertical()
        self.screen.move(y + 1, len(prompt) - 1)
        self.printed += prompt

    def input(self):
        while True:
            line = self.line
            key = self.get_key()
            self.update_screen()

            if key == "\n":
                yield line

    def get_key(self):
        key = self.screen.getkey()

        match key:
            case "KEY_RESIZE":
                pass
            case "KEY_UP":
                self.up()
            case "KEY_DOWN":
                self.down()
            case "KEY_PPAGE":
                self.page_up()
            case "KEY_NPAGE":
                self.page_down()
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
        if len(self.lines) == 1 and self.lines[0] == "":
            self.line, self.lines[0] = self.lines[0], self.line

        if abs(self.position) == len(self.lines):
            return

        if self.position == -1:
            self.lines[-1] = self.line

        self.shift_line(-1)

    def down(self):
        if len(self.lines) == 1 and self.lines[0] != "":
            self.line, self.lines[0] = self.lines[0], self.line

        if self.position == -1:
            return

        self.shift_line(1)

    def page_up(self):
        if self.position == -1:
            self.lines[-1] = self.line

        self.position = -len(self.lines)
        self.shift_line(0)

    def page_down(self):
        self.position = -1
        self.shift_line(0)

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
        self.position = -1

        self.printed += self.line
        self.lines[-1] = self.line

        if self.line != "":
            self.lines.append("")
            self.line = ""

    def character(self, key):
        self.slide_cursor(1)
        self.line = self.line[:self.cursor - 1] + key + self.line[self.cursor - 1:]
