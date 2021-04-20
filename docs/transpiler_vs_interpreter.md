# Transpiler vs. Interpreter

Until I implement the compiler, Sea will exist as an interpreted language or as a transpiled language. The transpiler generates C code from Sea while the interpreter runs through the Sea code and performs it. Whichever you use is up to you and your needs.

For now, there may exist differences between the transpiled and interpreted results of Sea. The interpreter currently uses Python's built in functions to determine results while the transpiler uses C's built in functions. If there is a difference that doesn't make sense, let me know and I'll consider fixing it.
