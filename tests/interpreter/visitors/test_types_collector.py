import pytest

from src.interpreter.errors import FieldRedeclarationError, InternalError, \
    TypeRedeclarationError, UnknownTypeError
from src.interpreter.types.typename import TypeName
from src.interpreter.visitors.types_collector import TypesCollector
from tests.interpreter.helpers import load_module


# region Structs

def test_types_collector__struct():
    module = load_module("""
    struct Rectangle {
        width: i32;
    }
    """)

    collector = TypesCollector()
    collector.visit(module)
    types_registry = collector.types_registry

    assert types_registry.get_type(TypeName.parse("Rectangle")) is not None
    assert types_registry.get_type(TypeName.parse("Square")) is None
    assert types_registry.get_struct(TypeName.parse("Rectangle")) is not None


def test_types_collector__field_redeclaration():
    module = load_module("""
    struct Rectangle {
        width: i32;
        width: i32;
    }
    """)

    collector = TypesCollector()

    with pytest.raises(FieldRedeclarationError):
        collector.visit(module)


# endregion

# region Enums

def test_types_collector__enum():
    module = load_module("""
    enum Shape {
        struct Rectangle {};
        enum Other {
            struct Circle {};
            struct Square {};
        };  
    }
    """)

    collector = TypesCollector()
    collector.visit(module)
    types_registry = collector.types_registry

    assert types_registry.get_type(
        TypeName.parse("Shape::Rectangle")) is not None
    assert types_registry.get_struct(
        TypeName.parse("Shape::Other::Circle")) is not None
    assert types_registry.get_enum(TypeName.parse("Shape::Other")) is not None


def test_types_collector__enum_prepared():
    module = load_module("enum Hack {} struct X { width: i32; }")
    module.enum_declarations[0].variants.append(
        module.struct_declarations[0].fields[0]
    )

    collector = TypesCollector()
    with pytest.raises(InternalError):
        collector.visit(module)


# endregion

# region Resolving

def test_types_collector__resolve_cyclic():
    module = load_module("""
    enum List {
        struct Empty {};
        struct Something {
            next: List;
            value: i32;
        };
    }
    """)

    collector = TypesCollector()
    collector.visit(module)
    types_registry = collector.types_registry

    something = types_registry.get_struct(TypeName.parse("List::Something"))
    assert something is not None
    assert something.fields.get("next") is not None
    assert something.fields.get("next").as_type() == TypeName.parse("List")


def test_types_collector__double_type():
    module = load_module("""
    struct Rectangle {}
    struct Rectangle {}
    """)

    collector = TypesCollector()
    with pytest.raises(TypeRedeclarationError):
        collector.visit(module)


def test_types_collector__unknown_type():
    module = load_module("""
    struct Rectangle { width: Size; }
    """)

    collector = TypesCollector()
    with pytest.raises(UnknownTypeError):
        collector.visit(module)

# endregion
