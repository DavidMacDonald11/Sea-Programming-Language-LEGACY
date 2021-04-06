from types import SimpleNamespace

def new_io(input_stream, output_stream, debug_stream = None):
    io = SimpleNamespace()

    io.input_stream = input_stream
    io.output_stream = output_stream
    io.debug_stream = debug_stream if debug_stream is not None else output_stream

    return io

def new_input(name, read):
    input_stream = SimpleNamespace()
    input_stream.name = name
    input_stream.read = read

    return input_stream

def new_output(write):
    output_stream = SimpleNamespace()
    output_stream.write = write

    return output_stream

def new_file_input(file):
    return new_input(file.name, lambda: file.read(1))

def new_file_output(file):
    return new_output(file.write)

def new_null_output():
    return new_output(lambda: None)
