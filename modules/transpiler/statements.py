from modules.statements.abstract.statement import UnkownStatementError
from modules.statements.basic.empty import PassStatement

def transpile(line):
    statement = get_top_level_statement(line)

    if statement is None:
        raise UnkownStatementError()

    if statement == "":
        return ""

    return statement.get_line()

def get_top_level_statement(line):
    line = line.strip()

    if line == "":
        return ""

    if PassStatement.check_match(line):
        return PassStatement(line)

    return None
