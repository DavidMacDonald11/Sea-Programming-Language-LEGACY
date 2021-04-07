from functools import wraps

def subscript(index):
    def outer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            value = func(*args, **kwargs)

            if value is None:
                return None

            return value[index]

        return wrapper

    return outer

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None

    @subscript(1)
    def get(self, name):
        value = self.symbols.get(name, None)

        if value is None and self.parent is not None:
            return self.parent.get(name)

        return value

    @subscript(0)
    def get_type(self, name):
        value = self.symbols.get(name, None)

        if value is None and self.parent is not None:
            return self.parent.get(name)

        return value

    def set(self, var_type, var_name, value = None):
        self.symbols[var_name] = (var_type, value)

    def remove(self, name):
        del self.symbols[name]
