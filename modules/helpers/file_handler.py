from modules.visitor.io import new_io
from modules.visitor.io import new_file_input
from modules.visitor.io import new_file_output
from modules.interpreter.io import new_terminal_output
from modules.visitor.main import visit
from .navigate_dirs import get_new, find_files, make_dirs

class Files:
    def __init__(self, file_paths):
        self.files = None
        self.file_paths = file_paths

    def __enter__(self):
        self.files = tuple(file for file in self.generate_files() if file is not None)
        return self.files

    def __exit__(self, e_type, e_value, e_traceback):
        for file in self.files:
            file.close()

    def generate_files(self):
        for i, file_path in enumerate(self.file_paths):
            yield open(file_path, "r" if i == 0 else "w")

def get_dirs(args):
    return tuple(file[:-1] if file[-1] == "/" else file for file in args)

def visit_files(args, visitor, dir_count, debug = False):
    dirs = get_dirs(args[:dir_count])
    paths = args[dir_count:]

    files = list(visit_each_file(visitor, dirs, paths, debug))

    if len(dirs) > 2:
        write_tmp_output(dirs[1], files)

def visit_each_file(visitor, dirs, paths, debug):
    for file_paths in generate_files(dirs, paths):
        if isinstance(file_paths, (tuple, list)):
            file_paths = (*file_paths, f"{file_paths[1]}.tmp")
        else:
            file_paths = (file_paths,)

        with Files(file_paths) as files:
            print(f"{visitor.vocab_base}ing {files[0].name}", end = "")
            print("" if len(files) < 2 else f" into {files[1].name}", end = "")
            print(" ...")

            io = get_io(files)
            success = visit(io, visitor, debug)

            if success and len(dirs) > 1:
                yield file_paths[1].replace(f"{dirs[1]}/", "", 1)

def generate_files(dirs, paths):
    for file in find_files(dirs[0]):
        if file.endswith(".sea") or file.endswith(".hea"):
            if len(paths) != 0 and all(file[:len(path)] != path for path in paths):
                continue

            yield get_file(file, dirs)
            continue

def get_file(file, dirs):
    if len(dirs) <= 1:
        return file

    swap_pairs = [
        (dirs[0], dirs[-1]),
        (".hea", ".h"),
        (".sea", ".c")
    ]

    binfile = get_new(file, swap_pairs)
    binfile_dir = binfile[:binfile.rfind("/")]
    make_dirs(binfile_dir)

    if len(dirs) <= 2:
        return file, binfile

    swap_pairs[0] = (dirs[0], dirs[1])

    outfile = get_new(file, swap_pairs)
    outfile_dir = binfile_dir.replace(dirs[-1], dirs[1])
    make_dirs(outfile_dir)

    return file, outfile

def get_io(files):
    input_stream = new_file_input(files[0])

    if len(files) > 1:
        output_stream = new_file_output(files[1])
        debug_stream = new_file_output(files[2])
    else:
        output_stream = new_terminal_output()
        debug_stream = None

    return new_io(input_stream, output_stream, debug_stream)

def write_tmp_output(output_dir, files):
    with open(f"{output_dir}/files.tmp", "w") as outfile:
        for file in files:
            outfile.write(f"{file}\n")
