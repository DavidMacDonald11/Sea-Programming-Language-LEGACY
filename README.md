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
- I also plan on making Sea usable on other operating systems besides Unix-based ones.

# Set-up Instructions
First thing's first, download the latest version from this [GitHub page](https://github.com/DavidMacDonald11/Sea-Programming-Language) and place it somewhere reasonable on your system.

It is possible to run Sea from inside of this folder without doing anything else. However, it'll be more convenient to perform the following steps:
1. [Create an alias](https://www.cyberciti.biz/faq/create-permanent-bash-alias-linux-unix/) for the ./sea.bash command as the following (note that this will override any preexisting `sea` command):
* `alias sea='[PATH TO FOLDER]/sea.bash'`
* In my case, `[PATH TO FOLDER]`=`~/Documents/Coding/Python/Sea\ Programming\ Language`.
* Once your terminal reloads, this will be undone. Use the link and your own research to figure out how to make this permenant.
2. [Update your PATH variable](https://opensource.com/article/17/6/set-path-linux) to include the sea folder with the following:
* `export PATH="$PATH:[PATH TO FOLDER]/"`
* It is essential that all white space within `[PATH TO FOLDER]` is escaped with "\\" as seen above.
* It is essential that the path to the folder ends with a "/".
* If you have multiple paths with "Sea" in them you might have issues. Let me know and I can make the search more specified.
* Once your terminal reloads, this will be undone. Use the link and your own research to figure out how to make this permenant.

# Run Instructions
This will provide you with a `sea` command. Run `sea --help` to see the usage information.

If you want to see the generated tokens and AST, add the `--debug` (or `-d`) argument to your command.
* If you're interpreting, it will print out info to the terminal.
* If you're compiling or transpiling, it will create a `.tmp` file in your `BIN` or `OUT` directory respectively.

You determine which of the following modes to use with a `--mode=[MODE]` argument. Note that `-m=` is equivalent to `--mode=`. Only the first character after the `=` is checked and it is case insentive. Thus, `-m=Transpile`, `--mode=cKJFLK`, and `-m=i` are all valid. All of the following general uses are defined:

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

# Docs
Read through the [documentation](./docs/ROOT.md) to learn the Sea syntax.

It is a mixture of Python and C. I personally think indent-based blocks are better than brackets in general. You should be indenting anyway for your code to be readalbe, and at that point the brackets are redundant. There are times when it isn't convenient, but it is what it is.

I am not going to make Sea higher level than C. There will be syntactical sugar, but I don't want to create a performance cost to using Sea. All of the cost should be paid at transpile-time and compile-time, not at run-time. In the future, I plan on making a compiler from the ground up for Sea.

I also plan on making a Sea library for Python-like data stuctures and functions such as `range`, `enumerate`, tuples, lists, etc.

# Legal
I am basing much of this code on [David Callanan's BASIC interpreter written in Python](https://github.com/davidcallanan/py-myopl-code) which is licensed under [MIT](https://github.com/davidcallanan/py-myopl-code/blob/master/LICENSE).

Feel free to write your own program to interact with this code and absolutely feel free to use the Sea language. It is my intention for this language and code to be useful. If you think my current license is too strict, let me know. See [LICENSE](./LICENSE) for details.

Feel free to use my code as a basis for your own compiler, programming language, etc!
