import curses
from .streams.holder import StreamHolder
from .streams.terminal import TerminalInStream, TerminalOutStream, TerminalErrorStream
from . import general

def interface(screen, debug):
    terminal = NewTerminal(screen)

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

            terminal.prompt(terminal.line_prompt)
            terminal.refresh()
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

class Cursor:
    def __init__(self, screen):
        self.line_wrap = 0

        self.screen = screen
        self.inline = 0
        self.scroll = 0

    def _move(self, y_delta, x_delta, condition, else_values, then = None):
        y, x = self.screen.getyx()
        max_y, max_x = self.screen.getmaxyx()

        y += y_delta
        x += x_delta

        if condition(y, x, max_y, max_x):
            self.screen.move(y, x)
            return

        self.screen.move(*else_values(y, x, max_y, max_x))

        if then is not None:
            then()

    def move_up(self):
        condition = lambda y, x, max_y, max_x: y >= 0
        else_values = lambda y, x, max_y, max_x: (0, x)

        def then():
            self.scroll -= 1

        self._move(-1, 0, condition, else_values, then)

    def move_down(self):
        condition = lambda y, x, max_y, max_x: y < max_y
        else_values = lambda y, x, max_y, max_x: (max_y - 1, x)

        def then():
            self.scroll += 1

        self._move(1, 0, condition, else_values, then)

    def move_right(self):
        condition = lambda y, x, max_y, max_x: x < max_x
        else_values = lambda y, x, max_y, max_x: (y, 0)

        def then():
            self.line_wrap += 1
            self.move_down()

        self._move(0, 1, condition, else_values, then)

    def move_left(self):
        condition = lambda y, x, max_y, max_x: x >= 0
        else_values = lambda y, x, max_y, max_x: (y, max_x - 1)

        def then():
            self.line_wrap -= 1
            self.move_up()

        self._move(0, -1, condition, else_values, then)

    def move(self, y = None, x = None, y_delta = 0, x_delta = 0):
        oy, ox = self.screen.getyx()

        y = oy if y is None else y
        x = ox if x is None else x

        y += y_delta
        x += x_delta

        self.scroll = 0
        self.screen.move(0, 0)

        for _ in range(y):
            self.move_down()

        for _ in range(x):
            self.move_right()

    def adjust(self, len_prompt, line):
        _, max_x = self.screen.getmaxyx()
        self.inline = len(line)

        line_wrap = self.line_wrap
        self.line_wrap = (len_prompt + self.inline) // max_x
        self.move(x = len_prompt + self.inline, y_delta = -line_wrap)

# TODO allow window scrolling
# TODO fix insert issues

