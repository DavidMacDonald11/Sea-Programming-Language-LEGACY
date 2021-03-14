class MetaScope(type):
    @property
    def allows_empty(cls):
        return cls._allows_empty

    @property
    def allows_verbatum(cls):
        return cls._allows_verbatum

    @property
    def lines_are_indented(cls):
        return cls._lines_are_indented

    @property
    def sea_declaration(cls):
        return cls._sea_declaration

    @property
    def c_declaration(cls):
        return cls._c_declaration

    @property
    def sea_ending(cls):
        return cls._sea_ending

    @property
    def c_ending(cls):
        return cls._c_ending
