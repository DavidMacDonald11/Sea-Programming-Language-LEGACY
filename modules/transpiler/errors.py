class TranspilerError(Exception):
    def __init__(self, message = ""):
        self.message = message
        super().__init__(message)

    def get_message(self):
        return self.message
