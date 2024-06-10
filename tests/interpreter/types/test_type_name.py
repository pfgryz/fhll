from src.interpreter.types.typename import TypeName


def test_type_name__is_derived_from():
    item = TypeName.parse("Item")
    tool = TypeName.parse("Item::Tool")

    assert tool.is_derived_from(item)
    assert not item.is_derived_from(tool)


def test_type_name__is_base_of():
    item = TypeName.parse("Item")
    tool = TypeName.parse("Item::Tool")

    assert item.is_base_of(tool)
    assert not tool.is_base_of(item)
