import pytest

from src.lexer.token_kind import TokenKind
from src.parser.errors import SyntaxExpectedTokenException
from tests.parser.test_parser import create_parser


def test_consume():
    parser = create_parser("1 test", True)

    first = parser.consume()
    second = parser.consume()

    assert first.kind == TokenKind.Integer
    assert second.kind == TokenKind.Identifier


def test_consume_eof():
    parser = create_parser("2 eof", True)

    for _ in range(5):
        parser.consume()
    token = parser.consume()

    assert token.kind == TokenKind.EOF


def test_consume_if_matching():
    parser = create_parser("3 match", True)

    token = parser.consume_if(TokenKind.Integer)

    assert token is not None
    assert token.kind == TokenKind.Integer


def test_consume_if_not_matching():
    parser = create_parser("4 not_match", True)

    token = parser.consume_if(TokenKind.Identifier)

    assert token is None


def test_consume_match_matching():
    parser = create_parser("5 many", True)

    first = parser.consume_match([TokenKind.Identifier, TokenKind.Integer])
    second = parser.consume_match([TokenKind.Identifier, TokenKind.Integer])

    assert first is not None
    assert second is not None
    assert first.kind == TokenKind.Integer
    assert second.kind == TokenKind.Identifier


def test_consume_match_not_matching():
    parser = create_parser("nmany = 6", True)

    token = parser.consume_match([TokenKind.Fn, TokenKind.Mut])

    assert token is None


def test_expect_exists():
    parser = create_parser("exists = 7", True)

    token = parser.expect(TokenKind.Identifier)

    assert token.kind == TokenKind.Identifier


def test_expect_missing():
    parser = create_parser("mut missing", True)

    with pytest.raises(SyntaxExpectedTokenException):
        parser.expect(TokenKind.Fn)


def test_expect_conditional_exists():
    parser = create_parser("x + y", True)

    token = parser.expect_conditional(TokenKind.Identifier, False)

    assert token.kind == TokenKind.Identifier


def test_expect_conditional_exists_required():
    parser = create_parser("y = 10", True)

    token = parser.expect_conditional(TokenKind.Identifier, True)

    assert token.kind == TokenKind.Identifier


def test_expect_conditional_missing():
    parser = create_parser("11 * c", True)

    token = parser.expect_conditional(TokenKind.Identifier, False)

    assert token is None


def test_expect_conditional_missing_required():
    parser = create_parser("fn main()", True)

    with pytest.raises(SyntaxExpectedTokenException):
        parser.expect_conditional(TokenKind.Identifier, True)


def test_expect_match_exists():
    parser = create_parser("mut x = 13", True)

    token = parser.expect_match([TokenKind.Mut, TokenKind.Identifier])

    assert token is not None
    assert token.kind == TokenKind.Mut


def test_expect_match_missing():
    parser = create_parser("fn main()", True)

    with pytest.raises(SyntaxExpectedTokenException):
        parser.expect_match([TokenKind.Mut, TokenKind.Identifier])
