from streams.basic import NullStream
from streams.holder import StreamHolder
from streams.terminal import TerminalInStream, TerminalOutStream, TerminalErrorStream

def main(debug):
    print("Sea Programming Language")
    streams = StreamHolder(TerminalInStream(), TerminalOutStream(), TerminalErrorStream())

    try:
        while True:
            buffer = TerminalInStream.buffer = input("sea > ")

            if buffer == "":
                continue

            if buffer == "exit":
                raise EOFError()

            if buffer in ("debug", "nodebug"):
                debug = buffer == "debug"
                continue

            TerminalInStream.buffer += "\n"

            if buffer.rstrip()[-1] == ":":
                buffer = ""

                while buffer != "\n":
                    buffer = input("...   ") + "\n"
                    TerminalInStream.buffer += buffer
    except (KeyboardInterrupt, EOFError):
        print()
