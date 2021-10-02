from errors.errors import SeaError

def interface(streams, debug, mode):
    try:
        pass
    except SeaError as error:
        streams.error_stream.write(error)
    finally:
        print_debug_info(debug, streams.debug_stream)

def print_debug_info(debug, debug_stream):
    if not debug:
        return

    debug_stream.write("Debug is enabled.")
