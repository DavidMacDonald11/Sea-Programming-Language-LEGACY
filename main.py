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

def get_new(file, src_dir, bin_dir):
    new_file = file.replace(src_dir, bin_dir, 1)
    new_file = new_file.replace(".hea", ".h")
    new_file = new_file.replace(".sea", ".c")

    return new_file

def make_dirs(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e

def file_was_requested(file, rest):
    if rest == "":
        return True

    for path in rest.split():
        if path == "":
            continue

        if file[:len(path)] == path:
            return True

    return False

def write_tmp_output(bin_dir, files):
    with open(f"{bin_dir}/files.tmp", "w") as outfile:
        for file in files:
            outfile.write(f"{file}\n")

def main():
    src_dir = sys.argv[1]
    bin_dir = sys.argv[2]
    rest = sys.argv[3]

    files = []

    for file in find_files(src_dir):
        if file.endswith(".sea") or file.endswith(".hea"):
            new_file = get_new(file, src_dir, bin_dir)

            if not file_was_requested(file, rest):
                continue

            file_dir = new_file[:new_file.rfind("/")]

            make_dirs(file_dir)
            make_dirs(f"bin/{file_dir}")

            print(f"Transpiling {file} into {new_file} ...")
            success = transpiler.transpile(file, new_file)

            if success:
                files += [new_file.replace("bin/", "", 1)]

    write_tmp_output(bin_dir, files)

if __name__ == "__main__":
    main()
