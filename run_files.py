import os
import sys
import errno
from modules.visitor.io import IO
from modules.visitor.io import FileInput
from modules.visitor.io import FileOutput
from modules.visitor.io import NullOutput
from modules.visitor.main import visit
from modules.transpiler.transpiler import Transpiler
from modules.interpreter.io import TerminalOutput

class Files:
    def __init__(self, *file_paths):
        self.files = None
        self.file_paths = file_paths

    def __enter__(self):
        self.files = tuple(self.generate_files())
        return self.files

    def __exit__(self, e_type, e_value, e_traceback):
        for file in self.files:
            file.close()

    def generate_files(self):
        for i, file_path in enumerate(self.file_paths):
            yield open(file_path, "r" if i == 0 else "w")

def main():
    visitor_type = sys.argv[1].lower()

    if visitor_type == "transpile":
        visit_files((Transpiler, "Transpiling"), 3)
    elif visitor_type == "compile":
        visit_files((None, "Compiling"), 2)
    else:
        visit_files((None, "Interpreting"), 1)

def visit_files(visitor, number_of_dirs):
    dirs = get_dirs(sys.argv[2:2 + number_of_dirs])
    paths = sys.argv[2 + number_of_dirs:]

    files = list(visit_each_file(visitor, dirs, paths))

    if len(dirs) > 1:
        write_tmp_output(dirs[1], files)

def visit_each_file(visitor, dirs, paths):
    for file_paths in generate_files(dirs, paths):
        if file_paths[1] is not None:
            file_paths += (f"{file_paths[1]}.tmp",)

        with Files(*file_paths) as (infile, outfile, errorfile):
            print(f"{visitor[1]} {infile.name}", end = "")
            print("" if outfile is None else f" into {outfile.name}", end = "")
            print(" ...")

            io = get_io(infile, outfile, errorfile)
            success = visit(io, visitor[0])

            if success and len(dirs) > 1:
                yield file_paths[1].replace(f"{dirs[1]}/", "", 1)

def get_dirs(args):
    return tuple(file[:-1] if file[-1] == "/" else file for file in args)

def generate_files(dirs, paths):
    for file in find_files(dirs[0]):
        if file.endswith(".sea") or file.endswith(".hea"):
            if len(paths) != 0 and all(file[:len(path)] != path for path in paths):
                continue

            if len(dirs) > 1:
                binfile = get_new(file, dirs[0], dirs[-1])
                binfile_dir = binfile[:binfile.rfind("/")]
                make_dirs(binfile_dir)

                if len(dirs) > 2:
                    outfile = get_new(file, dirs[0], dirs[1])
                    outfile_dir = binfile_dir.replace(dirs[-1], dirs[1])
                    make_dirs(outfile_dir)

                    yield file, outfile
                    continue

                yield file, binfile
                continue

            yield file, None

def get_io(*files):
    input_stream = FileInput(files[0])

    if files[1] is not None:
        output_stream = FileOutput(files[1])
        error_stream = FileOutput(files[2])
    else:
        output_stream = TerminalOutput("TERMINAL")
        error_stream = NullOutput()

    return IO(input_stream, output_stream, error_stream)

def write_tmp_output(output_dir, files):
    with open(f"{output_dir}/files.tmp", "w") as outfile:
        for file in files:
            outfile.write(f"{file}\n")

def find_files(directory):
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

if __name__ == "__main__":
    main()
