from src.common.location import Location
from src.common.position import Position
from src.parser.ast.declaration.enum_declaration import EnumDeclaration
from src.parser.ast.declaration.struct_declaration import StructDeclaration
from src.parser.ast.name import Name
from tests.parser.test_parser import create_parser


def test_parse_enum__empty():
    parser = create_parser("enum First {}", True)

    enum = parser.parse_enum_declaration()
    expected = EnumDeclaration(
        Name("First", Location(Position(1, 6), Position(1, 10))),
        [],
        Location(Position(1, 1), Position(1, 13)),
    )

    assert enum is not None
    assert enum == expected
    assert enum.location == expected.location
    assert enum.name.location == expected.name.location


def test_parse_enum_declaration__with_structs():
    parser = create_parser("enum Elem { struct Button {}; struct Div {}; }",
                           True)

    enum = parser.parse_enum_declaration()
    expected = EnumDeclaration(
        Name("Elem", Location(Position(1, 6), Position(1, 9))),
        [
            StructDeclaration(
                Name("Button", Location(Position(1, 20), Position(1, 25))),
                [],
                Location(Position(1, 13), Position(1, 28))
            ),
            StructDeclaration(
                Name("Div", Location(Position(1, 38), Position(1, 40))),
                [],
                Location(Position(1, 31), Position(1, 43))
            )
        ],
        Location(Position(1, 1), Position(1, 46)),
    )

    assert enum is not None
    assert enum == expected
    assert enum.location == expected.location
    assert enum.name.location == expected.name.location
    assert enum.variants[0].name.location == expected.variants[0].name.location
    assert enum.variants[1].location == expected.variants[1].location


def test_parse_enum_declaration__nested_enum():
    parser = create_parser("enum Elem { enum Button { }; }", True)

    enum = parser.parse_enum_declaration()
    expected = EnumDeclaration(
        Name("Elem", Location(Position(1, 6), Position(1, 9))),
        [
            EnumDeclaration(
                Name("Button", Location(Position(1, 18), Position(1, 23))),
                [],
                Location(Position(1, 13), Position(1, 27))
            )
        ],
        Location(Position(1, 1), Position(1, 30)),
    )

    assert enum is not None
    assert enum == expected
    assert enum.location == expected.location
    assert enum.name.location == expected.name.location
    assert enum.variants[0].location == enum.variants[0].location


def test_parse_enum_declaration__deeply_nested():
    parser = create_parser(
        """
        enum Elem {
            enum Button {
                struct Disabled {};
                struct Active {};
            };
        }
        """,
        True)

    enum = parser.parse_enum_declaration()
    expected = EnumDeclaration(
        Name("Elem", Location(Position(2, 14), Position(2, 17))),
        [
            EnumDeclaration(
                Name("Button", Location(Position(3, 18), Position(3, 23))),
                [
                    StructDeclaration(
                        Name("Disabled",
                             Location(Position(4, 24), Position(4, 31))),
                        [],
                        Location(Position(4, 17), Position(4, 34))
                    ),
                    StructDeclaration(
                        Name("Active",
                             Location(Position(5, 24), Position(5, 29))),
                        [],
                        Location(Position(5, 17), Position(5, 32))
                    )
                ],
                Location(Position(3, 13), Position(6, 13))
            )
        ],
        Location(Position(2, 9), Position(7, 9))
    )

    assert enum is not None
    assert enum == expected
    assert enum.location == expected.location
    assert enum.name.location == expected.name.location
