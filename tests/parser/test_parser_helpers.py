import pytest

from src.common.position import Position
from src.lexer.token_kind import TokenKind
from src.parser.errors import TokenExpectedError, ParserError
from tests.parser.test_parser import create_parser


# region Check If

def test_check_if__exists():
    parser = create_parser("0 test", True)

    check = parser.check_if(TokenKind.Integer)

    assert check


def test_check_if__missing():
    parser = create_parser("0 test", True)

    check = parser.check_if(TokenKind.Identifier)

    assert not check


def test_check_if__empty():
    parser = create_parser("0 test", False)

    check = parser.check_if(TokenKind.Integer)

    assert not check


# endregion

# region Consume

def test_consume__consumed():
    parser = create_parser("1 test", True)

    first = parser.consume()
    second = parser.consume()

    assert first.kind == TokenKind.Integer
    assert second.kind == TokenKind.Identifier


def test_consume__eof():
    parser = create_parser("2 eof", True)

    for _ in range(5):
        parser.consume()
    token = parser.consume()

    assert token.kind == TokenKind.EOF


# endregion

# region Consume If

def test_consume_if__matching():
    parser = create_parser("3 match", True)

    token = parser.consume_if(TokenKind.Integer)

    assert token is not None
    assert token.kind == TokenKind.Integer


def test_consume_if__not_matching():
    parser = create_parser("4 not_match", True)

    token = parser.consume_if(TokenKind.Identifier)

    assert token is None


# endregion

# region Consume Match

def test_consume_match__matching():
    parser = create_parser("5 many", True)

    first = parser.consume_match([TokenKind.Identifier, TokenKind.Integer])
    second = parser.consume_match([TokenKind.Identifier, TokenKind.Integer])

    assert first is not None
    assert second is not None
    assert first.kind == TokenKind.Integer
    assert second.kind == TokenKind.Identifier


def test_consume_match__not_matching():
    parser = create_parser("nmany = 6", True)

    token = parser.consume_match([TokenKind.Fn, TokenKind.Mut])

    assert token is None


# endregion

# region Expect

def test_expect__exists():
    parser = create_parser("exists = 7", True)

    token = parser.expect(TokenKind.Identifier)

    assert token.kind == TokenKind.Identifier


def test_expect__missing():
    parser = create_parser("mut missing", True)

    with pytest.raises(TokenExpectedError):
        parser.expect(TokenKind.Fn)


def test_expect__custom_error():
    parser = create_parser("mut missing", True)

    class CustomException(ParserError):
        def __init__(self, position: Position):
            super().__init__("Custom exception", position)

    with pytest.raises(CustomException):
        parser.expect(TokenKind.Fn, CustomException)


# endregion

# region Expect Conditional

def test_expect_conditional__exists():
    parser = create_parser("x + y", True)

    token = parser.expect_conditional(TokenKind.Identifier, False)

    assert token.kind == TokenKind.Identifier


def test_expect_conditional__exists_required():
    parser = create_parser("y = 11", True)

    token = parser.expect_conditional(TokenKind.Identifier, True)

    assert token.kind == TokenKind.Identifier


def test_expect_conditional__missing():
    parser = create_parser("12 * c", True)

    token = parser.expect_conditional(TokenKind.Identifier, False)

    assert token is None


def test_expect_conditional__missing_required():
    parser = create_parser("fn main()", True)

    with pytest.raises(TokenExpectedError):
        parser.expect_conditional(TokenKind.Identifier, True)


# endregion

# region Expect Match

def test_expect_match__exists():
    parser = create_parser("mut x = 14", True)

    token = parser.expect_match([TokenKind.Mut, TokenKind.Identifier])

    assert token is not None
    assert token.kind == TokenKind.Mut


def test_expect_match__missing():
    parser = create_parser("fn main()", True)

    with pytest.raises(TokenExpectedError):
        parser.expect_match([TokenKind.Mut, TokenKind.Identifier])

# endregion
