import re
import curses
from types import SimpleNamespace
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

    terminal = SimpleNamespace(
        title = "Sea Programming Language",
        prompt = "\nsea > ",
        printed = "",
        lines = [""],
        line = "",
        position = -1,
        cursor = 0
    )

    curses.wrapper(handle_input, terminal)

def handle_input(screen, t):
    t.printed = t.title + t.prompt
    screen.addstr(t.printed)
    screen.refresh()

    while True:
        key = screen.getkey()
        KEY_MAP.get(key, character)(screen, t, key)

        cursor = screen.getyx()
        screen.clear()
        screen.addstr(t.printed + t.line)
        screen.move(*cursor)
        screen.refresh()

def up(screen, t, _):
    if abs(t.position) == len(t.lines):
        return

    if t.position == -1:
        t.lines[-1] = t.line

    t.position -= 1
    t.line = t.lines[t.position]

    y, _ = screen.getyx()
    screen.move(y, len(t.prompt) - 1 + len(t.line))

def down(screen, t, _):
    if t.position == -1:
        return

    t.position += 1
    t.line = t.lines[t.position]

    y, _ = screen.getyx()
    screen.move(y, len(t.prompt) - 1 + len(t.line))

def left(screen, t, _):
    if t.cursor == 0:
        return

    slide_cursor(screen, t, -1)

def right(screen, t, _):
    if t.cursor == len(t.line):
        return

    slide_cursor(screen, t, 1)

def backspace(screen, t, _):
    if t.cursor == 0:
        return

    slide_cursor(screen, t, -1)
    t.line = t.line[:t.cursor] + t.line[t.cursor + 1:]

def delete(screen, t, _):
    if t.cursor == len(t.line):
        return

    t.line = t.line[:t.cursor] + t.line[t.cursor + 2:]

def enter(screen, t, _):
    t.cursor = 0
    t.position = 0

    y, _ = screen.getyx()
    screen.move(y + 1, len(t.prompt) - 1)

    t.printed += t.line + t.prompt
    t.lines[-1] = t.line

    t.lines.append("")
    t.line = ""

def character(screen, t, key):
    slide_cursor(screen, t, 1)
    t.line = t.line[:t.cursor - 1] + key + t.line[t.cursor - 1:]

def slide_cursor(screen, t, amount):
    t.cursor += amount

    y, x = screen.getyx()
    screen.move(y, x + amount)

KEY_MAP = {
    "KEY_UP": up,
    "KEY_DOWN": down,
    "KEY_LEFT": left,
    "KEY_RIGHT": right,
    "\x7f": backspace,
    "KEY_DC": delete,
    "\n": enter
}

class Exit(Exception):
    pass


