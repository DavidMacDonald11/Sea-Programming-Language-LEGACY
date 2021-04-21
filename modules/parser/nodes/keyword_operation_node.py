from modules.lexer.position import Position
from .ast_node import ASTNode
from ...parser import errors

class KeywordOperationNode(ASTNode):
    def __init__(self, keyword_token, value = None, condition = None):
        self.keyword_token = keyword_token
        self.keyword = keyword_token.value
        self.value = value
        self.condition = condition

        position_start = keyword_token.position.start
        position_end = keyword_token.position.end

        if condition is not None:
            position_end = condition.position.end
        elif value is not None:
            position_end = value.position.end

        super().__init__(Position(position_start, position_end))

    def __repr__(self):
        keyword = f"{self.keyword}"
        value = "" if self.value is None else f" {self.value}"
        condition = "" if self.condition is None else f" if {self.condition}"

        return f"{keyword}{value}{condition}"

    def interpret(self, interpreter):
        if self.keyword == "pass":
            return "Success: Do Nothing"

        if self.condition is not None:
            condition = self.condition.interpret(interpreter)

            if not condition:
                return ""

        if self.keyword == "continue":
            raise errors.UndefinedContinueError(self)

        raise errors.UndefinedBreakError(self)

    def transpile(self, transpiler):
        keyword = "" if self.keyword == "pass" else self.keyword
        value = "" if self.value is None else self.value.transpile(transpiler)

        if self.condition is None:
            return f"{keyword} {value}"

        condition = self.condition.transpile(transpiler)

        return f"if({condition}){{ {keyword} {value} }}"
