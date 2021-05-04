from interfaces import general
from files.files import generate_file_pairs
from streams.holder import StreamHolder
from streams.terminal import TerminalErrorStream, TerminalOutStream
from streams.file import FileInStream, FileOutStream

def main(*args):
    mode, debug, in_dir, out_dir, bin_dir, *filenames = args

    filenames = clean_filenames(filenames)
    dirs = (in_dir, out_dir, bin_dir)

    visit_files(mode, debug, filenames, dirs)

def clean_filenames(filenames):
    return tuple(name[:-1] if name[-1] == "/" else name for name in filenames)

def visit_files(mode, debug, filenames, dirs):
    for file_pair in generate_file_pairs(filenames, dirs, mode):
        streams = get_streams(mode, file_pair)

        print(f"{VOCAB[mode]} {streams.in_stream.name}", end = "")
        print("" if mode == "i" else f" into {streams.out_stream.name}", end = "")
        print(" ...")

        general.main(streams, debug, mode[0].lower())

def get_streams(mode, file_pair):
    return StreamHolder(
        FileInStream(file_pair[0]),
        TerminalOutStream() if mode == "i" else FileOutStream(file_pair[1]),
        TerminalErrorStream(),
        TerminalOutStream()
    )

VOCAB = {
    "c": "Compiling",
    "i": "Interpreting",
    "t": "Transpiling"
}
