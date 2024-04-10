from typing import Any

import pytest
from _pytest.mark import ParameterSet

from src.buffer import StreamBuffer
from src.errors import IdentifierTooLongError, IntegerOverflowError, \
    IntegerLeadingZerosError, StringTooLongError, UnterminatedStringError
from src.lexer import Lexer
from src.location import Location
from src.position import Position
from src.token import Token
from src.token_kind import TokenKind


# region Helpers

def create_lexer(string: str) -> Lexer:
    stream = StreamBuffer.from_str(string)
    lexer = Lexer(stream)
    return lexer


def create_token_test_case(content: str, kind: TokenKind,
                           value: Any = None) -> ParameterSet:
    lexer = create_lexer(content)
    token = Token(kind, Location(Position(1, 1), Position(1, len(content))),
                  value)
    return pytest.param(lexer, token, id=kind.value)


def create_kind_test_case(content: str, kind: TokenKind) -> ParameterSet:
    lexer = create_lexer(content)
    return pytest.param(lexer, kind, id=kind.value)


# endregion

# region Build identifier or keyword

def test_build_identifier():
    lexer = create_lexer("  lexer")
    token = lexer.get_next_token()

    assert token == Token(TokenKind.Identifier,
                          Location(Position(1, 3), Position(1, 7)),
                          value="lexer")


def test_build_identifier_followed_by_other_char():
    lexer = create_lexer("  lex = Lexer{}")
    token = lexer.get_next_token()

    assert token == Token(TokenKind.Identifier,
                          Location(Position(1, 3), Position(1, 5)),
                          value="lex")


def test_build_too_long_identifier_error():
    lexer = create_lexer("a" * 256)

    with pytest.raises(IdentifierTooLongError):
        lexer.get_next_token()


@pytest.mark.parametrize(
    "lexer, expected",
    (
            create_token_test_case("u16", TokenKind.U16),
            create_token_test_case("u32", TokenKind.U32),
            create_token_test_case("u64", TokenKind.U64),
            create_token_test_case("i16", TokenKind.I16),
            create_token_test_case("i32", TokenKind.I32),
            create_token_test_case("i64", TokenKind.I64),
            create_token_test_case("f32", TokenKind.F32),
            create_token_test_case("bool", TokenKind.Bool),
            create_token_test_case("str", TokenKind.Str)
    )
)
def test_build_builtin_type(lexer: Lexer, expected: Token):
    token = lexer.get_next_token()
    assert token == expected


@pytest.mark.parametrize(
    "lexer, expected",
    (
            create_token_test_case("fn", TokenKind.Fn),
            create_token_test_case("struct", TokenKind.Struct),
            create_token_test_case("enum", TokenKind.Enum),
            create_token_test_case("mut", TokenKind.Mut),
            create_token_test_case("let", TokenKind.Let),
            create_token_test_case("is", TokenKind.Is),
            create_token_test_case("if", TokenKind.If),
            create_token_test_case("while", TokenKind.While),
            create_token_test_case("return", TokenKind.Return),
            create_token_test_case("as", TokenKind.As),
            create_token_test_case("match", TokenKind.Match)
    )
)
def test_build_keyword(lexer: Lexer, expected: Token):
    token = lexer.get_next_token()
    assert token == expected


def test_build_boolean_true():
    lexer = create_lexer("true")
    token = lexer.get_next_token()

    assert token == Token(TokenKind.Boolean,
                          Location(Position(1, 1), Position(1, 4)), True)


def test_build_boolean_false():
    lexer = create_lexer("false")
    token = lexer.get_next_token()

    assert token == Token(TokenKind.Boolean,
                          Location(Position(1, 1), Position(1, 5)), False)


# endregion

# region Build number literals

def test_build_short_integer():
    lexer = create_lexer("3")
    token = lexer.get_next_token()

    assert token == Token(TokenKind.Integer,
                          Location.from_position(Position(1, 1)), value=3)


def test_build_integer():
    lexer = create_lexer("312345123")
    token = lexer.get_next_token()

    assert token == Token(TokenKind.Integer,
                          Location(Position(1, 1), Position(1, 9)),
                          value=312345123)


def test_build_large_integer():
    lexer = create_lexer("9223372036854775807")
    token = lexer.get_next_token()

    assert token.kind == TokenKind.Integer
    assert token.value == 9223372036854775807


def test_build_integer_overflow():
    lexer = create_lexer("18446744073709551616")

    with pytest.raises(IntegerOverflowError):
        lexer.get_next_token()


def test_build_integer_with_leading_zeros_error():
    lexer = create_lexer("00001")

    with pytest.raises(IntegerLeadingZerosError):
        lexer.get_next_token()


def test_build_float():
    lexer = create_lexer("3.14")
    token = lexer.get_next_token()

    assert token.kind == TokenKind.Float
    assert token.location == Location(Position(1, 1), Position(1, 4))
    assert token.value == pytest.approx(3.14, 0.1)


def test_build_float_with_leading_zero():
    lexer = create_lexer("0.0001")
    token = lexer.get_next_token()

    assert token.kind == TokenKind.Float
    assert token.value == pytest.approx(0.0001, 0.1)


def test_build_float_with_last_comma():
    lexer = create_lexer("3.")
    token = lexer.get_next_token()

    assert token.kind == TokenKind.Float
    assert token.location == Location(Position(1, 1), Position(1, 2))
    assert token.value == pytest.approx(3.0, 0.1)


