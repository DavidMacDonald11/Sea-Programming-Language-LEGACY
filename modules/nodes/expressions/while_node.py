from position.position import Position
from memory.stack import stack
from interpreting import errors
from ..ast_node import ASTNode

class WhileNode(ASTNode):
    def __init__(self, while_token, condition, block, else_case = None):
        self.condition = condition
        self.block = block
        self.else_case = else_case

        position_start = while_token.position.start
        position_end = (else_case if else_case is not None else block).position.end

        super().__init__(Position(position_start, position_end))

    def __repr__(self):
        else_str = ")" if not self.else_case else f", ELSE, {{{self.else_case}}})"
        return f"(WHILE, {{({self.condition}, {self.block})}}" + else_str

    def interpret(self, memory):
        with stack(memory):
            broke = False

            while self.condition.interpret(memory):
                try:
                    self.block.interpret(memory)
                except errors.UndefinedBreakError:
                    broke = True
                    break
                except errors.UndefinedContinueError:
                    continue

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

            result = f"while({condition})\n{indent}{{\n{expression}{indent}}}\n"
            result += f"if({broke_variable})\n{indent}{{\n"
            result += f"{inner_indent}{broke_variable} = 0;\n{indent}}}\n"

            if self.else_case is not None:
                result += f"else\n{indent}{{\n{self.else_case.transpile(memory)}{indent}}}\n"

            return result
