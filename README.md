# Sea to C Transpiler - Python Based
A Sea to C transpiler written in Python.

The Sea programming language is a variant of the C language, with python-like syntax. The goal is to make C as enjoyable to write as Python. This should allow for faster programming, faster debugging, fewer lines of code, and all the features of C.

Sea - It's C, just written differently.

# Instructions
## In Place
Run `./sea-to-c.bash SRC BIN` where:

`SRC` is the folder containing `.sea` and `.hea` files. Subdirectories will be automatically discovered.

`BIN` is the folder you wish to contain `.c` and `.h` files. Subdirectories in `SRC` will be matched.

## Hybrid
Run `./sea-to-c.bash SRC`

This will behave like the In Place command except `BIN` is automatically chosen as `./bin`

## Nonstationary
Move the files you wish to transpile into `./src`.

Run `./sea-to-c.bash`

The `BIN` directory will be `./bin` by default.

## The "Linux" Method
Write your own program to interact with the files in modules. Good luck!

# Docs
Read through the [documentation](./docs/ROOT) to learn the Sea syntax.
