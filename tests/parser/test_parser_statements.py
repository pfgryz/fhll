import pytest

from src.common.location import Location
from src.common.position import Position
from src.parser.ast.constant import Constant
from src.parser.ast.name import Name
from src.parser.ast.statements.new_struct_statement import NewStruct
from src.parser.ast.statements.variable_declaration import VariableDeclaration
from src.parser.errors import NameExpectedError, TypeExpectedError, \
    ExpressionExpectedError, LetKeywordExpectedError
from tests.parser.test_parser import create_parser


# region Parse Declaration

def test_parse_declaration__empty():
    parser = create_parser("let a", True)

    declaration = parser.parse_declaration()
    expected = VariableDeclaration(
        Name("a", Location(Position(1, 5), Position(1, 5))),
        False,
        None,
        None,
        Location(Position(1, 1), Position(1, 5))
    )

    assert declaration is not None
    assert declaration == expected
    assert declaration.location == expected.location
    assert declaration.name.location == expected.name.location


def test_parse_declaration__mutable():
    parser = create_parser("mut let b", True)

    declaration = parser.parse_declaration()
    expected = VariableDeclaration(
        Name("b", Location(Position(1, 9), Position(1, 9))),
        True,
        None,
        None,
        Location(Position(1, 1), Position(1, 9))
    )

    assert declaration is not None
    assert declaration == expected
    assert declaration.location == expected.location


def test_parse_declaration__value():
    parser = create_parser("let c = 3", True)

    declaration = parser.parse_declaration()
    expected = VariableDeclaration(
        Name("c", Location(Position(1, 5), Position(1, 5))),
        False,
        None,
        Constant(
            3,
            Location(Position(1, 9), Position(1, 9))
        ),
        Location(Position(1, 1), Position(1, 9))
    )

    assert declaration is not None
    assert declaration == expected
    assert declaration.location == expected.location


def test_parse_declaration__type():
    parser = create_parser("let d: i32", True)

    declaration = parser.parse_declaration()
    expected = VariableDeclaration(
        Name("d", Location(Position(1, 5), Position(1, 5))),
        False,
        Name("i32", Location(Position(1, 8), Position(1, 10))),
        None,
        Location(Position(1, 1), Position(1, 10))
    )

    assert declaration is not None
    assert declaration == expected
    assert declaration.location == expected.location


# @TODO: Will fail until parse_expression is not fixed
def test_parse_declaration__complex():
    parser = create_parser("mut let e: Item = Item {}", True)

    declaration = parser.parse_declaration()
    expected = VariableDeclaration(
        Name("e", Location(Position(1, 9), Position(1, 9))),
        False,
        Name("Item", Location(Position(1, 12), Position(1, 15))),
        NewStruct(
            Name("Item", Location(Position(1, 19), Position(1, 22))),
            [],
            Location(Position(1, 19), Position(1, 25))
        ),
        Location(Position(1, 1), Position(1, 25))
    )

    assert declaration is not None
    assert declaration == expected


def test_parse_declaration__name_expected():
    parser = create_parser("let =", True)

    with pytest.raises(NameExpectedError):
        parser.parse_declaration()


def test_parse_declaration__let_expected():
    parser = create_parser("mut e: Item = Item {}", True)

    with pytest.raises(LetKeywordExpectedError):
        parser.parse_declaration()


def test_parse_declaration__type_expected():
    parser = create_parser("let e: = Item {}", True)

    with pytest.raises(TypeExpectedError):
        parser.parse_declaration()


def test_parse_declaration__expression_expected():
    parser = create_parser("mut let e: Item = ", True)

    with pytest.raises(ExpressionExpectedError):
        parser.parse_declaration()

# endregion
