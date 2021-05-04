from position.position import Position
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

        super().__init__(Position(position_start, position_end))

    def __repr__(self):
        else_str = ")" if self.else_case is None else f", ELSE, {{{self.else_case}}})"
        for_triple = f"{self.assignment}; {self.condition}; {self.reassignment}"

        return f"(FOR, {{(({for_triple}), {self.block})}}" + else_str

    def interpret(self, memory):
        pass

    def transpile(self, memory):
        pass
