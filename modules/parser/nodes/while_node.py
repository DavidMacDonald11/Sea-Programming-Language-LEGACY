from modules.lexer.position import Position
from .ast_node import ASTNode
from ...parser import errors

class WhileNode(ASTNode):
    def __init__(self, while_token, condition, expression, else_case = None):
        self.condition = condition
        self.expression = expression
        self.else_case = else_case

        position_start = while_token.position.start
        position_end = (else_case or expression).position.end

        super().__init__(Position(position_start, position_end))

    def __repr__(self):
        else_str = ")" if not self.else_case else f", ELSE, {{{self.else_case}}})"
        return f"(WHILE, {{({self.condition}, {self.expression})}}" + else_str

    def interpret(self, interpreter):
        broke = False

        while self.condition.interpret(interpreter):
            try:
                self.expression.interpret(interpreter)
            except errors.UndefinedBreakError:
                broke = True
                break
            except errors.UndefinedContinueError:
                continue

        if self.else_case is not None and not broke:
            self.else_case.interpret(interpreter)

        return ""

    def transpile(self, transpiler):
        broke_variable = f"__sea__Broke_{transpiler.depth}"
        transpiler.headers.add(f"int {broke_variable} = 0;")
        transpiler.break_depth = transpiler.depth

        condition = self.condition.transpile(transpiler)
        expression = self.expression.transpile(transpiler)
        indent = "\t" * transpiler.break_depth
        inner_indent = "\t" * transpiler.depth

        result = f"while({condition})\n{indent}{{\n{expression}{indent}}}\n"
        result += f"if({broke_variable})\n{indent}{{\n"
        result += f"{inner_indent}{broke_variable} = 0;\n{indent}}}\n"

        if self.else_case is not None:
            result += f"else\n{indent}{{\n{self.else_case.transpile(transpiler)}{indent}}}\n"

        return result
