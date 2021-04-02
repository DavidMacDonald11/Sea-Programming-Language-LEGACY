class Token:
    TYPES = {
        " \t": "INDENT",
        "0123456789": "INT",
        "0123456789.": "FLOAT",
        "+": "PLUS",
        "-": "MINUS",
        "*": "MULTIPLY",
        "/": "DIVIDE",
        "(": "LPAREN",
        ")": "RPAREN"
    }

    SYMBOLS = {value:key for key, value in TYPES.items()}

    def __init__(self, token_type, value = None):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f"{self.type}" + ("" if self.value is None else f":{self.value}")
