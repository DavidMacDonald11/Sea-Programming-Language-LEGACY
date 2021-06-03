from position.position import Position
from memory.stack import stack
from ..ast_node import ASTNode

class IfNode(ASTNode):
    def __init__(self, if_token, cases, else_case = None):
        self.cases = cases
        self.else_case = else_case

        position_start = if_token.position.start
        position_end = (else_case if else_case is not None else cases[-1][1]).position.end
        stream = if_token.position.stream

        super().__init__(Position(stream, position_start, position_end))

    def __repr__(self):
        else_str = ")" if self.else_case is None else f", ELSE, {{{self.else_case}}})"
        return f"(IF, {{{self.cases}}}" + else_str

    def interpret(self, memory):
        with stack(memory):
            for condition, expression in self.cases:
                condition_value = condition.interpret(memory)

                if condition_value:
                    return expression.interpret(memory)

            if self.else_case is not None:
                return self.else_case.interpret(memory)

            return ""

    def transpile(self, memory):
        with stack(memory.memory):
            indent = "\t" * memory.depth
            statement = ""
            first = True

            for condition, expression in self.cases:
                condition_value = condition.transpile(memory)

                if first:
                    statement += f"if({condition_value})\n{indent}{{\n"
                    first = False
                else:
                    statement += f"else if({condition_value})\n{indent}{{\n"

                statement += f"{expression.transpile(memory)}"
                statement += f"{indent}}}\n"

            if self.else_case is not None:
                statement += f"else\n{indent}{{\n{self.else_case.transpile(memory)}{indent}}}\n"

            return statement
