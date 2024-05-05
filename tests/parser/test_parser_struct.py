import pytest

from src.common.location import Location
from src.common.position import Position
from src.parser.ast.declaration.field_declaration import FieldDeclaration
from src.parser.ast.declaration.struct_declaration import StructDeclaration
from src.parser.ast.name import Name
from src.parser.errors import SemicolonExpectedError, ColonExpectedError
from tests.parser.test_parser import create_parser


# region Parse Struct

def test_parse_struct__empty():
    parser = create_parser("struct Item {}", True)

    struct = parser.parse_struct_declaration()
    expected = StructDeclaration(
        Name("Item", Location(Position(1, 8), Position(1, 11))),
        [],
        Location(Position(1, 1), Position(1, 14))
    )

    assert struct is not None
    assert struct == expected
    assert struct.location == expected.location
    assert struct.name.location == expected.name.location


def test_parse_struct__fields():
    parser = create_parser("struct Item { value: i32; }", True)

    struct = parser.parse_struct_declaration()
    expected = StructDeclaration(
        Name("Item", Location(Position(1, 8), Position(1, 11))),
        [
            FieldDeclaration(
                Name("value", Location(Position(1, 15), Position(1, 19))),
                Name("i32", Location(Position(1, 22), Position(1, 24))),
                Location(Position(1, 15), Position(1, 24))
            )
        ],
        Location(Position(1, 1), Position(1, 27))
    )

    assert struct is not None
    assert struct == expected
    assert struct.location == expected.location


# endregion

# region Parse Field

def test_parse_field_declaration():
    parser = create_parser("value: i32;", True)

    field = parser.parse_field_declaration()
    expected = FieldDeclaration(
        Name("value", Location(Position(1, 1), Position(1, 5))),
        Name("i32", Location(Position(1, 8), Position(1, 10))),
        Location(Position(1, 1), Position(1, 10))
    )

    assert field is not None
    assert field == expected
    assert field.location == expected.location


def test_parse_field_declaration__colon_expected():
    parser = create_parser("value i32", True)

    with pytest.raises(ColonExpectedError):
        parser.parse_field_declaration()


def test_parse_field_declaration__semicolon_expected():
    parser = create_parser("value: i32", True)

    with pytest.raises(SemicolonExpectedError):
        parser.parse_field_declaration()

# endregion
