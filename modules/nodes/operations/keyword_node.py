from position.position import Position
from ..ast_node import ASTNode

class KeywordOperationNode(ASTNode):
    def __init__(self, keyword_token, value = None, condition = None):
        self.keyword_token = keyword_token
        self.keyword = keyword_token.keyword
        self.value = value
        self.condition = condition

        position_start = keyword_token.position.start
        position_end = keyword_token.position.end

        if condition is not None:
            position_end = condition.position.end
        elif value is not None:
            position_end = value.position.end

        super().__init__(Position(position_start, position_end))

    def __repr__(self):
        keyword = f"{self.keyword}"
        value = "" if self.value is None else f" {self.value}"
        condition = "" if self.condition is None else f" if {self.condition}"

        return f"{keyword}{value}{condition}"
