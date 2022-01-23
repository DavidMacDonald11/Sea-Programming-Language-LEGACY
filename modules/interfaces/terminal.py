from .streams.holder import StreamHolder
from .streams.terminal import TerminalInStream, TerminalOutStream, TerminalErrorStream
from . import general

def interface(debug):
    print("Sea Programming Language")

    streams = StreamHolder(
        TerminalInStream(),
        TerminalOutStream(),
        TerminalErrorStream(),
        TerminalOutStream()
    )

    try:
        while True:
            buffer = streams.in_stream.buffer = input("sea > ")

            if buffer == "":
                continue

            if buffer == "exit":
                raise Exit()

            if buffer in ("debug", "nodebug"):
                debug = (buffer == "debug")
                continue

            streams.in_stream.buffer += "\n"

            if buffer.rstrip()[-1] == ":":
                buffer = ""

                while buffer != "\n":
                    buffer = input("...   ") + "\n"
                    streams.in_stream.buffer += buffer

            general.interface(streams, debug, "i")
    except (KeyboardInterrupt, EOFError):
        print()
    except Exit:
        pass

class Exit(Exception):
    pass
