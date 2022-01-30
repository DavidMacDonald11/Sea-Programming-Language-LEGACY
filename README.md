# The Sea Programming Language
The Sea programming language is a variant of the C language, with python-like syntax. The goal is to make C as enjoyable to write as Python. This should allow for faster programming, faster debugging, fewer lines of code, and all the features of C.

Sea - It's C, just written differently.

# Pronunciation
While this play-on-words thing is fun, I don't want to create a "gif" situation. The `.sea` file extension is pronounced like the english word "sea". The `.hea` file extension is pronounced like the english word "he".

I chose the name Sea because it is pronounced identically to C, but written differently. I then chose `.hea` because it is `.sea` with an 'h', it contains the first three letters in "header", and I made it rhyme because it's more fun than "hey", "hey-ah", "he-ah", or any other arbitrary pronuncation. Say what you will about "he", but it isn't arbitrary.

# Functionality
Currently, this project is in its early stages and most of the Sea langauge has not been fully designed. Please keep watch as I develop this over time.

This project will contain a few key features:
1. A Sea to C transpiler.
2. A Sea interpreter.
3. A Sea compiler.
4. A Sea terminal interface.
5. Sea language documentation.

# Future Development
- I am currently writing all of this code in Python. Once I create everything, I want to rewrite it in Sea.
- I plan on creating syntax highlighting and a linter for Code OSS, as well as icons and logos.
- I also plan on making Sea usable on other operating systems besides Unix-based ones.

# Install Instructions
The ideal way to install Sea is to download the [installer](https://github.com/DavidMacDonald11/Sea-Programming-Language/blob/main/installer.bash) and run it.
It will take you through the installation process.

The installer is very young and will likely not work on all systems.
Contact me if you would like me to modify it for specific systems.

Otherwise, you can simply download Sea from [GitHub](https://github.com/DavidMacDonald11/Sea-Programming-Language) and run it from the folder.
If you do this, replace all future `sea` commands with `./sea.bash`.

All the installer does is clone Sea into a folder and modify your `.bashrc` file to use a global `sea` command. This installation method also allows for easy updating.

# Run Instructions
Run `sea --help` to see the usage information.

To access the installer, add the `--install` (or `-i`) argument to your command.

If you want to update sea, add the `--update` (or `-u`) argument to your command.

If you want to see the generated tokens and AST, add the `--debug` (or `-d`) argument.
* If you're interpreting, it will print out info to the terminal.
* If you're compiling or transpiling, it will create a `.tmp` file in your `BIN` or `OUT` directory, respectively.

You determine which of the following modes to use with a `--mode=[MODE]` argument. Note that `-m=` is equivalent to `--mode=`. Only the first character after the `=` is checked and it is case insentive. Thus, `-m=Transpile`, `--mode=cKJFLK`, and `-m=i` are all valid.

## Interpreting Terminal Input
Run `sea` and you'll enter the interpreter's terminal interface. This provides you with the `sea` interpreter to mess around with, similar to running `python`.

The terminal interpreter has special commands:
* `debug` - to enable debugging.
* `nodebug` - to disable debugging.
* `exit` - to exit. (Ctrl+C and Ctrl+D also work)

## Interpreting Files
Run `sea -m=i -s IN FILES` to interpret Sea files

`FILES` are the directories and or files you want to interpet. This is relative to the `IN` directory. Leaving this blank will result in a visit to the entire `IN` directory.
* If you enter a directory and a subdirectory, the subdirectory will be redundant.

`-s IN` is an optional argument to specify the folder containing Sea files. If you do not include this argument, the program will assume there exists a folder in the directory you ran the command from called "input" that contains Sea files.
* The program will only read `.hea` and `.sea` files from this folder

## Compiling Files
Run `sea -m=c -s IN -b BIN FILES` to compile Sea files into assembly.

`FILES` are the directories and or files you want to compile. This is relative to the `IN` directory. Leaving this blank will result in a visit to the entire `IN` directory.
* If you enter a directory and a subdirectory, the subdirectory will be redundant.

`-s IN` is an optional argument to specify the folder containing Sea files. If you do not include this argument, the program will assume there exists a folder in the directory you ran the command from called "input" that contains Sea files.
* The program will only read `.hea` and `.sea` files from this folder

`-b BIN` is an optional argument to specify the folder you wish to contain binary files. If you do not include this argument, the program will use a "bin" folder in the directory you ran the command from.
* If the directory does not exist, the program will create it.
* It will mimick the folder structure in the `IN` folder and create an executable called "program" at the root level of `BIN`.

## Transpiling Files
Run `sea -m=t -s IN -c OUT -b BIN FILES` to transpile Sea files into C.

`FILES` are the directories and or files you want to transpile. This is relative to the `IN` directory. Leaving this blank will result in a visit to the entire `IN` directory.
* If you enter a directory and a subdirectory, the subdirectory will be redundant.

`-s IN` is an optional argument to specify the folder containing Sea files. If you do not include this argument, the program will assume there exists a folder in the directory you ran the command from called "input" that contains Sea files.
* The program will only read `.hea` and `.sea` files from this folder

`-c OUT` is an optional argument to specify the folder you wish to contain C files. If you do not include this argument, the program will use an "output" folder in the directory you ran the command from.
* If the directory does not exist, the program will create it.
* It will mimick the folder structure in the `IN` folder and create a temporary list of C files created at the root level of `OUT` which can be useful for manually compiling the C files.
* There are useful bash scripts in this project's output directory for manual compilation.

`-b BIN` is an optional argument to specify the folder you wish to contain binary files. If you do not include this argument, the program will use a "bin" folder in the directory you ran the command from.
* If the directory does not exist, the program will create it.
* It will mimick the folder structure in the `IN` folder and create an executable called "program" at the root level of `BIN`.

# Docs / Syntax
I will work to add proper language documentation as I continue development.
Check out the [docs folder](./docs).

It is a mixture of Python and C. I personally think indent-based blocks are better than brackets in general. You should be indenting anyway for your code to be readalbe, and at that point the brackets are redundant. There are times when it isn't convenient, but it is what it is.

I am not going to make Sea higher level than C. There will be syntactical sugar, but I don't want to create a performance cost to using Sea. All of the cost should be paid at transpile-time and compile-time, not at run-time. In the future, I plan on making a compiler from the ground up for Sea.

I also plan on making a Sea library for Python-like data stuctures and functions such as `range`, `enumerate`, tuples, lists, etc.

# Legal
I am basing much of this code on [David Callanan's BASIC interpreter written in Python](https://github.com/davidcallanan/py-myopl-code) which is licensed under [MIT](https://github.com/davidcallanan/py-myopl-code/blob/master/LICENSE).

Feel free to write your own program to interact with this code and absolutely feel free to use the Sea language. It is my intention for this language and code to be useful. If you think my current license is too strict, let me know. See [LICENSE](./LICENSE) for details.

Feel free to use my code as a basis for your own compiler, programming language, etc!
