class Cursor:
    def __init__(self, screen, offset):
        self.screen = screen
        self.offset = offset

        self.i = 0
        self.wrap = 0
        self.scroll = 0

    def clear(self, ):
        self.move(y = 1, x = self.offset)
        self.i = 0
        self.wrap = 0
        self.scroll = 0

    def adjust(self, line):
        self.i = len(line)
        wrap, self.wrap = self.wrap, 0
        self.move(x = self.offset + self.i, y_delta = -wrap)

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

    def move_up(self):
        y, x = self.screen.getyx()
        y -= 1

        if y >= 0:
            self.screen.move(y, x)
            return

        self.screen.move(0, x)
        self.scroll -= 1

    def move_down(self):
        y, x = self.screen.getyx()
        max_y, _ = self.screen.getmaxyx()
        y += 1

        if y < max_y:
            self.screen.move(y, x)
            return

        self.screen.move(max_y - 1, x)
        self.scroll += 1

    def move_right(self):
        y, x = self.screen.getyx()
        _, max_x = self.screen.getmaxyx()
        x += 1

        if x < max_x:
            self.screen.move(y, x)
            return

        self.screen.move(y, 0)
        self.wrap += 1
        self.move_down()

    def move_left(self):
        y, x = self.screen.getyx()
        _, max_x = self.screen.getmaxyx()
        x -= 1

        if x >= 0:
            self.screen.move(y, x)
            return

        self.screen.move(y, max_x - 1)
        self.wrap -= 1
        self.move_up()
