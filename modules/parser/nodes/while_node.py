from modules.lexer.position import Position
from .ast_node import ASTNode
from ...parser import errors

class WhileNode(ASTNode):
    def __init__(self, while_token, condition, expression):
        self.condition = condition
        self.expression = expression

        position_start = while_token.position.start
        position_end = expression.position.end

        super().__init__(Position(position_start, position_end))

    def __repr__(self):
        return f"(WHILE, {{({self.condition}, {self.expression})}})"

    def interpret(self, interpreter):
        while self.condition.interpret(interpreter):
            try:
                self.expression.interpret(interpreter)
            except errors.UndefinedBreakError:
                break
            except errors.UndefinedContinueError:
                continue

        return ""

    def transpile(self, transpiler):
        condition = self.condition.transpile(transpiler)
        expression = self.expression.transpile(transpiler)

        return f"while({condition})\n{{\n{expression}}}\n"
