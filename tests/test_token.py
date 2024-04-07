import pytest

from src.location import Location
from src.position import Position
from src.token import Token
from src.token_kind import TokenKind


@pytest.fixture
def invalid_token():
    location = Location(
        Position(1, 1),
        Position(1, 5)
    )
    return Token(TokenKind.Invalid, location)


@pytest.fixture
def identifier():
    location = Location(
        Position(4, 15),
        Position(4, 25)
    )
    return Token(TokenKind.Identifier, location, value="lexer")


def test_token(invalid_token):
    assert invalid_token.kind == TokenKind.Invalid
    assert invalid_token.location.begin == Position(1, 1)
    assert invalid_token.location.end == Position(1, 5)
    assert invalid_token.value is None


def test_token_str(invalid_token):
    assert str(invalid_token) == "<invalid>(None) at <1:1>"


def test_identifier_token_str(identifier):
    assert str(identifier) == "identifier('lexer') at <4:15>"


def test_token_repr(invalid_token):
    assert repr(invalid_token) == ("Token("
                                   "kind=TokenKind.Invalid, "
                                   "location=Location("
                                   "begin=Position(line=1, column=1), "
                                   "end=Position(line=1, column=5)), "
                                   "value=None)")


def test_identifier_token_repr(identifier):
    assert repr(identifier) == ("Token("
                                "kind=TokenKind.Identifier, "
                                "location=Location("
                                "begin=Position(line=4, column=15), "
                                "end=Position(line=4, column=25)), "
                                "value='lexer')")
