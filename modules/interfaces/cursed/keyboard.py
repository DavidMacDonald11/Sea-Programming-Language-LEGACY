class Keyboard:
    def __init__(self, screen, cursor):
        self.screen = screen
        self.cursor = cursor

        self.lines = [""]
        self.line = ""
        self.line_i = ""

        self.enters = 0
        self.replace = False

    def clear(self):
        self.enters = 0

    def switch_line(self, shift):
        self.line_i += shift
        self.line = self.lines[self.line_i]
        self.cursor.adjust(self.line)

    def press(self, key, printed):
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
                self.enter_key(printed)
            case "\x1B":
                self.escape_key()
            case "KEY_RESIZE":
                self.resize()
            case _:
                self.generic_key(key)

    def up_key(self):
        if len(self.lines) == 1 and self.lines[0] == "":
            self.line, self.lines[0] = self.lines[0], self.line
            self.cursor.adjust(self.line)
            return

        if abs(self.line_i) == len(self.lines):
            return

        if self.line_i == -1:
            self.lines[-1] = self.line

        self.switch_line(-1)

    def down_key(self):
        if len(self.lines) == 1 and self.lines[0] != "":
            self.line, self.lines[0] = self.lines[0], self.line
            self.cursor.adjust(self.line)
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
        if self.cursor.i == 0:
            return

        self.cursor.i -= 1
        self.cursor.move_left()

    def right_key(self):
        if self.cursor.i == len(self.line):
            return

        self.cursor.i += 1
        self.cursor.move_right()

    def home_key(self):
        self.cursor.move(x_delta = -self.cursor.i)
        self.cursor.i = 0

    def end_key(self):
        self.cursor.move(x_delta = len(self.line) - self.cursor.i)
        self.cursor.i = len(self.line)

    def insert_key(self):
        self.replace = not self.replace

    def delete_key(self):
        if self.cursor.i == len(self.line):
            return

        self.line = self.line[:self.cursor.i] + self.line[self.cursor.i + 1:]

    def backspace_key(self):
        if self.cursor.i == 0:
            return

        self.cursor.i -= 1
        self.cursor.move_left()
        self.line = self.line[:self.cursor.i] + self.line[self.cursor.i + 1:]

    def enter_key(self, printed):
        self.cursor.wrap = 0
        self.cursor.i = 0
        self.enters += 1
        self.line_i = -1

        printed[-1] += self.line + "\n"
        self.lines[-1] = self.line

        if self.line != "":
            self.lines.append("")
            self.line = ""

    def generic_key(self, key):
        self.cursor.i += len(key)
        self.cursor.move_right()
        i = self.cursor.i

        shift = 0 if self.replace else 1
        self.line = self.line[:i - 1] + key + self.line[i - shift:]

    def escape_key(self):
        raise KeyboardInterrupt

    def resize(self):
        # TODO move cursor on window resize
        pass
