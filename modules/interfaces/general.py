from errors.errors import SeaError

def interface(streams, debug, mode):
    try:
        data = ""
        symbol = streams.in_stream.read_symbol()

        while symbol != "":
            data += symbol
            symbol = streams.in_stream.read_symbol()

        streams.out_stream.write(data)
    except SeaError as error:
        streams.error_stream.write(error)
    finally:
        print_debug_info(debug, streams.debug_stream)

def print_debug_info(debug, debug_stream):
    if not debug:
        return

    debug_stream.write("\nDebug is enabled.\n")
