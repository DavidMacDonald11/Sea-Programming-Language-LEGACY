import sys
from modules.files.file_handler import visit_files

def main():
    visitors = {
        "transpile": ("Transpiler", 3),
        "compile": ("Compiler", 2),
        "interpret": ("Interpreter", 1)
    }

    visit_files(sys.argv[3:], *visitors[sys.argv[1].lower()], sys.argv[2] == "True")

if __name__ == "__main__":
    main()
