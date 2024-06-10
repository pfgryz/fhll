import pytest

from src.interpreter.errors import VariableRedeclarationError, InferenceError, \
    EmptyVariableError, MissingOperationImplementationError, \
    UndefinedVariableError, UndefinedStructError, UndefinedFieldError, \
    AssignmentTooConstantVariable, InvalidTypeError
from src.interpreter.operations.builtin_operations_registry import \
    BuiltinOperationsRegistry
from src.interpreter.visitors.semantic.dynamic_type_validator import \
    DynamicTypeValidator
from src.parser.ast.module import Module
from tests.interpreter.helpers import load_module
from tests.interpreter.visitors.semantic.test_fn_call_validator import \
    get_functions_registry
from tests.interpreter.visitors.semantic.test_new_struct_validator import \
    get_types_registry


def get_dynamic_type_validator(module: Module) -> DynamicTypeValidator:
    return DynamicTypeValidator(
        get_types_registry(module),
        get_functions_registry(module),
        BuiltinOperationsRegistry()
    )


def test_dynamic_type_validator__variable_declaration__positive():
    module = load_module("""
    fn main() {
        let z: i32 = 3;
        {
            let z: i32 = 4;
        }
    }""")

    dynamic_type_validator = get_dynamic_type_validator(module)
    dynamic_type_validator.visit(module)


def test_dynamic_type_validator__variable_declaration__redeclaration():
    module = load_module("""
    fn main() {
        let z: i32 = 3;
        let z: i32 = 4;
    }""")

    dynamic_type_validator = get_dynamic_type_validator(module)

    with pytest.raises(VariableRedeclarationError):
        dynamic_type_validator.visit(module)


def test_dynamic_type_validator__variable_declaration__inference():
    module = load_module("""
    fn main() {
        let z;
    }""")

    dynamic_type_validator = get_dynamic_type_validator(module)

    with pytest.raises(InferenceError):
        dynamic_type_validator.visit(module)


def test_dynamic_type_validator__variable_declaration__empty():
    module = load_module("""
    fn main() {
        let z: i32;
    }""")

    dynamic_type_validator = get_dynamic_type_validator(module)

    with pytest.raises(EmptyVariableError):
        dynamic_type_validator.visit(module)


def test_dynamic_type_validator__variable_declaration__cannot_cast():
    module = load_module("""
    struct Item {}
    
    fn main() {
        let z: Item = 3;
    }""")

    dynamic_type_validator = get_dynamic_type_validator(module)

    with pytest.raises(MissingOperationImplementationError):
        dynamic_type_validator.visit(module)


def test_dynamic_type_validator__assignment__constant():
    module = load_module("""
    fn main() {
        let z: i32 = 3;
        z = 4;
    }""")

    dynamic_type_validator = get_dynamic_type_validator(module)

    with pytest.raises(AssignmentTooConstantVariable):
        dynamic_type_validator.visit(module)


def test_dynamic_type_validator__assignment__undefined_struct():
    module = load_module("""
    struct Item { amount: i32; }
    
    fn main() {
        let item: Item = Item {};
        item.amount.inner = 4;
    }""")

    dynamic_type_validator = get_dynamic_type_validator(module)

    with pytest.raises(UndefinedStructError):
        dynamic_type_validator.visit(module)


def test_dynamic_type_validator__assignment__undefined_field():
    module = load_module("""
    struct Item { }
    
    fn main() {
        let item: Item = Item {};
        item.amount = 4;
    }""")

    dynamic_type_validator = get_dynamic_type_validator(module)

    with pytest.raises(UndefinedFieldError):
        dynamic_type_validator.visit(module)


def test_dynamic_type_validator__assignment__undefined_variable():
    module = load_module("""
    fn main() {
        z = 4;
    }""")

    dynamic_type_validator = get_dynamic_type_validator(module)

    with pytest.raises(UndefinedVariableError):
        dynamic_type_validator.visit(module)


def test_dynamic_type_validator__new_struct__type_missmatch():
    module = load_module("""
    struct Item { amount: i32; }
    fn main() {
        let item = Item { amount = "test"; };
    }""")

    dynamic_type_validator = get_dynamic_type_validator(module)

    with pytest.raises(InvalidTypeError):
        dynamic_type_validator.visit(module)


def test_dynamic_type_validator__matcher__inside():
    module = load_module("""
    struct Item { amount: i32; }
    fn main() {
        let x = 3;
        match (x) {
            i32 proper => {
            
            };
            f32 y => {
                z = 4;
            };
        }
    }""")

    dynamic_type_validator = get_dynamic_type_validator(module)

    with pytest.raises(UndefinedVariableError):
        dynamic_type_validator.visit(module)


def test_dynamic_type_validator__return_statement__type():
    module = load_module("""
    fn main() -> f32 {
        return 3;
    }
    """)

    dynamic_type_validator = get_dynamic_type_validator(module)

    with pytest.raises(InvalidTypeError):
        dynamic_type_validator.visit(module)


def test_dynamic_type_validator__fn_call__type():
    module = load_module("""
    fn other(x: i32) {}
    
    fn main() -> f32 {
        other(4.5);
        return 3.4;
    }
    """)

    dynamic_type_validator = get_dynamic_type_validator(module)

    with pytest.raises(InvalidTypeError):
        dynamic_type_validator.visit(module)
