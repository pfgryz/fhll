import pytest

from src.interpreter.errors import UndefinedStructError, \
    AssignmentToUndefinedFieldError, InvalidFieldAssignmentError
from src.interpreter.types.types_registry import TypesRegistry
from src.interpreter.visitors.semantic.new_struct_validator import \
    NewStructValidator
from src.interpreter.visitors.types_collector import TypesCollector
from src.parser.ast.module import Module
from tests.interpreter.helpers import load_module


def get_types_registry(module: Module) -> TypesRegistry:
    types_collector = TypesCollector()
    types_collector.visit(module)
    return types_collector.types_registry


def test_new_struct_validator__simple():
    module = load_module("""
    struct Test {
        x: i32;
    }
    
    fn main() {
         x = Test { x = 3; };
    }
    """)

    new_struct_validator = NewStructValidator(
        get_types_registry(
            module
        )
    )
    new_struct_validator.visit(module)


def test_new_struct_validator__missing_struct():
    module = load_module("""
    struct Test {
        x: i32;
    }

    fn main() {
         x = Window { name = "Main Window"; };
    }
    """)

    new_struct_validator = NewStructValidator(
        get_types_registry(
            module
        )
    )

    with pytest.raises(UndefinedStructError):
        new_struct_validator.visit(module)


def test_new_struct_validator__undefined_field():
    module = load_module("""
    struct Button {
        id: i32;
    }

    fn main() {
         x = Button { description = "Main Window"; };
    }
    """)

    new_struct_validator = NewStructValidator(
        get_types_registry(
            module
        )
    )

    with pytest.raises(AssignmentToUndefinedFieldError):
        new_struct_validator.visit(module)



def test_new_struct_validator__illegal_field_name():
    module = load_module("""
    struct Button {
        id: i32;
    }

    fn main() {
         x = Button { description.id = 3; };
    }
    """)

    new_struct_validator = NewStructValidator(
        get_types_registry(
            module
        )
    )

    with pytest.raises(InvalidFieldAssignmentError):
        new_struct_validator.visit(module)
