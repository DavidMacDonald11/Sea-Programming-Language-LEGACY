from modules.lexer.keywords import cast_value_to_type
from modules.visitor import symbols
from .ast_node import ASTNode

class VariableAssignNode(ASTNode):
    def __init__(self, variable_type, variable, value):
        self.type = variable_type
        self.variable = variable
        self.value = value

        self.var_name = variable.value
        self.var_type = variable_type.value

        super().__init__(variable.position)

    def __repr__(self):
        return f"({self.type}, {self.variable}, EQUALS, {self.value})"

    def interpret(self, interpreter):
        return self.save_in_symbol_table(interpreter, self.var_type, True)

    def transpile(self, transpiler):
        var_type = "int" if self.var_type == "bool" else self.var_type
        value = self.save_in_symbol_table(transpiler, var_type)

        return f"({var_type} {self.var_name} = {value})"

    def save_in_symbol_table(self, visitor, var_type, cast = False):
        value = self.value.visit(visitor)

        if cast:
            value = cast_value_to_type(var_type, value)

        found = visitor.symbol_table[self.var_name]

        if found is not None:
            found.modify(value, self)
        else:
            variable = symbols.Variable(self.var_name, var_type, value)
            visitor.symbol_table[self.var_name] = variable

        return value
