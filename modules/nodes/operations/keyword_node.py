from position.position import Position
from interpreting import errors
from ..ast_node import ASTNode

class KeywordOperationNode(ASTNode):
    def __init__(self, keyword_token, value = None, condition = None):
        self.keyword_token = keyword_token
        self.keyword = keyword_token.keyword
        self.value = value
        self.condition = condition

        position_start = keyword_token.position.start
        position_end = keyword_token.position.end
        stream = position_start.stream

        if condition is not None:
            position_end = condition.position.end
        elif value is not None:
            position_end = value.position.end

        super().__init__(Position(stream, position_start, position_end))

    def __repr__(self):
        keyword = f"{self.keyword}"
        value = "" if self.value is None else f" {self.value}"
        condition = "" if self.condition is None else f" if {self.condition}"

        return f"{keyword}{value}{condition}"

    def interpret(self, memory):
        if self.keyword == "pass":
            return "Success: Do Nothing"

        if self.condition is not None:
            condition = self.condition.interpret(memory)

            if not condition:
                return ""

        if self.keyword == "continue":
            raise errors.UndefinedContinueError(self)

        raise errors.UndefinedBreakError(self)

    def transpile(self, memory):
        keyword = "" if self.keyword == "pass" else self.keyword
        value = "" if self.value is None else self.value.transpile(memory)

        indent = "\t" * memory.depth
        broke_variable = f"__sea__Broke_{memory.break_depth}"

        if self.keyword == "break":
            value = f"{value};\n{indent}{broke_variable} = 1;"

        if self.condition is None:
            return f"{keyword} {value}"

        condition = self.condition.transpile(memory)

        return f"if({condition})\n{indent}{{\n{indent}{keyword} {value}\n{indent}}}\n"
