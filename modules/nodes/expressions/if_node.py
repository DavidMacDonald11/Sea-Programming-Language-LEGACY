from position.position import Position
from ..ast_node import ASTNode

class IfNode(ASTNode):
    def __init__(self, if_token, cases, else_case = None):
        self.cases = cases
        self.else_case = else_case

        position_start = if_token.position.start
        position_end = (else_case if else_case is not None else cases[-1][1]).position.end

        super().__init__(Position(position_start, position_end))

    def __repr__(self):
        else_str = ")" if self.else_case is None else f", ELSE, {{{self.else_case}}})"
        return f"(IF, {{{self.cases}}}" + else_str

    def interpret(self, memory):
        pass

    def transpile(self, memory):
        pass