class NewTerminal:
    @property
    def history(self):
        return "".join(self.printed) + self.line + str(self.cursor.inline)

    def __init__(self, screen):
        self.title ="Sea Programming Language"
        self.line_prompt = "\nsea > "
        self.block_prompt = "\n...   "

        self.printed = []
        self.lines = [""]
        self.line = ""

        self.line_i = -1
        self.insert_mode = False

        self.screen = screen
        self.cursor = Cursor(screen)
        self.clear()

    def switch_line(self, adjust):
        self.line_i += adjust
        self.line = self.lines[self.line_i]
        self.cursor.adjust(len(self.line_prompt) - 1, self.line)

    def clear(self):
        self.printed = [self.title, self.line_prompt]
        self.cursor.move(y = 1, x = len(self.line_prompt) - 1)
        self.refresh()

    def refresh(self):
        cursor = self.screen.getyx()
        self.screen.clear()
        self.screen.addstr(self.history)
        self.screen.move(*cursor)
        self.screen.refresh()

    def write(self, text = ""):
        lines = text.split("\n")
        self.printed += [line + "\n" for line in lines]

        self.cursor.move(y_delta = len(lines))
        self.refresh()

    def prompt(self, prompt):
        self.cursor.move(x = len(prompt) - 1, y_delta = 1)
        self.printed += [prompt]

    def input(self):
        while True:
            line = self.line
            key = self.screen.getkey()

            self.press_key(key)
            self.refresh()

            if key == "\n":
                yield line

    def press_key(self, key):
        match key:
            case "KEY_RESIZE":
                pass
            case "KEY_UP":
                self.up_key()
            case "KEY_DOWN":
                self.down_key()
            case "KEY_PPAGE":
                self.page_up_key()
            case "KEY_NPAGE":
                self.page_down_key()
            case "KEY_LEFT":
                self.left_key()
            case "KEY_RIGHT":
                self.right_key()
            case "KEY_HOME":
                self.home_key()
            case "KEY_END":
                self.end_key()
            case "KEY_IC":
                self.insert_key()
            case "KEY_DC":
                self.delete_key()
            case ("\x7f"|"KEY_BACKSPACE"):
                self.backspace_key()
            case "\n":
                self.enter_key()
            case _:
                self.generic_key(key)

    def up_key(self):
        if len(self.lines) == 1 and self.lines[0] == "":
            self.line, self.lines[0] = self.lines[0], self.line
            self.cursor.adjust(len(self.line_prompt) - 1, self.line)
            return

        if abs(self.line_i) == len(self.lines):
            return

        if self.line_i == -1:
            self.lines[-1] = self.line

        self.switch_line(-1)

    def down_key(self):
        if len(self.lines) == 1 and self.lines[0] != "":
            self.line, self.lines[0] = self.lines[0], self.line
            self.cursor.adjust(len(self.line_prompt) - 1, self.line)
            return

        if self.line_i == -1:
            return

        self.switch_line(1)

    def page_up_key(self):
        if self.line_i == -1:
            self.lines[-1] = self.line

        self.line_i = -len(self.lines)
        self.switch_line(0)

    def page_down_key(self):
        self.line_i = -1
        self.switch_line(0)

    def left_key(self):
        if self.cursor.inline == 0:
            return

        self.cursor.inline -= 1
        self.cursor.move_left()

    def right_key(self):
        if self.cursor.inline == len(self.line):
            return

        self.cursor.inline += 1
        self.cursor.move_right()

    def home_key(self):
        self.cursor.move(x_delta = -self.cursor.inline)
        self.cursor.inline = 0

    def end_key(self):
        self.cursor.move(x_delta = len(self.line) - self.cursor.inline)
        self.cursor.inline = len(self.line)

    def insert_key(self):
        self.insert_mode = not self.insert_mode

    def delete_key(self):
        if self.cursor.inline == len(self.line):
            return

        self.line = self.line[:self.cursor.inline] + self.line[self.cursor.inline + 1:]

    def backspace_key(self):
        if self.cursor.inline == 0:
            return

        self.cursor.inline -= 1
        self.cursor.move_left()
        self.line = self.line[:self.cursor.inline] + self.line[self.cursor.inline + 1:]

    def enter_key(self):
        self.cursor.inline = 0
        self.line_i = -1

        self.printed += [self.line]
        self.lines[-1] = self.line

        if self.line != "":
            self.lines.append("")
            self.line = ""

    def generic_key(self, key):
        self.cursor.inline += 1
        self.cursor.move_right()

        move = 1 if self.insert_mode and self.cursor.inline != len(self.line) else 0
        self.line = self.line[:self.cursor.inline - 1] + key + self.line[self.cursor.inline - move:]


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
        self.insert_mode = False

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
            case "KEY_IC":
                self.insert()
            case "KEY_HOME":
                self.home()
            case "KEY_END":
                self.end()
            case ("\x7f"|"KEY_BACKSPACE"):
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

    def insert(self):
        self.insert_mode = not self.insert_mode

    def home(self):
        self.slide_cursor(-self.cursor)

    def end(self):
        self.slide_cursor(len(self.line) - self.cursor)

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

        shift = 1 if self.insert_mode and self.cursor != len(self.line) else 0
        self.line = self.line[:self.cursor - 1] + key + self.line[self.cursor - shift:]
