from position.position import Position
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
        pass

    def transpile(self, memory):
        pass
