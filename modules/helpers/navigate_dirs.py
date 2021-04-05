import os
import errno

def make_dirs(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e

def find_files(directory):
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            yield os.path.join(root, filename)

        for new_dir in dirs:
            yield from find_files(new_dir)

def get_new(file, swap_pairs):
    new_file = file

    for pair in swap_pairs:
        new_file = new_file.replace(pair[0], pair[1], 1)

    return new_file
