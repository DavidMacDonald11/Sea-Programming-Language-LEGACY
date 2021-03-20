import re
from ..transpiler import conditionals

string = re.compile(r"\".*\"")
comment = re.compile(r"//.*")
multi_comment = re.compile(r"/\*.*\*/")
return_line = re.compile(r"return.*")
func_call = re.compile(r"\w+\(.*\):{0}")
name_or_literal = re.compile(r"\w+[\w\s]*")

def transpile(line, nested = False):
    line = line.strip()

    if line == "":
        return ""

    if line == "pass":
        return "// pass"

    if match(string, line):
        return line

    if match(comment, line):
        return transpile(remove(comment, line)) + find(comment, line) + "\n"

    if match(multi_comment, line):
        ending = "\n" if not nested else ""
        return transpile(remove(multi_comment, line)) + find(multi_comment, line) + ending

    if match(return_line, line):
        return transpile(remove(return_line, line)) + find(return_line, line) + ";\n"

    if match(func_call, line):
        func = line[:line.find("(")]

        params = line[line.find("(") + 1:line.rfind(")")].split(",")
        params = list(map(lambda x: transpile(x, True), params))
        params = "".join(str(p) + commas(i, len(params) - 1) for i, p in enumerate(params))

        ending = ";\n" if not nested else ""
        return f"{transpile(func)}({params})" + ending

    line = conditionals.transpile(line)

    if match(name_or_literal, line):
        return line

    return "// UNKNOWN: " + line

def match(pattern, line):
    return pattern.match(line) is not None

def find(pattern, line):
    return pattern.findall(line)[0]

def remove(pattern, line):
    return pattern.sub("", line)

def commas(i, upper):
    return ", " if i != upper else ""
