from src.common.position import Position
from src.lexer.token_kind import TokenKind


class ParserException(Exception):
    pass


class SyntaxException(ParserException):
    def __init__(self, message: str, position: Position):
        self.message = message
        self.position = position

        super().__init__(self.message)


class SyntaxExpectedTokenException(ParserException):
    def __init__(self, expected: TokenKind | list[TokenKind], got: TokenKind,
                 position: Position):
        if isinstance(expected, list):
            name = "or".join([e.value for e in expected])
        else:
            name = expected.value

        self.message = (f"Expected \"{name}\", "
                        f"got \"{got.value}\" at {position}")
        self.expected = expected
        self.got = got

        super().__init__(self.message, position)
