from .streams.holder import StreamHolder
from .streams.terminal import TerminalInStream, TerminalOutStream, TerminalErrorStream
from . import general
from .cursed.terminal import Terminal

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

            terminal.prompt()
            terminal.refresh()
    except (KeyboardInterrupt, EOFError):
        pass

def check_for_block(terminal, terminal_input, streams):
    terminal.prompt(block = True)
    terminal.refresh()

    for line in terminal_input:
        if not line:
            terminal.write("\n")
            return

        streams.in_stream.buffer += line + "\n"
        terminal.prompt(block = True)
        terminal.refresh()
