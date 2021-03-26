from .basic.collections import BASIC_STATEMENTS
from .loops.collections import LOOPS

ALL_STATEMENTS = BASIC_STATEMENTS | LOOPS

SORTED_STATEMENTS = sorted(list(ALL_STATEMENTS), key = lambda x: x.complexity)

def check_match_all(line):
    for statement_type in SORTED_STATEMENTS:
        if statement_type.check_match(line):
            return statement_type

    return None
