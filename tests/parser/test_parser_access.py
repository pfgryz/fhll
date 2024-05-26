import pytest

from src.common.location import Location
from src.common.position import Position
from src.parser.ast.access import Access
from src.parser.ast.name import Name
from src.parser.ast.variant_access import VariantAccess
from src.parser.errors import NameExpectedError
from tests.parser.test_parser import create_parser


# region Parse Name

def test_parse_name():
    parser = create_parser("test", True)

    name = parser.parse_name()
    expected = Name("test", Location(Position(1, 1), Position(1, 4)))

    assert name is not None
    assert name == expected
    assert name.location == expected.location


# endregion

# region Parse Access

def test_parse_access__single_name():
    parser = create_parser("single", True)

    access = parser.parse_access()
    expected = Name("single", Location(Position(1, 1), Position(1, 6)))

    assert access is not None
    assert access == expected
    assert access.location == expected.location


def test_parse_access__nested():
    parser = create_parser("nested.name", True)

    access = parser.parse_access()
    expected = Access(
        Name(
            identifier="name",
            location=Location(Position(1, 8), Position(1, 11))
        ),
        Name(
            identifier="nested",
            location=Location(Position(1, 1), Position(1, 6))
        ),
        Location(Position(1, 1), Position(1, 11))
    )

    assert access is not None
    assert access == expected
    assert access.location == expected.location
    assert access.name.location == expected.name.location


def test_parse_access__deeply_nested():
    parser = create_parser("deeply.nested.name", True)

    access = parser.parse_access()
    expected = Access(
        Name(
            identifier="name",
            location=Location(Position(1, 15), Position(1, 18))
        ),
        Access(
            Name(
                identifier="nested",
                location=Location(Position(1, 8), Position(1, 13))
            ),
            Name(
                identifier="deeply",
                location=Location(Position(1, 1), Position(1, 6))
            ),
            Location(Position(1, 1), Position(1, 13))
        ),
        Location(Position(1, 1), Position(1, 18))
    )

    assert access is not None
    assert access == expected
    assert access.location == expected.location


def test_parse_access__name_expected_after_period():
    parser = create_parser("person.", True)

    with pytest.raises(NameExpectedError):
        parser.parse_access()


# endregion

# region Parse Variant Access

def test_parse_variant_access__single_name():
    parser = create_parser("Entity", True)

    access = parser.parse_variant_access()
    expected = Name("Entity", Location(Position(1, 1), Position(1, 6)))

    assert access is not None
    assert access == expected


def test_parse_variant_access__nested():
    parser = create_parser("Entity::Item", True)

    variant_access = parser.parse_variant_access()
    expected = VariantAccess(
        Name(
            identifier="Item",
            location=Location(Position(1, 9), Position(1, 12))
        ),
        Name(
            identifier="Entity",
            location=Location(Position(1, 1), Position(1, 6))
        ),
        Location(Position(1, 1), Position(1, 12))
    )

    assert variant_access is not None
    assert variant_access == expected
    assert variant_access.location == expected.location


def test_parse_variant_access__deeply_nested():
    parser = create_parser("Entity::Item::Sword", True)

    variant_access = parser.parse_variant_access()
    expected = VariantAccess(
        Name(
            identifier="Sword",
            location=Location(Position(1, 15), Position(1, 19))
        ),
        VariantAccess(
            Name("Item", Location(Position(1, 9), Position(1, 12))),
            Name("Entity", Location(Position(1, 1), Position(1, 6))),
            Location(Position(1, 1), Position(1, 12))
        ),
        Location(Position(1, 1), Position(1, 19))
    )

    assert variant_access is not None
    assert variant_access == expected
    assert variant_access.location == expected.location


def test_parse_variant_access__name_expected_after_period():
    parser = create_parser("Entity::", True)

    with pytest.raises(NameExpectedError):
        parser.parse_variant_access()


# endregion

# region Parse Type

def test_parse_type__builtin():
    parser = create_parser("i32", True)

    builtin_type = parser.parse_type()
    expected = Name("i32", Location(Position(1, 1), Position(1, 3)))

    assert builtin_type is not None
    assert builtin_type == expected
    assert builtin_type.location == expected.location


def test_parse_type__name():
    parser = create_parser("Sword", True)

    name = parser.parse_type()
    expected = Name("Sword", Location(Position(1, 1), Position(1, 5)))

    assert name is not None
    assert name == expected
    assert name.location == expected.location


def test_parse_type__variant():
    parser = create_parser("Entity::Sword", True)

    variant = parser.parse_type()
    expected = VariantAccess(
        Name(
            identifier="Sword",
            location=Location(Position(1, 9), Position(1, 13))
        ),
        Name(
            identifier="Entity",
            location=Location(Position(1, 1), Position(1, 6))
        ),
        Location(Position(1, 1), Position(1, 13))
    )

    assert variant is not None
    assert variant == expected
    assert variant.location == expected.location

# endregion
