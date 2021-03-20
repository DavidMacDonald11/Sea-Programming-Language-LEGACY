import re

comment = re.compile(r"//.*")

def transpile(line):
    line = line.strip()

    if line == "":
        return ""

    if line == "pass":
        return "// pass"

    if comment.match(line) is not None:
        cline = comment.findall(line)[0] + "\n"
        return transpile(comment.sub("", line)) + cline

    return "// UNKNOWN: " + line
