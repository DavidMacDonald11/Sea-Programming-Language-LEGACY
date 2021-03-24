import os
import sys
import errno
from modules.transpiler import transpiler

def find_files(directory = "src"):
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            yield os.path.join(root, filename)

        for new_dir in dirs:
            yield from find_files(new_dir)

def make_dirs(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e

def main():
    src_dir = sys.argv[1]
    bin_dir = sys.argv[2]

    for file in find_files(src_dir):
        if file.endswith(".sea") or file.endswith(".hea"):
            new_file = file.replace(src_dir, bin_dir, 1)
            new_file = new_file.replace(".hea", ".h")
            new_file = new_file.replace(".sea", ".c")

            file_dir = new_file[:new_file.rfind("/")]

            make_dirs(file_dir)
            make_dirs(f"bin/{file_dir}")

            print(f"Transpiling {file} into {new_file}...")
            transpiler.transpile(file, new_file)

if __name__ == "__main__":
    main()
