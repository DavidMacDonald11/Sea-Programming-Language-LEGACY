from errors.errors import SeaError

class ParserError(SeaError):
    parser = None

    def __init__(self, position = None, message = ""):
        if position is None:
            position = type(self).parser.position.copy()

        super().__init__(position, message)
