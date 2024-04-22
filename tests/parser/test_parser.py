import pytest

from src.lexer.lexer import Lexer
from src.lexer.token_kind import TokenKind
from src.parser.ast.access import Access
from src.parser.ast.name import Name
from src.parser.ast.variant_access import VariantAccess
from src.parser.errors import SyntaxExpectedTokenException
from src.parser.parser import Parser
from src.utils.buffer import StreamBuffer


# region Utilities

def create_parser(content: str, consume_first: bool = False) -> Parser:
    buffer = StreamBuffer.from_str(content)
    lexer = Lexer(buffer)
    parser = Parser(lexer)

    # Read first token
    if consume_first:
        parser.consume()

    return parser


# endregion

# region Helper Methods

def test_consume():
    parser = create_parser("1 test", True)

    first = parser.consume()
    second = parser.consume()

    assert first.kind == TokenKind.Integer
    assert second.kind == TokenKind.Identifier


def test_consume_if_matching():
    parser = create_parser("1 test", True)

    token = parser.consume_if(TokenKind.Integer)

    assert token is not None
    assert token.kind == TokenKind.Integer


def test_consume_if_not_matching():
    parser = create_parser("1 test", True)

    token = parser.consume_if(TokenKind.Identifier)

    assert token is None


def test_consume_match_matching():
    parser = create_parser("1 test", True)

    first = parser.consume_match([TokenKind.Identifier, TokenKind.Integer])
    second = parser.consume_match([TokenKind.Identifier, TokenKind.Integer])

    assert first is not None
    assert second is not None
    assert first.kind == TokenKind.Integer
    assert second.kind == TokenKind.Identifier


def test_consume_match_not_matching():
    parser = create_parser("y = 3", True)

    token = parser.consume_match([TokenKind.Fn, TokenKind.Mut])

    assert token is None


def test_expect_exists():
    parser = create_parser("x = 3", True)

    token = parser.expect(TokenKind.Identifier)

    assert token.kind == TokenKind.Identifier


def test_expect_missing():
    parser = create_parser("mut x", True)

    with pytest.raises(SyntaxExpectedTokenException):
        parser.expect(TokenKind.Fn)


def test_expect_conditional_exists():
    parser = create_parser("x + y", True)

    token = parser.expect_conditional(TokenKind.Identifier, False)

    assert token.kind == TokenKind.Identifier


def test_expect_conditional_exists_required():
    parser = create_parser("y = 5", True)

    token = parser.expect_conditional(TokenKind.Identifier, True)

    assert token.kind == TokenKind.Identifier


def test_expect_conditional_missing():
    parser = create_parser("123 * c", True)

    token = parser.expect_conditional(TokenKind.Identifier, False)

    assert token is None


def test_expect_conditional_missing_required():
    parser = create_parser("fn main()", True)

    with pytest.raises(SyntaxExpectedTokenException):
        parser.expect_conditional(TokenKind.Identifier, True)


def test_expect_match_exists():
    parser = create_parser("mut x = 3", True)

    token = parser.expect_match([TokenKind.Mut, TokenKind.Identifier])

    assert token is not None
    assert token.kind == TokenKind.Mut


def test_expect_match_missing():
    parser = create_parser("fn main()", True)

    with pytest.raises(SyntaxExpectedTokenException):
        parser.expect_match([TokenKind.Mut, TokenKind.Identifier])


# endregion

# region Parse Methods

# endregion

# region Parse Functions

def test_parse_parameter_simple():
    parser = create_parser("x: i32", True)

    parameter = parser.parse_parameter()

    assert parameter is not None
    assert parameter.name.identifier == "x"
    assert parameter.type.identifier == "i32"
    assert not parameter.mutable


def test_parse_parameter_mutable():
    parser = create_parser("mut y: Item", True)

    parameter = parser.parse_parameter()

    assert parameter is not None
    assert parameter.name.identifier == "y"
    assert parameter.type.identifier == "Item"
    assert parameter.mutable


