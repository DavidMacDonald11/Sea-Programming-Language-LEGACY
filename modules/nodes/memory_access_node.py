from .ast_node import ASTNode

class MemoryAccessNode(ASTNode):
    def __init__(self, identifier):
        self.identifier = identifier
        super().__init__(identifier.position)

    def __repr__(self):
        return f"{self.identifier}"
