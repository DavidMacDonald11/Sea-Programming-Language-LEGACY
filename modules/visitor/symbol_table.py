from types import SimpleNamespace
from modules.lexer.keywords import cast_value_to_type
from ..visitor import errors

class SymbolTable:
    def __init__(self, visitor_type):
        self.interpret = visitor_type.__name__ == "Interpreter"
        self.symbols = {}
        self.parent = None

    def __getitem__(self, key):
        value = self.symbols.get(key, None)

        if value is None and self.parent is not None:
            return self.parent.get(key, None)

        return value

    def __setitem__(self, key, value):
        var = SimpleNamespace()

        var.name = key
        var.type = value[0]
        var.value = value[1]
        var.is_constant = value[2] if len(value) > 2 else False

        if self.interpret:
            var.casted_value = cast_value_to_type(var.type, var.value, not self.interpret)

        self.symbols[key] = var

    def safe_get(self, node):
        key = node.variable_token.value
        var = self[key]

        if var is None:
            raise errors.UndefinedVariableError(node)

        return var

    def safe_set(self, node, value, initial = True):
        key = node.variable_token.value
        value = (node.keyword_token.value, value)

        var = self[key]

        if var is None:
            if not initial:
                raise errors.UndefinedVariableError(node)

            self[key] = value
            return

        if var.is_constant:
            raise errors.ModifyingConstantVariableError(node)

        if initial:
            raise errors.RedeclaredVariableError(node)

    def __delitem__(self, key):
        del self.symbols[key]
