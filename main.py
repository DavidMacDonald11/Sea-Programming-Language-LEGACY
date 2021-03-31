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

def get_new(file, input_dir, output_dir):
    new_file = file.replace(input_dir, output_dir, 1)
    new_file = new_file.replace(".hea", ".h")
    new_file = new_file.replace(".sea", ".c")

    return new_file

def make_dirs(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e

def write_tmp_output(output_dir, files):
    with open(f"{output_dir}/files.tmp", "w") as outfile:
        for file in files:
            outfile.write(f"{file}\n")

def get_dirs():
    return tuple(file[:-1] if file[-1] == "/" else file for file in sys.argv[1:4])

def main():
    (input_dir, output_dir, bin_dir) = get_dirs()
    paths = sys.argv[4:]

    files = []

    for file in find_files(input_dir):
        if file.endswith(".sea") or file.endswith(".hea"):
            if len(paths) != 0 and all(file[:len(path)] != path for path in paths):
                continue

            new_file = get_new(file, input_dir, output_dir)

            outfile_dir = new_file[:new_file.rfind("/")]
            binfile_dir = outfile_dir.replace(output_dir, bin_dir)

            make_dirs(outfile_dir)
            make_dirs(binfile_dir)

            print(f"Transpiling {file} into {new_file} ...")
            success = transpiler.transpile(file, new_file)

            if success:
                files += [new_file.replace(f"{output_dir}/", "", 1)]

    write_tmp_output(output_dir, files)

if __name__ == "__main__":
    main()
