from types import SimpleNamespace

WARNING = SimpleNamespace()

def init_global_warning(error_stream, print_warnings = True):
    WARNING.error_stream = error_stream
    WARNING.print_warnings = print_warnings

def raise_warning(warning):
    if not WARNING.print_warnings:
        return

    print_warning(WARNING.error_stream, warning)

def print_warning(error_stream, error):
    to_print = f"{type(error).__name__} at {error.get_position()}: {error.get_message()}"
    error_stream.write(f"{to_print}\n")

    return to_print

def print_error(visitor_type, io, error):
    to_print = print_warning(io.error_stream, error)

    if visitor_type.__name__ == "Transpiler":
        io.output_stream.write("// Transpilation stopped due to error\n")
        io.output_stream.write(f"/* {to_print} */\n")
    elif visitor_type.__name__ == "Interpreter":
        io.output_stream.write(f"{to_print}\n")
