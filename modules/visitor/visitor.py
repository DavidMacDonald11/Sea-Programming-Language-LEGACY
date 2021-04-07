from abc import ABC
from abc import abstractmethod
from .symbol_table import SymbolTable
from .helpers import convert_to_camel_case
from ..visitor import errors

class Visitor(ABC):
    vocab_base = None

    def __init__(self, output_stream):
        self.output_stream = output_stream
        self.symbol_table = SymbolTable()
        self.symbol_table.set("int", "null", 0)

    def traverse(self, root):
        self.output_stream.write(f"{self.visit(root)}\n")

    def visit(self, node):
        method_name = f"visit{convert_to_camel_case(node.__name__)}"
        method = getattr(self, method_name, Visitor.no_visit_method)

        return method(node)

    @classmethod
    def no_visit_method(cls, node):
        raise errors.UndefinedVisitMethod(node)

    @abstractmethod
    def visit_number_node(self, node):
        pass

    @abstractmethod
    def visit_variable_access_node(self, node):
        pass

    @abstractmethod
    def visit_variable_assign_node(self, node):
        pass

    @abstractmethod
    def visit_binary_operation_node(self, node):
        pass

    @abstractmethod
    def visit_unary_operation_node(self, node):
        pass
