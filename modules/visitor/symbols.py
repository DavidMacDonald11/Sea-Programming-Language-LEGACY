from ..visitor import errors

class Symbol:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"{self.name}: {self.value}"

    def modify(self, value, node):
        pass

class Variable(Symbol):
    def __init__(self, name, var_type, value):
        self.type = var_type
        super().__init__(name, value)

    def __repr__(self):
        return f"{self.type} {self.name}: {self.value}"

    def modify(self, value, node):
        self.value = value

class Constant(Symbol):
    def modify(self, value, node):
        raise errors.ModifyingConstantError(node, self)

class ConstantVariable(Constant, Variable):
    pass
