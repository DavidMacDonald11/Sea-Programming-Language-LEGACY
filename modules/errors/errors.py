class MessageException(Exception):
    def __init__(self, message = ""):
        self.message = message
        super().__init__(message)

    def get_message(self):
        return self.message

class SeaError(MessageException):
    pass

class HandledSeaError(MessageException):
    def __init__(self, position, error):
        self.position = position
        self.error = error
        super().__init__(error.message)

    def get_message(self):
        return self.error.get_message()

    def get_name(self):
        return type(self.error).__name__