def test_parse_parameter_missing_colon():
    parser = create_parser("mut y f32", True)

    with pytest.raises(SyntaxExpectedTokenException):
        parser.parse_parameter()


def test_parse_parameter_missing_identifier_after_mut():
    parser = create_parser("mut : f32", True)

    with pytest.raises(SyntaxExpectedTokenException):
        parser.parse_parameter()


def test_parse_parameter_junk():
    parser = create_parser(": f32", True)

    parameter = parser.parse_parameter()

    assert parameter is None


# endregion

# region Parse Structs

# endregion

# region Parse Enum

# endregion

# region Parse Statements

# endregion

# region Parse Access


def test_parse_access_single():
    parser = create_parser("person", True)

    access = parser.parse_access()

    assert access is not None
    assert isinstance(access, Name)
    assert access.identifier == "person"


def test_parse_access_standard():
    parser = create_parser("person.name", True)

    access = parser.parse_access()

    assert access is not None
    assert isinstance(access, Access)
    assert isinstance(access.name, Name)
    assert isinstance(access.parent, Name)
    assert access.name.identifier == "name"
    assert access.parent.identifier == "person"


def test_parse_access_nested():
    parser = create_parser("person.name.value", True)

    access = parser.parse_access()

    assert access is not None
    assert isinstance(access, Access)
    assert isinstance(access.name, Name)
    assert isinstance(access.parent, Access)
    assert access.name.identifier == "value"
    assert access.parent.name.identifier == "name"
    assert access.parent.parent.identifier == "person"


def test_parse_access_missing_identifier_after_comma():
    parser = create_parser("person.", True)

    with pytest.raises(SyntaxExpectedTokenException):
        parser.parse_access()


def test_parse_variant_access_single():
    parser = create_parser("Entity", True)

    access = parser.parse_variant_access()

    assert access is not None
    assert isinstance(access, Name)
    assert access.identifier == "Entity"


def test_parse_variant_access_standard():
    parser = create_parser("Entity::Item", True)

    variant_access = parser.parse_variant_access()

    assert variant_access is not None
    assert isinstance(variant_access, VariantAccess)
    assert isinstance(variant_access.name, Name)
    assert isinstance(variant_access.parent, Name)
    assert variant_access.name.identifier == "Item"
    assert variant_access.parent.identifier == "Entity"


def test_parse_variant_access_nested():
    parser = create_parser("Entity::Item::Sword", True)

    variant_access = parser.parse_variant_access()

    assert variant_access is not None
    assert isinstance(variant_access, VariantAccess)
    assert isinstance(variant_access.name, Name)
    assert isinstance(variant_access.parent, VariantAccess)
    assert variant_access.name.identifier == "Sword"
    assert variant_access.parent.name.identifier == "Item"
    assert variant_access.parent.parent.identifier == "Entity"


def test_parse_variant_access_missing_identifier_after_comma():
    parser = create_parser("Entity::", True)

    with pytest.raises(SyntaxExpectedTokenException):
        parser.parse_variant_access()


def test_parse_type_builtin():
    parser = create_parser("i32", True)

    typ = parser.parse_type()

    assert typ is not None
    assert isinstance(typ, Name)
    assert typ.identifier == "i32"


def test_parse_type_struct():
    parser = create_parser("Sword", True)

    typ = parser.parse_type()

    assert typ is not None
    assert isinstance(typ, Name)
    assert typ.identifier == "Sword"


def test_parse_type_variant():
    parser = create_parser("Entity::Sword", True)

    typ = parser.parse_type()

    assert typ is not None
    assert isinstance(typ, VariantAccess)
    assert typ.name.identifier == "Sword"
    assert typ.parent.identifier == "Entity"

# endregion

# region Parse Expressions

# endregion


