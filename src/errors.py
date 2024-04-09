from src.location import Location
from src.position import Position


class IdentifierTooLongError(Exception):
    def __init__(self, location: Location):
        super().__init__(self)
        self.message = "The identifier you provided is too long."
        self.location = location


class IntegerOverflowError(Exception):
    def __init__(self, location: Location):
        super().__init__(self)
        self.message = "Integer overflow detected."
        self.location = location


class IntegerLeadingZerosError(Exception):
    def __init__(self, location: Location):
        super().__init__(self)
        self.message = "Integer leading zeros detected."
        self.location = location


class StringTooLongError(Exception):
    def __init__(self, location: Location):
        super().__init__(self)
        self.message = "The string you provided is too long."
        self.location = location


class UnterminatedStringError(Exception):
    def __init__(self, location: Location):
        super().__init__(self)
        self.message = "Undetermined string literal"
        self.location = location


class InvalidEscapeSequenceError(Exception):
    def __init__(self, position: Position):
        super().__init__(self)
        self.message = "Invalid escape sequence"
        self.position = position
