from lexing.position.position import Position

class SeaError(Exception):
    def __init__(self, position = None, message = ""):
        self.position = position if position is not None else Position(None)
        self.message = message
        super().__init__(message)

    def get_message(self):
        return self.message
