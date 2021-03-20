import re

AND = re.compile(" and ")
OR = re.compile(" or ")
NOT = re.compile(" not ")

def transpile(line):
    line = AND.sub(" && ", line)
    line = OR.sub(" || ", line)
    line = NOT.sub(" !", line)

    return line
