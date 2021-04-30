import os
import errno

def generate_file_pairs(filenames, dirs, mode):
    """Generates all of the files in the in_dir"""
    paths = tuple(f"{dirs[0]}/{name}" for name in filenames)

    for file in find_files(dirs[0]):
        if not file.endswith(".sea") and not file.endswith(".hea"):
            continue

        if len(filenames) != 0 and all(file[:len(path)] != path for path in paths):
            continue

        yield get_file_pairs(file, dirs, mode)

def find_files(directory):
    """Generates all of the files in a directory or subdirectory."""
    for root, dirs, filenames in os.walk(directory):
        for name in filenames:
            yield os.path.join(root, name)

        for new_dir in dirs:
            yield from find_files(new_dir)

def get_file_pairs(file, dirs, mode):
    """Creates pairs of in and out files."""
    if mode == "i":
        return file, None

    swap_pairs = [
        (dirs[0], dirs[-1]),
        (".hea", ".h"),
        (".sea", ".s")
    ]

    binfile = get_new_file(file, swap_pairs)
    binfile_dir = binfile[:binfile.rfind("/")]
    make_dir(binfile_dir)

    if mode == "c":
        return file, binfile

    swap_pairs[0] = (dirs[0], dirs[1])
    swap_pairs[2] = (".sea", ".c")

    outfile = get_new_file(file, swap_pairs)
    outfile_dir = binfile_dir.replace(dirs[-1], dirs[1])
    make_dir(outfile_dir)

    return file, outfile

def get_new_file(file, swap_pairs):
    """Creates a new filename based on pairs to swap."""
    for pair in swap_pairs:
        file = file.replace(pair[0], pair[1], 1)

    return file

def make_dir(directory):
    """Makes a directory if it doesn't exist."""
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e
