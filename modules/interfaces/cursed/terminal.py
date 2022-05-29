import curses
from .cursor import Cursor
from .keyboard import Keyboard

class Terminal:
    def __init__(self, screen):
        self.printed = []
        self.debug = False

        self.screen = screen
        self.cursor = Cursor(screen, 6)
        self.keyboard = Keyboard(self.cursor)

        self.clear()

    def clear(self):
        self.printed = ["sea > "]
        self.keyboard.clear()
        self.cursor.clear()
        self.refresh()

    def refresh(self):
        y, x = self.screen.getyx()
        self.screen.clear()

        try:
            self.screen.addstr(self.status_bar(x), curses.A_BOLD)
            self.screen.addstr("".join(self.text()))
        except curses.error:
            pass

        self.screen.move(y, x)
        self.screen.refresh()

    def status_bar(self, x):
        _, max_x = self.screen.getmaxyx()

        y = self.keyboard.enters + 1
        x += max_x * self.cursor.wrap - 5

        status = "Sea Programming Language"
        status += f"    Ln {y}, Col {x}"
        status += "    " + ("REPLACE" if self.keyboard.replace else "INSERT")

        if self.debug:
            status += "    DEBUG"

        key = self.keyboard.last_key
        key = (key[0] if self.debug else key[1])
        key = key.encode("unicode_escape").decode("utf-8")

        status += "    " + key

        return status[:max_x - 1] + "\n"

    def text(self):
        max_y, max_x = self.screen.getmaxyx()
        text = "".join(self.printed[-max_y:] + [self.keyboard.line])

        lines = []
        line = ""

        for c in text:
            line += c

            if c == "\n" or len(line) == max_x:
                lines += [line]
                line = ""

        return (lines + [line])[1 - max_y:]

    def prompt(self, block = False):
        prompt = "sea > " if not block else "...   "
        self.cursor.move(x = len(prompt), y_delta = 1)
        self.printed += [prompt]

    def input(self):
        while True:
            line = self.keyboard.line
            key = self.screen.getkey()

            self.keyboard.press(key, self.printed)
            self.refresh()

            if key == "\n":
                yield line

    def write(self, text = ""):
        lines = text.split("\n")
        self.printed += [line + "\n" for line in lines]

        self.cursor.move(y_delta = len(lines))
        self.refresh()
