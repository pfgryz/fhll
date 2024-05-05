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


# region Punctation

class CommaExpectedError(SyntaxException):
    def __init__(self, position: Position):
        super().__init__("Comma expected", position)


class ColonExpectedError(SyntaxException):
    def __init__(self, position: Position):
        super().__init__("Colon expected", position)


class SemicolonExpectedError(SyntaxException):
    def __init__(self, position: Position):
        super().__init__("Semicolon expected", position)


class ParenthesisExpectedError(SyntaxException):
    def __init__(self, position: Position):
        super().__init__("Parenthesis expected", position)


# endregion

# region Nodes

class NameExpectedError(SyntaxException):
    def __init__(self, position: Position):
        super().__init__("Name expected", position)


class TypeExpectedError(SyntaxException):
    def __init__(self, position: Position):
        super().__init__("Type expected", position)


class ParameterExpectedError(SyntaxException):
    def __init__(self, position: Position):
        super().__init__("Parameter expected", position)


class BlockExpectedError(SyntaxException):
    def __init__(self, position: Position):
        super().__init__("Block expected", position)

# endregion
