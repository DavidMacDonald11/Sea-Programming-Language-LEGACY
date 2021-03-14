# Sea to C Transpiler - Python Based
A Sea to C transpiler written in Python.

The Sea programming language is a variant of the C language, with python-like syntax. The goal is to make C as enjoyable to write as Python. This should allow for faster programming, faster debugging, fewer lines of code, and all the features of C.

Sea - It's C, just written differently.

# Pronunciation
While this play-on-words thing is fun, I don't want to create a "gif" situation. The `.sea` file extension is pronounced like the english word "sea". The `.hea` file extension is pronounced like the english word "he".

I chose the name Sea because it is pronounced identically to C, but written differently. I then chose `.hea` because it is `.sea` with an 'h', it contains the first three letters in "header", and I made it rhyme because it's more fun than "hey", "hey-ah", "he-ah", or any other arbitrary pronuncation. Say what you will about "he", but it isn't arbitrary.

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
Read through the [documentation](./docs/ROOT.md) to learn the Sea syntax.
