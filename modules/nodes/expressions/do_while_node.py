from position.position import Position
from memory.stack import stack
from interpreting import errors
from ..ast_node import ASTNode

class DoWhileNode(ASTNode):
    def __init__(self, do_token, block, condition, else_case = None):
        self.block = block
        self.condition = condition
        self.else_case = else_case

        position_start = do_token.position.start
        position_end = (else_case if else_case is not None else block).position.end
        stream = do_token.position.stream

        super().__init__(Position(stream, position_start, position_end))

    def __repr__(self):
        else_str = ")" if self.else_case is None else f", ELSE, {{{self.else_case}}})"
        return f"(DO, {{{self.block}}}, WHILE, {self.condition}" + else_str

    def interpret(self, memory):
        with stack(memory):
            broke = False

            while True:
                try:
                    self.block.interpret(memory)
                except errors.UndefinedBreakError:
                    broke = True
                    break
                except errors.UndefinedContinueError:
                    pass

                if not self.condition.interpret(memory):
                    break

            if self.else_case is not None and not broke:
                self.else_case.interpret(memory)

            return ""

    def transpile(self, memory):
        with stack(memory):
            broke_variable = f"__sea__Broke_{memory.depth}"
            memory.headers.add(f"int {broke_variable} = 0;")
            memory.break_depth = memory.depth

            condition = self.condition.transpile(memory)
            expression = self.block.transpile(memory)
            indent = "\t" * memory.break_depth
            inner_indent = "\t" * memory.depth

            result = f"do {{\n{expression}{indent}}}"
            result += f"while({condition});\n"
            result += f"if({broke_variable})\n{indent}{{\n"
            result += f"{inner_indent}{broke_variable} = 0;\n{indent}}}\n"

            if self.else_case is not None:
                result += f"else\n{indent}{{\n{self.else_case.transpile(memory)}{indent}}}\n"

            return result
