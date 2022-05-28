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

            terminal.prompt(terminal.line_prompt)
            terminal.refresh()
    except (KeyboardInterrupt, EOFError):
        pass

def check_for_block(terminal, terminal_input, streams):
    terminal.prompt(terminal.block_prompt)
    terminal.refresh()

    for line in terminal_input:
        if not line:
            terminal.write("\n")
            return

        streams.in_stream.buffer += line + "\n"
        terminal.prompt(terminal.block_prompt)
        terminal.refresh()

class Cursor:
    def __init__(self, screen):
        self.screen = screen
        self.inline = 0
        self.scroll = 0
        self.line_wrap = 0

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

    def clear(self, prompt_len):
        self.move(y = 1, x = prompt_len)
        self.inline = 0
        self.scroll = 0
        self.line_wrap = 0

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

        y_delta += y - oy
        x_delta += x - ox

        while y_delta > 0:
            self.move_down()
            y_delta -= 1

        while y_delta < 0:
            self.move_up()
            y_delta += 1

        while x_delta > 0:
            self.move_right()
            x_delta -= 1

        while x_delta < 0:
            self.move_left()
            x_delta += 1

    def adjust(self, prompt, line):
        self.inline = len(line)
        line_wrap, self.line_wrap = self.line_wrap, 0
        self.move(x = len(prompt) + self.inline, y_delta = -line_wrap)

# TODO move cursor on window resize

class Terminal:
    @property
    def safe_printed(self):
        max_y, max_x = self.screen.getmaxyx()
        text = "".join(self.printed[-max_y:] + [self.line])

        lines = []
        line = ""

        for c in text:
            line += c

            if c == "\n" or len(line) == max_x:
                lines += [line]
                line = ""

        return (lines + [line])[1 - max_y:]

    def __init__(self, screen):
        self.title = "Sea Programming Language"
        self.line_prompt = "sea > "
        self.block_prompt = "...   "

        self.printed = []
        self.lines = [""]
        self.line = ""

        self.line_i = -1
        self.enter_count = 0
        self.insert_mode = False

        self.screen = screen
        self.cursor = Cursor(screen)
        self.clear()

    def switch_line(self, adjust):
        self.line_i += adjust
        self.line = self.lines[self.line_i]
        self.cursor.adjust(self.line_prompt, self.line)

    def clear(self):
        self.printed = [self.line_prompt]
        self.enter_count = 0
        self.cursor.clear(len(self.line_prompt))
        self.refresh()

    def refresh(self):
        cursor = self.screen.getyx()
        self.screen.clear()

        try:
            self.screen.addstr(self.status_bar(cursor), curses.A_BOLD)
            self.screen.addstr("".join(self.safe_printed))
        except curses.error:
            pass

        self.screen.move(*cursor)
        self.screen.refresh()

    def status_bar(self, cursor):
        _, x = cursor
        _, max_x = self.screen.getmaxyx()

        y = self.enter_count + 1
        x += max_x * self.cursor.line_wrap - len(self.line_prompt) + 1

        status = self.title
        status += "    INS: " + ("Y" if self.insert_mode else "N")
        status += f"    Ln {y}, Col {x}"

        return status[:max_x - 1] + "\n"

    def write(self, text = ""):
        lines = text.split("\n")
        self.printed += [line + "\n" for line in lines]

        self.cursor.move(y_delta = len(lines))
        self.refresh()

    def prompt(self, prompt):
        self.cursor.move(x = len(prompt), y_delta = 1)
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
            case "\x1B":
                self.escape_key()
            case "KEY_RESIZE":
                self.resize()
            case _:
                self.generic_key(key)

    def up_key(self):
        if len(self.lines) == 1 and self.lines[0] == "":
            self.line, self.lines[0] = self.lines[0], self.line
            self.cursor.adjust(self.line_prompt, self.line)
            return

        if abs(self.line_i) == len(self.lines):
            return

        if self.line_i == -1:
            self.lines[-1] = self.line

        self.switch_line(-1)

    def down_key(self):
        if len(self.lines) == 1 and self.lines[0] != "":
            self.line, self.lines[0] = self.lines[0], self.line
            self.cursor.adjust(self.line_prompt, self.line)
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
        self.cursor.line_wrap = 0
        self.cursor.inline = 0
        self.enter_count += 1
        self.line_i = -1

        self.printed[-1] += self.line + "\n"
        self.lines[-1] = self.line

        if self.line != "":
            self.lines.append("")
            self.line = ""

    def generic_key(self, key):
        self.cursor.inline += len(key)
        self.cursor.move_right()
        i = self.cursor.inline

        shift = 0 if self.insert_mode else 1
        self.line = self.line[:i - 1] + key + self.line[i - shift:]

    def escape_key(self):
        raise KeyboardInterrupt

    def resize(self):
        pass
