from .position import Position

class Token:
    TYPES = {
        " \t": "INDENT",
        "\n": "LINEEND",
        "0123456789": "INT",
        "0123456789.": "FLOAT",
        "+": "PLUS",
        "-": "MINUS",
        "*": "MUL",
        "/": "DIV",
        "(": "LPAREN",
        ")": "RPAREN",
        "": "EOF"
    }

    SYMBOLS = {value:key for key, value in TYPES.items()}

    def __init__(self, token_type, value = None, position = Position()):
        self.type = token_type
        self.value = value
        self.position = position

    def __repr__(self):
        return f"{self.type}" + ("" if self.value is None else f":{self.value}")
