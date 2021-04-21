from modules.visitor.symbol_table import SymbolTable
from .ast_node import ASTNode
from .if_node import IfNode

class LineNode(ASTNode):
    def __init__(self, expression, depth, no_end = False):
        self.expression = expression
        self.depth = depth
        self.no_end = no_end

        super().__init__(expression.position)

    def __repr__(self):
        return f"[{self.expression}]"

    def interpret(self, interpreter):
        return self.get_expression(interpreter)

    def transpile(self, transpiler):
        transpiler.depth = self.depth
        expression = self.get_expression(transpiler)
        indent = "\t" * self.depth

        return f"{indent}{expression}{'' if self.no_end else ';'}\n"

    def get_expression(self, visitor):
        if isinstance(self.expression, IfNode):
            visitor.symbol_table = SymbolTable(visitor.symbol_table)
            expression = self.expression.visit(visitor)
            visitor.symbol_table = visitor.symbol_table.parent

            return expression

        return self.expression.visit(visitor)
