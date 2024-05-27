import pytest

from src.common.position import Position
from src.lexer.token_kind import TokenKind
from src.parser.errors import SyntaxExpectedTokenException, SyntaxException
from tests.parser.test_parser import create_parser


# region Check If

def test_check_if__exists():
    parser = create_parser("0 test")

    check = parser.check_if(TokenKind.Integer)

    assert check


def test_check_if__missing():
    parser = create_parser("0 test")

    check = parser.check_if(TokenKind.Identifier)

    assert not check


def test_check_if__empty():
    parser = create_parser("")

    check = parser.check_if(TokenKind.Integer)

    assert not check


# endregion

# region Consume

def test_consume__consumed():
    parser = create_parser("1 test")

    first = parser.consume()
    second = parser.consume()

    assert first.kind == TokenKind.Integer
    assert second.kind == TokenKind.Identifier


def test_consume__eof():
    parser = create_parser("2 eof")

    for _ in range(5):
        parser.consume()
    token = parser.consume()

    assert token.kind == TokenKind.EOF


# endregion

# region Consume If

def test_consume_if__matching():
    parser = create_parser("3 match")

    token = parser.consume_if(TokenKind.Integer)

    assert token is not None
    assert token.kind == TokenKind.Integer


def test_consume_if__not_matching():
    parser = create_parser("4 not_match")

    token = parser.consume_if(TokenKind.Identifier)

    assert token is None


def test_consume_if__many_matching():
    parser = create_parser("5 many")

    first = parser.consume_if(TokenKind.Identifier, TokenKind.Integer)
    second = parser.consume_if(TokenKind.Identifier, TokenKind.Integer)

    assert first is not None
    assert second is not None
    assert first.kind == TokenKind.Integer
    assert second.kind == TokenKind.Identifier


def test_consume_if__many_not_matching():
    parser = create_parser("nmany = 6")

    token = parser.consume_if(TokenKind.Fn, TokenKind.Mut)

    assert token is None


# endregion

# region Expect

def test_expect__exists():
    parser = create_parser("exists = 7")

    token = parser.expect(TokenKind.Identifier)

    assert token.kind == TokenKind.Identifier


def test_expect__missing():
    parser = create_parser("mut missing")

    with pytest.raises(SyntaxExpectedTokenException):
        parser.expect(TokenKind.Fn)


def test_expect__custom_error():
    parser = create_parser("mut missing")

    class CustomException(SyntaxException):
        def __init__(self, position: Position):
            super().__init__("Custom exception", position)

    with pytest.raises(CustomException):
        parser.expect(TokenKind.Fn, exception=CustomException)


def test_expect__conditional_exists():
    parser = create_parser("x + y")

    token = parser.expect(TokenKind.Identifier, False)

    assert token.kind == TokenKind.Identifier


def test_expect__conditional_exists_required():
    parser = create_parser("y = 11")

    token = parser.expect(TokenKind.Identifier, True)

    assert token.kind == TokenKind.Identifier


def test_expect__conditional_missing():
    parser = create_parser("12 * c")

    token = parser.expect(TokenKind.Identifier, False)

    assert token is None


def test_expect__conditional_missing_required():
    parser = create_parser("fn main()")

    with pytest.raises(SyntaxExpectedTokenException):
        parser.expect(TokenKind.Identifier, True)


# endregion

# region Expect Match

def test_expect__match_exists():
    parser = create_parser("mut x = 14")

    token = parser.expect([TokenKind.Mut, TokenKind.Identifier])

    assert token is not None
    assert token.kind == TokenKind.Mut


def test_expect__match_missing():
    parser = create_parser("fn main()")

    with pytest.raises(SyntaxExpectedTokenException):
        parser.expect([TokenKind.Mut, TokenKind.Identifier])

# endregion
