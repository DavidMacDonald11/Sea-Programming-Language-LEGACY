# Sea to C Transpiler - Python Based
A Sea to C transpiler written in Python.

The Sea programming language is a variant of the C language, with python-like syntax. The goal is to make C as enjoyable to write as Python. This should allow for faster programming, faster debugging, fewer lines of code, and all the features of C.

Sea - It's C, just written differently.

# Pronunciation
While this play-on-words thing is fun, I don't want to create a "gif" situation. The `.sea` file extension is pronounced like the english word "sea". The `.hea` file extension is pronounced like the english word "he".

I chose the name Sea because it is pronounced identically to C, but written differently. I then chose `.hea` because it is `.sea` with an 'h', it contains the first three letters in "header", and I made it rhyme because it's more fun than "hey", "hey-ah", "he-ah", or any other arbitrary pronuncation. Say what you will about "he", but it isn't arbitrary.

# Transpilation Instructions
## In Place
Run `./transpile-sea.bash SRC BIN` where:

`SRC` is the folder containing `.sea` and `.hea` files. Subdirectories will be automatically discovered.

`BIN` is the folder you wish to contain `.c` and `.h` files. Subdirectories in `SRC` will be matched.

## Hybrid
Run `./transpile-sea.bash SRC`

This will behave like the In Place command except `BIN` is automatically chosen as `./bin`

## Nonstationary
Delete any pre-existing files in `./src` and move the files you wish to transpile into there.

Run `./transpile-sea.bash`

The `BIN` directory will be `./bin` by default.

## The "Linux" Method
Write your own program to interact with the files in modules. Good luck!

# Compilation and Run Instructions
This only applies if you transpiled in place. Otherwise, you'll unfortunately have to figure this out for yourself.

Run `cd bin` followed by `./compile-c.bash FILES`.

`FILES` are all of the files, newly compiled into `bin`, that need to be included in the program.

Then, run `bin/program` to run the code.

This isn't that much more convenient than just compiling by hand, but I'll probably have a better solution eventually. Until then, you can always compile the transpiled files yourself.

# Docs
Read through the [documentation](./docs/ROOT.md) to learn the Sea syntax.
