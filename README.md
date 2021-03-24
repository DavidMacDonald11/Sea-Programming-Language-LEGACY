# Sea to C Transpiler - Python Based
A Sea to C transpiler written in Python.

The Sea programming language is a variant of the C language, with python-like syntax. The goal is to make C as enjoyable to write as Python. This should allow for faster programming, faster debugging, fewer lines of code, and all the features of C.

Sea - It's C, just written differently.

# Pronunciation
While this play-on-words thing is fun, I don't want to create a "gif" situation. The `.sea` file extension is pronounced like the english word "sea". The `.hea` file extension is pronounced like the english word "he".

I chose the name Sea because it is pronounced identically to C, but written differently. I then chose `.hea` because it is `.sea` with an 'h', it contains the first three letters in "header", and I made it rhyme because it's more fun than "hey", "hey-ah", "he-ah", or any other arbitrary pronuncation. Say what you will about "he", but it isn't arbitrary.

# Transpilation Instructions
Run `./transpile-sea.bash SRC BIN FILES` where:

`FILES` are the files or directories you wish to transpile. This is relative to the current directory, not to the `SRC` directory. Leaving this blank will transpile the entire `SRC` directory.

- If you do a directory and a subdirectory, the subdirectory will be redundant.

`BIN` is the folder you wish to contain `.c` and `.h` files. Subdirectories in `SRC` will be matched. Leaving this blank will use the project's `bin` folder by default.

`SRC` is the folder containing `.sea` and `.hea` files. Subdirectories will be automatically discovered. Leaving this blank will use the project's `src` folder by default.

- If you wish to use the project's `src` folder, delete anything in the `src` folder and place in the files you wish to transpile.

# Transpilation, Compilation, and Run Instructions
Run `./run-sea.bash SRC BIN FILES`.

This will first run `./transpile-sea.bash SRC BIN FILES`.

- When the files are transpiled, the program creates a temporary file called `BIN/files.tmp` which keeps a list of just-transpiled files. Feel free to delete it afterwards.

The command will transpile the files as per usual, and then it will enter the `BIN` directory and it will try to run `compile-c.bash $(cat files.tmp | tr "\n" " ")`.

- The `compile-c.bash` script is provided in the project's `bin` directory. Feel free to write your own of the same name or to copy paste this one. It takes in file paths relative to `BIN` and compiles them to `BIN/bin`. It then uses those object files to create an executable `BIN/bin/program` file.

Lastly, the script will enter the `BIN/bin` directory where it wil run the generated `./program` file. As of right now, if you wish to pass arguments to the program, you'll have to edit this scipt and add them in.

## Components
Notice that each stage is split into separate scripts. This allows you to transpile, compile, and run at different times under different circumstances.

# Docs
Read through the [documentation](./docs/ROOT.md) to learn the Sea syntax.

It is a mixture of Python and C. I personally think indent-based scopes are better than brackets in general. You should be indenting anyway for your code to be readalbe, and at that point the brackets are redundant. There are times when it isn't convenient, but it is what it is.

I am not going to make Sea higher level than C. There will be syntactical sugar, but I don't want to create a performance cost to using Sea. All of the cost should be paid at transpile-time and compile-time, not at run-time. In the future, I plan on making a compiler from the ground up for Sea.

I also plan on making a Sea library for Python-like datastuctures and functions such as `range`.

# Legal
Feel free to write your own program to interact with this code and absolutely feel free to use the Sea language. It is my intention for this language and code to be useful. If you think my current license is too strict, let me know. See [LICENSE](./LICENSE) for details.
