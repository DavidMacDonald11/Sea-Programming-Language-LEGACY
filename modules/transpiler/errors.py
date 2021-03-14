class TranspilerError(Exception):
    def __init__(self, message = ""):
        self.message = message
        super().__init__(message)

class IndentError(TranspilerError):
    def __init__(self, message = "Indents must be 4 spaces or 1 tab."):
        super().__init__(message)

class IncorrectScopeError(TranspilerError):
    def __init__(self, correct_scope, scope, message = ""):
        if message == "":
            message = f"Current scope is {correct_scope} indents deep not {scope}."

        super().__init__(message)

class UnknownScopeError(IncorrectScopeError):
    def __init__(self, scope_type, message = ""):
        if message == "":
            message = f"Scope defined by \"{scope_type}:\" is unknown."

        super().__init__(None, None, message)

class EmptyScopeError(IncorrectScopeError):
    def __init__(self, message = "Scope cannot be empty. Use pass to declare empty scope."):
        super().__init__(None, None, message)

class EmptyCScopeError(EmptyScopeError):
    def __init__(self, message = "C Scope cannot be empty."):
        super().__init__(message)
