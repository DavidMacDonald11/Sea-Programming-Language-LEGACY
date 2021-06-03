from position.position import Position
from memory.stack import stack
from interpreting import errors
from ..ast_node import ASTNode

class ForNode(ASTNode):
    def __init__(self, for_token, triple, block, else_case = None):
        self.assignment = triple[0]
        self.condition = triple[1]
        self.reassignment = triple[2]
        self.block = block
        self.else_case = else_case

        position_start = for_token.position.start
        position_end = (else_case if else_case is not None else block).position.end
        stream = for_token.position.stream

        super().__init__(Position(stream, position_start, position_end))

    def __repr__(self):
        else_str = ")" if self.else_case is None else f", ELSE, {{{self.else_case}}})"
        for_triple = f"{self.assignment}; {self.condition}; {self.reassignment}"

        return f"(FOR, {{(({for_triple}), {self.block})}}" + else_str

    def interpret(self, memory):
        with stack(memory):
            self.assignment.interpret(memory)
            broke = False

            while self.condition.interpret(memory):
                try:
                    self.block.interpret(memory)
                except errors.UndefinedBreakError:
                    broke = True
                    break
                except errors.UndefinedContinueError:
                    continue

                self.reassignment.interpret(memory)

            if self.else_case is not None and not broke:
                self.else_case.interpret(memory)

            return ""

    def transpile(self, memory):
        with stack(memory.memory):
            broke_variable = f"__sea__Broke_{memory.depth}"
            memory.headers.add(f"int {broke_variable} = 0;")
            memory.break_depth = memory.depth

            assignment = self.assignment.transpile(memory)
            condition = self.condition.transpile(memory)
            reassignment = self.reassignment.transpile(memory)
            expression = self.block.transpile(memory)

            indent = "\t" * memory.break_depth
            inner_indent = "\t" * memory.depth

            result = f"for({assignment}; {condition}; {reassignment})\n"
            result += f"{indent}{{\n{expression}{indent}}}\n"
            result += f"if({broke_variable})\n{indent}{{\n"
            result += f"{inner_indent}{broke_variable} = 0;\n{indent}}}\n"

            if self.else_case is not None:
                result += f"else\n{indent}{{\n{self.else_case.transpile(memory)}{indent}}}\n"

            return result
