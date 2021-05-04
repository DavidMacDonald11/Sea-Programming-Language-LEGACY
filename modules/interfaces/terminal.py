from interfaces import general
from streams.holder import StreamHolder
from streams.terminal import TerminalInStream, TerminalOutStream, TerminalErrorStream

def main(debug):
    print("Sea Programming Language")
    streams = StreamHolder(
        TerminalInStream(),
        TerminalOutStream(),
        TerminalErrorStream(),
        TerminalOutStream()
        )

    try:
        while True:
            buffer = TerminalInStream.buffer = input("sea > ")

            if buffer == "":
                continue

            if buffer == "exit":
                raise ExitError()

            if buffer in ("debug", "nodebug"):
                debug = buffer == "debug"
                continue

            TerminalInStream.buffer += "\n"

            if buffer.rstrip()[-1] == ":":
                buffer = ""

                while buffer != "\n":
                    buffer = input("...   ") + "\n"
                    TerminalInStream.buffer += buffer

            general.main(streams, debug, "i")
    except (KeyboardInterrupt, EOFError):
        print()
    except ExitError:
        pass

class ExitError(Exception):
    pass
