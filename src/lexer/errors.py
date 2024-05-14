from src.common.location import Location
from src.common.position import Position
from src.lexer.token_kind import TokenKind


class LexerError(Exception):
    def __init__(self, message: str, location: Location):
        self.message = message
        self.location = location

        super().__init__(message)

    def __str__(self):
        return f"{self.message} {str(self.location)}"


class IdentifierTooLongError(LexerError):
    def __init__(self, location: Location):
        super().__init__("Provided identifier is too long", location)


class IntegerOverflowError(LexerError):
    def __init__(self, location: Location):
        super().__init__("Provided integer literal overflow", location)


class IntegerLeadingZerosError(LexerError):
    def __init__(self, location: Location):
        super().__init__("Provided integer literal has leading zeros",
                         location)


class StringTooLongError(LexerError):
    def __init__(self, location: Location):
        super().__init__("Provided string is too long", location)


class UnterminatedStringError(LexerError):
    def __init__(self, location: Location):
        super().__init__("Undetermined string literal", location)


class InvalidEscapeSequenceError(LexerError):
    def __init__(self, location: Location):
        super().__init__("Invalid escape sequence", location)


class ExpectingCharError(LexerError):
    def __init__(self, expected: str, got: str, kind: TokenKind,
                 position: Position):
        self.expected = expected
        self.got = got

        super().__init__(f"Expected {expected} got {got} at "
                         f"position {position} by {kind}",
                         Location.at(position))
