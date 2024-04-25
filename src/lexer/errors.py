from src.lexer.location import Location
from src.lexer.position import Position
from src.lexer.token_kind import TokenKind


class LexerException(Exception):
    pass


class IdentifierTooLongException(LexerException):
    def __init__(self, location: Location):
        super().__init__(self)
        self.message = "Provided identifier is too long."
        self.location = location


class IntegerOverflowException(LexerException):
    def __init__(self, location: Location):
        super().__init__(self)
        self.message = "Provided integer literal overflow."
        self.location = location


class IntegerLeadingZerosException(LexerException):
    def __init__(self, location: Location):
        super().__init__(self)
        self.message = "Provided integer literal has leading zeros"
        self.location = location


class StringTooLongException(LexerException):
    def __init__(self, location: Location):
        super().__init__(self)
        self.message = "Provided string is too long."
        self.location = location


class UnterminatedStringException(LexerException):
    def __init__(self, location: Location):
        super().__init__(self)
        self.message = "Undetermined string literal"
        self.location = location


class InvalidEscapeSequenceException(LexerException):
    def __init__(self, position: Position):
        super().__init__(self)
        self.message = "Invalid escape sequence"
        self.position = position


class ExpectingCharException(LexerException):
    def __init__(self, expected: str, got: str, kind: TokenKind,
                 position: Position):
        super().__init__(self)
        self.message = (f"Expected {expected} got {got} at "
                        f"position {position} by {kind}")
        self.expected = expected
        self.got = got
        self.position = position
