from src.common.position import Position
from src.lexer.token_kind import TokenKind


class ParserError(Exception):
    def __init__(self, message: str, position: Position):
        self.message = message
        self.position = position

        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message} at {self.position}"


class TokenExpectedError(ParserError):
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


class UnexpectedTokenError(ParserError):
    def __init__(self, position: Position):
        super().__init__("Unexpected token", position)


# region Punctuation

class CommaExpectedError(ParserError):
    def __init__(self, position: Position):
        super().__init__("Comma expected", position)


class ColonExpectedError(ParserError):
    def __init__(self, position: Position):
        super().__init__("Colon expected", position)


class SemicolonExpectedError(ParserError):
    def __init__(self, position: Position):
        super().__init__("Semicolon expected", position)


class ParenthesisExpectedError(ParserError):
    def __init__(self, position: Position):
        super().__init__("Parenthesis expected", position)


class BraceExpectedError(ParserError):
    def __init__(self, position: Position):
        super().__init__("Brace expected", position)


class AssignExpectedError(ParserError):
    def __init__(self, position: Position):
        super().__init__("Assign expected", position)


class BoldArrowExpectedError(ParserError):
    def __init__(self, position: Position):
        super().__init__("Bold arrow expected", position)


# endregion

# region Nodes

class NameExpectedError(ParserError):
    def __init__(self, position: Position):
        super().__init__("Name expected", position)


class TypeExpectedError(ParserError):
    def __init__(self, position: Position):
        super().__init__("Type expected", position)


class ParameterExpectedError(ParserError):
    def __init__(self, position: Position):
        super().__init__("Parameter expected", position)


class ExpressionExpectedError(ParserError):
    def __init__(self, position: Position):
        super().__init__("Expression expected", position)


class BlockExpectedError(ParserError):
    def __init__(self, position: Position):
        super().__init__("Block expected", position)


class MatchersExpectedError(ParserError):
    def __init__(self, position: Position):
        super().__init__("Matchers expected", position)


# endregion

# region Keywords

class LetKeywordExpectedError(ParserError):
    def __init__(self, position: Position):
        super().__init__("Let keyword expected", position)

# endregion
