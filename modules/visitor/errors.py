from modules.errors import errors
from .helpers import convert_to_camel_case

class VisitorError(errors.SeaError):
    def __init__(self, node, message = ""):
        self.node = node
        super().__init__(message)

class UndefinedVisitMethod(VisitorError):
    def __init__(self, node, message = ""):
        self.name = type(node).__name__
        super().__init__(node, message)

    def get_message(self):
        return f"No visit{convert_to_camel_case(self.name)} method defined."
