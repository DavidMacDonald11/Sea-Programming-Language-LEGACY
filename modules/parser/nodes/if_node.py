from modules.lexer.position import Position
from .ast_node import ASTNode

class IfNode(ASTNode):
    def __init__(self, if_token, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        position_start = if_token.position.start
        position_end = (else_case or cases[-1][1]).position.end

        super().__init__(Position(position_start, position_end))

    def __repr__(self):
        else_str = ")" if not self.else_case else f", ELSE, {{{self.else_case}}})"
        return f"(IF, {{{self.cases}}}" + else_str

    def interpret(self, interpreter):
        for condition, expression in self.cases:
            condition_value = condition.interpret(interpreter)

            if condition_value:
                return expression.interpret(interpreter)

        if self.else_case is not None:
            return self.else_case.interpret(interpreter)

        return ""

    def transpile(self, transpiler):
        statement = ""
        first = True

        for condition, expression in self.cases:
            condition_value = condition.transpile(transpiler)

            if first:
                statement += f"if({condition_value})\n{{\n"
                first = False
            else:
                statement += f"else if({condition_value})\n{{\n"

            statement += f"{expression.transpile(transpiler)}"
            statement += "}\n"

        if self.else_case is not None:
            statement += f"else\n{{\n{self.else_case.transpile(transpiler)}}}\n"

        return statement
