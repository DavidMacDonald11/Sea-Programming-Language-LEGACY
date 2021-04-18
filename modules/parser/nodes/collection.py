from types import SimpleNamespace
from .ast_node import ASTNode
from .binary_operation_node import BinaryOperationNode
from .constant_define_node import ConstantDefineNode
from .constant_undefine_node import ConstantUndefineNode
from .eof_node import EOFNode
from .if_node import IfNode
from .left_unary_operation_node import LeftUnaryOperationNode
from .line_node import LineNode
from .number_node import NumberNode
from .sequential_operation_node import SequentialOperationNode
from .symbol_access_node import SymbolAccessNode
from .ternary_operation_node import TernaryOperationNode
from .variable_assign_node import VariableAssignNode

NODES = SimpleNamespace(
    ASTNode = ASTNode,
    BinaryOperationNode = BinaryOperationNode,
    ConstantDefineNode = ConstantDefineNode,
    ConstantUndefineNode = ConstantUndefineNode,
    EOFNode = EOFNode,
    IfNode = IfNode,
    LeftUnaryOperationNode = LeftUnaryOperationNode,
    LineNode = LineNode,
    NumberNode = NumberNode,
    SequentialOperationNode = SequentialOperationNode,
    SymbolAccessNode = SymbolAccessNode,
    TernaryOperationNode = TernaryOperationNode,
    VariableAssignNode = VariableAssignNode
)