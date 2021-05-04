from position.position import Position
from ..ast_node import ASTNode

class DoWhileNode(ASTNode):
    def __init__(self, do_token, block, condition, else_case = None):
        self.block = block
        self.condition = condition
        self.else_case = else_case

        position_start = do_token.position.start
        position_end = (else_case if else_case is not None else block).position.end

        super().__init__(Position(position_start, position_end))

    def __repr__(self):
        else_str = ")" if self.else_case is None else f", ELSE, {{{self.else_case}}})"
        return f"(DO, {{{self.block}}}, WHILE, {self.condition}" + else_str

    def interpret(self, memory):
        pass

    def transpile(self, memory):
        pass
