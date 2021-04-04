# The Sea Programming Language
The Sea programming language is a variant of the C language, with python-like syntax. The goal is to make C as enjoyable to write as Python. This should allow for faster programming, faster debugging, fewer lines of code, and all the features of C.

Sea - It's C, just written differently.

# Pronunciation
While this play-on-words thing is fun, I don't want to create a "gif" situation. The `.sea` file extension is pronounced like the english word "sea". The `.hea` file extension is pronounced like the english word "he".

I chose the name Sea because it is pronounced identically to C, but written differently. I then chose `.hea` because it is `.sea` with an 'h', it contains the first three letters in "header", and I made it rhyme because it's more fun than "hey", "hey-ah", "he-ah", or any other arbitrary pronuncation. Say what you will about "he", but it isn't arbitrary.

# Functionality
Currently, this project is in its early stages and most of the Sea langauge has not been fully designed. Please keep watch as I develop this over time.

This project contains a few key features:
1. A Sea to C transpiler.
2. A Sea interpreter.
3. A Sea compiler.
4. A Sea terminal interface.
5. Sea language documentation.

# Future Development
- I'm currently writing all of this code in Python. Once I create everything, I want to rewrite it in Sea.
- I plan on creating syntax highling and a linter for Code OSS as well as icons and logos.
- I plan on creating a unified bash command for all functionality as well as a more formal package for the code with aliases, etc.
- I also plan on making Sea useable on other operating systems besides Unix-based ones.

# Transpilation Instructions
Run `./transpile-sea.bash -s IN -c OUT -b BIN FILES` where:
- All of the following arguments are relative to the current working directory unless otherwise stated.

`FILES` are the files or directories you wish to transpile. This is relative to the `IN` directory. Leaving this blank will transpile the entire `IN` directory.
- If you transpile a directory and a subdirectory, the subdirectory will be redundant.

`IN` is the folder containing `.sea` and `.hea` files. Subdirectories will be automatically discovered. Leaving this blank will use the project's `input` folder by default.

`OUT` is the folder you wish to contain `.c` and `.h` files. Subdirectories in `IN` will be matched. Leaving this blank will use the project's `output` folder by default.

`BIN` is the folder you wish to contain `.o` and executable files. Subdirectories in `IN` will be matched. Leaving this blank will use the project's `bin` folder by default.
- If you wish to use the project's `input` folder, delete anything in the `input` folder and place in the files you wish to transpile.
- When you run `./transpile-sea.bash`, the previously transpiled files in `OUT` and `BIN` will be erased.

# Transpilation, Compilation, and Run Instructions
Run `./run-sea.bash -s IN -c OUT -b BIN -a arg FILES`.

This will first run `./transpile-sea.bash -s IN -c OUT -b BIN FILES`.
- When the files are transpiled, the program creates a temporary file called `OUT/files.tmp` which keeps a list of just-transpiled files. Feel free to delete it afterwards.

The command will transpile the files as per usual, and then it will enter the `OUT` directory and it will try to run `./compile-c.bash -b BIN $(cat files.tmp | tr "\n" " ")`.
- The `compile-c.bash` script is provided in the project's `bin` directory. Feel free to write your own of the same name or to copy paste this one. It takes in file paths relative to `OUT` and compiles them to `BIN`. It then uses those object files to create an executable `BIN/program` file.

Lastly, the script will enter the `BIN` directory where it wil run the generated `./program` file. If you want to pass arguments to this program, include them with `-a arg` in the `./run-sea.bash` command.
- For instance, `./run-sea.bash -a 15 -a hello -a 5` will run as `./program 15 hello 5`.

## Components
Notice that each stage is split into separate scripts. This allows you to transpile, compile, and run at different times under different circumstances.
- You can run `./transpile-sea.bash -s IN -c OUT FILES` to just transpile.
- You can run `cd OUT && ./compile-c.bash FILES` to just compile.
- You can run `./compile-sea.bash -s IN -c OUT FILES` to transpile and compile.
- You can run `cd BIN && ./program` to just run the program.
- You can run `./run-sea.bash -s IN -c OUT FILES` to transpile, compile, and run.

# Docs
Read through the [documentation](./docs/ROOT.md) to learn the Sea syntax.

It is a mixture of Python and C. I personally think indent-based blocks are better than brackets in general. You should be indenting anyway for your code to be readalbe, and at that point the brackets are redundant. There are times when it isn't convenient, but it is what it is.

I am not going to make Sea higher level than C. There will be syntactical sugar, but I don't want to create a performance cost to using Sea. All of the cost should be paid at transpile-time and compile-time, not at run-time. In the future, I plan on making a compiler from the ground up for Sea.

I also plan on making a Sea library for Python-like data stuctures and functions such as `range`, `enumerate`, tuples, lists, etc.

# Legal
I am basing much of this code on [David Callanan's BASIC interpreter written in Python](https://github.com/davidcallanan/py-myopl-code) which is licensed under [MIT](https://github.com/davidcallanan/py-myopl-code/blob/master/LICENSE).

Feel free to write your own program to interact with this code and absolutely feel free to use the Sea language. It is my intention for this language and code to be useful. If you think my current license is too strict, let me know. See [LICENSE](./LICENSE) for details.

Feel free to use my code as a basis for your own compiler, programming language, etc!
