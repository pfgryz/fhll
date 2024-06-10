import pytest

from src.interpreter.types.field_access import FieldAccess


def test_field_access__to_name():
    field_access = FieldAccess.parse("Item.name")

    assert field_access.to_name() == "Item"


@pytest.mark.parametrize(
    "raw, expected",
    (
            ("Item", False),
            ("Item.name", True),
            ("Item.name.str", True)
    )
)
def test_field_access__is_access(raw: str, expected: bool):
    field_access = FieldAccess.parse(raw)

    assert field_access.is_access() == expected
