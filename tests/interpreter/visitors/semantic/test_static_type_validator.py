import pytest

from src.interpreter.errors import UnknownTypeError
from src.interpreter.visitors.semantic.static_type_validator import \
    StaticTypeValidator
from tests.interpreter.helpers import load_module
from tests.interpreter.visitors.semantic.test_new_struct_validator import \
    get_types_registry


def test_static_type_validator__variable_declaration():
    module = load_module("""
    struct Item {}
    
    fn main() {
        mut let z: bool = (3 as i32) is bool;
        match (z) {
            i32 x => {};
        }
        let other = Item{};
    }""")

    static_type_validator = StaticTypeValidator(
        get_types_registry(module)
    )
    static_type_validator.visit(module)


def test_static_type_validator__variable_declaration():
    module = load_module("""
    fn main() {
        mut let z: Item;
    }""")

    static_type_validator = StaticTypeValidator(
        get_types_registry(module)
    )

    with pytest.raises(UnknownTypeError):
        static_type_validator.visit(module)


def test_static_type_validator__cast():
    module = load_module("""
    fn main() {
        mut let z = 3 as Item;
    }""")

    static_type_validator = StaticTypeValidator(
        get_types_registry(module)
    )

    with pytest.raises(UnknownTypeError):
        static_type_validator.visit(module)


def test_static_type_validator__is_compare():
    module = load_module("""
    fn main() {
        mut let z = 3 is Item;
    }""")

    static_type_validator = StaticTypeValidator(
        get_types_registry(module)
    )

    with pytest.raises(UnknownTypeError):
        static_type_validator.visit(module)


def test_static_type_validator__match_statement():
    module = load_module("""
    fn main() {
        match(x) {
            Item y => {};
        }
    }""")

    static_type_validator = StaticTypeValidator(
        get_types_registry(module)
    )

    with pytest.raises(UnknownTypeError):
        static_type_validator.visit(module)


def test_static_type_validator__new_struct():
    module = load_module("""
    fn main() {
        let window = Window {};
    }""")

    static_type_validator = StaticTypeValidator(
        get_types_registry(module)
    )

    with pytest.raises(UnknownTypeError):
        static_type_validator.visit(module)