# endregion

# region Build string literals

def test_build_simple_string():
    lexer = create_lexer(""" "Hello World" """)
    token = lexer.get_next_token()

    assert token.kind == TokenKind.String
    assert token.location == Location(Position(1, 2), Position(1, 14))
    assert token.value == "Hello World"


def test_build_string_with_newline():
    lexer = create_lexer(""" "Hello\\nWorld" """)
    token = lexer.get_next_token()

    assert token.kind == TokenKind.String
    assert token.location == Location(Position(1, 2), Position(1, 15))
    assert token.value == "Hello\nWorld"


def test_build_string_with_delimiter():
    lexer = create_lexer(""" "D \\"E\\" L" """)
    token = lexer.get_next_token()

    assert token.kind == TokenKind.String
    assert token.value == "D \"E\" L"


@pytest.mark.parametrize(
    "sequence, escaped",
    (
            (""" "\\\"" """, "\""),
            (""" "\\n" """, "\n"),
            (""" "\\t" """, "\t"),
            (""" "\\\\" """, "\\"),
    )
)
def test_build_string_escaping(sequence: str, escaped: str):
    lexer = create_lexer(sequence)
    token = lexer.get_next_token()

    assert token.value == escaped


def test_build_string_too_long_error():
    lexer = create_lexer("\"" + "a" * 256 + "\"")

    with pytest.raises(StringTooLongError):
        lexer.get_next_token()


def test_build_string_exact_length():
    lexer = create_lexer("\"" + "a" * 128 + "\"")
    token = lexer.get_next_token()

    assert token.value == "a" * 128
    assert len(token.value) == 128
    assert lexer.flags.maximum_string_length == 128


def test_build_string_empty():
    lexer = create_lexer("\"\"")
    token = lexer.get_next_token()

    assert token.kind == TokenKind.String
    assert token.value == ""


def test_build_string_unterminated_error():
    lexer = create_lexer("\"a")

    with pytest.raises(UnterminatedStringError):
        lexer.get_next_token()


@pytest.mark.parametrize(
    "lexer, kind",
    (
            create_kind_test_case(">", TokenKind.Greater),
            create_kind_test_case("<", TokenKind.Less),
            create_kind_test_case("+", TokenKind.Plus),
            create_kind_test_case("*", TokenKind.Multiply)
    )
)
def test_build_single_operator(lexer: Lexer, kind: TokenKind):
    token = lexer.get_next_token()

    assert token.kind == kind
    assert token.location == Location.from_position(Position(1, 1))


@pytest.mark.parametrize(
    "lexer, kind",
    (
            create_kind_test_case("&&", TokenKind.And),
            create_kind_test_case("||", TokenKind.Or)
    )
)
def test_build_double_operator(lexer: Lexer, kind: TokenKind):
    token = lexer.get_next_token()

    assert token.kind == kind
    assert token.location == Location(Position(1, 1), Position(1, 2))


@pytest.mark.parametrize(
    "lexer, kind",
    (
            create_kind_test_case("!", TokenKind.Negate),
            create_kind_test_case("!=", TokenKind.NotEqual),
            create_kind_test_case("=", TokenKind.Assign),
            create_kind_test_case("==", TokenKind.Equal),
            create_kind_test_case("=>", TokenKind.Matcher),
            create_kind_test_case("-", TokenKind.Minus),
            create_kind_test_case("->", TokenKind.ReturnTypeAnnotation)
    )
)
def test_build_multiple_operator(lexer: Lexer, kind: TokenKind):
    token = lexer.get_next_token()

    assert token.kind == kind


@pytest.mark.parametrize(
    "lexer, kind",
    (
            create_kind_test_case("(", TokenKind.ParenthesisOpen),
            create_kind_test_case(")", TokenKind.ParenthesisClose),
            create_kind_test_case("{", TokenKind.BraceOpen),
            create_kind_test_case("}", TokenKind.BraceClose),
            create_kind_test_case(".", TokenKind.FieldAccess),
            create_kind_test_case(",", TokenKind.Period),
            create_kind_test_case(";", TokenKind.Separator),
            create_kind_test_case(":", TokenKind.TypeAnnotation),
            create_kind_test_case("::", TokenKind.VariantAccess)
    )
)
def test_build_punctation(lexer: Lexer, kind: TokenKind):
    token = lexer.get_next_token()

    assert token.kind == kind


def test_build_divide():
    lexer = create_lexer("/")
    token = lexer.get_next_token()

    assert token.kind == TokenKind.Divide


def test_build_comment():
    lexer = create_lexer("// Comment")
    token = lexer.get_next_token()

    assert token.kind == TokenKind.Comment
    assert token.location == Location(Position(1, 1), Position(1, 10))
    assert token.value == " Comment"


def test_build_divide_then_comment():
    lexer = create_lexer("/ // Comment")
    token = lexer.get_next_token()
    token_next = lexer.get_next_token()

    assert token.kind == TokenKind.Divide
    assert token_next.kind == TokenKind.Comment


def test_build_comment_with_leading_slashes():
    lexer = create_lexer("//////")
    token = lexer.get_next_token()

    assert token.kind == TokenKind.Comment
    assert token.value == "////"

# endregion