# import pytest
#
# from src.lexer.lexer import Lexer
# from src.parser.errors import SyntaxExpectedTokenException, SyntaxException
# from src.parser.parser import Parser
# from src.utils.buffer import StreamBuffer
#
#
# # region Utils
#
# def create_parser(content: str, consume_first: bool = False) -> Parser:
#     buffer = StreamBuffer.from_str(content)
#     lexer = Lexer(buffer)
#     parser = Parser(lexer)
#
#     # Read first token
#     if consume_first:
#         parser.consume()
#
#     return parser
#
#
# # endregion
#
# # region Parse Function
# def test_parse_function_simple():
#     parser = create_parser("fn main() {}", consume_first=True)
#
#     function = parser.parse_function()
#
#     assert function is not None
#     assert function.name == "main"
#     assert len(function.parameters) == 0
#     assert function.returns is None
#
#
# def test_parse_function_with_parameter():
#     parser = create_parser("fn main(x: i32) {}", consume_first=True)
#
#     function = parser.parse_function()
#
#     assert function is not None
#     assert len(function.parameters) == 1
#     assert function.parameters[0].name == "x"
#     assert function.parameters[0].types == "i32"
#     assert not function.parameters[0].mutable
#
#
# def test_parse_function_with_mutable_parameter():
#     parser = create_parser("fn main(mut x: i32) {}", consume_first=True)
#
#     function = parser.parse_function()
#
#     assert function is not None
#     assert len(function.parameters) == 1
#     assert function.parameters[0].mutable
#
#
# def test_parse_function_with_many_parameters():
#     parser = create_parser("fn main(x: i32, mut y: f32, c: str) {}",
#                            consume_first=True)
#
#     function = parser.parse_function()
#
#     assert function is not None
#     assert len(function.parameters) == 3
#     assert function.parameters[0].name == "x"
#     assert function.parameters[2].name == "c"
#     assert function.parameters[2].types == "str"
#
#
# def test_parse_function_with_return_type():
#     parser = create_parser("fn main() -> i32 {}", consume_first=True)
#
#     function = parser.parse_function()
#
#     assert function is not None
#     assert function.returns == "i32"
#
#
# def test_parse_function_missing_parenthesis():
#     parser = create_parser("fn main x: i32) {}", consume_first=True)
#
#     with pytest.raises(SyntaxExpectedTokenException):
#         parser.parse_function()
#
#
# def test_parse_parameters():
#     parser = create_parser("x: i32", consume_first=True)
#
#     parameters = parser.parse_parameters()
#     assert len(parameters) == 1
#
#
# def test_parse_parameters_multiple():
#     parser = create_parser("x: i32, mut y: f32", consume_first=True)
#
#     parameters = parser.parse_parameters()
#
#     assert len(parameters) == 2
#
#
# def test_parse_parameters_expected_parameter_after_comma():
#     parser = create_parser("x: i32, ", consume_first=True)
#
#     with pytest.raises(SyntaxException):
#         parameters = parser.parse_parameters()
#
#
# def test_parse_parameter():
#     parser = create_parser("x: i32", consume_first=True)
#
#     parameter = parser.parse_parameter()
#
#     assert parameter is not None
#     assert parameter.name == "x"
#     assert parameter.types == "i32"
#     assert not parameter.mutable
#
#
# def test_parse_parameter_mutable():
#     parser = create_parser("mut x: i32", consume_first=True)
#
#     parameter = parser.parse_parameter()
#
#     assert parameter is not None
#     assert parameter.mutable
#
#
# def test_parse_parameter_junk():
#     parser = create_parser("()", consume_first=True)
#
#     parameter = parser.parse_parameter()
#
#     assert parameter is None
#
#
# def test_parse_parameter_missing_identifier():
#     parser = create_parser("mut ()", consume_first=True)
#
#     with pytest.raises(SyntaxExpectedTokenException):
#         parser.parse_parameter()
#
#
# def test_parse_parameter_missing_colon():
#     parser = create_parser("x i32", consume_first=True)
#
#     with pytest.raises(SyntaxExpectedTokenException):
#         parser.parse_parameter()
#
# # endregion
