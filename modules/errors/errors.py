class SeaError(Exception):
    def __init__(self, position = None, message = ""):
        self.position = position
        self.message = message
        super().__init__(message)

    def get_message(self):
        return self.message

class SeaWarning(SeaError):
    pass
