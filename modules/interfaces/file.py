import os
import errno
from .streams.holder import StreamHolder
from .streams.terminal import TerminalOutStream, TerminalErrorStream
from .streams.file import FileInStream, FileOutStream
from . import general

def interface(*args):
    mode, debug, in_dir, out_dir, bin_dir, *filenames = args

    mode = mode[0].lower()
    filenames = tuple(name[:-1] if name[-1] == "/" else name for name in filenames)
    dirs = (in_dir, out_dir, bin_dir)

    for file_pair in generate_file_pairs(filenames, dirs, mode):
        streams = create_streams(mode, file_pair)

        print(f"{VOCAB[mode]} {streams.in_stream.name}", end = "")
        print("" if mode == "i" else f" into {streams.out_stream.name}", end = "")
        print(" ...")

        general.interface(streams, debug, mode)

def generate_file_pairs(filenames, dirs, mode):
    paths = tuple(f"{dirs[0]}/{name}" for name in filenames)

    for filepath in find_files(dirs[0]):
        if not filepath.endswith((".sea", ".hea")):
            continue

        if len(filenames) != 0 and all(filepath[:len(path)] != path for path in paths):
            continue

        yield create_file_pairs(filepath, dirs, mode)

def find_files(directory):
    for root, subdirs, names in os.walk(directory):
        for name in names:
            yield os.path.join(root, name)

        for subdir in subdirs:
            yield from find_files(subdir)

def create_file_pairs(filepath, dirs, mode):
    if mode == "i":
        return filepath, None

    swap_pairs = [
        (dirs[0], dirs[-1]),
        (".hea", ".h"),
        (".sea", ".s")
    ]

    binfile = swap_end(filepath, swap_pairs)
    binfile_dir = binfile[:binfile.rfind("/")]
    make_directory(binfile_dir)

    if mode == "c":
        return filepath, binfile

    swap_pairs[0] = (dirs[0], dirs[1])
    swap_pairs[2] = (".sea", ".c")

    outfile = swap_end(filepath, swap_pairs)
    outfile_dir = binfile_dir.replace(dirs[-1], dirs[1])
    make_directory(outfile_dir)

    return filepath, outfile

def swap_end(filepath, swap_pairs):
    for pair in swap_pairs:
        filepath = filepath.replace(*pair, 1)

    return filepath

def make_directory(name):
    try:
        os.makedirs(name)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e

def create_streams(mode, file_pair):
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
