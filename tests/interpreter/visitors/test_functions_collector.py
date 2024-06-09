import pytest

from src.interpreter.errors import ParameterRedeclarationError, \
    UnknownTypeError
from src.interpreter.types.typename import TypeName
from src.interpreter.visitors.functions_collector import FunctionsCollector
from src.interpreter.visitors.types_collector import TypesCollector
from tests.interpreter.visitors.helpers import load_module


def test_functions_collector__simple():
    module = load_module("""
    fn main(x: i32, mut y: i32) -> i32 {
        return x * x;
    }
    
    fn boot() {
        main(3, 4);
    }
    """)

    types_collector = TypesCollector()
    types_collector.visit(module)
    types_registry = types_collector.types_registry

    functions_collector = FunctionsCollector(types_registry)
    functions_collector.visit(module)
    functions_registry = functions_collector.functions_registry

    boot = functions_registry.get_function("boot")
    main = functions_registry.get_function("main")
    assert boot is not None
    assert boot.return_type is None
    assert main is not None
    assert main.name == "main"
    assert main.return_type == TypeName.parse("i32")
    assert main.parameters.get("x") == (False, TypeName.parse("i32"))
    assert main.parameters.get("y") == (True, TypeName.parse("i32"))


def test_functions_collector__parameter_redeclaration():
    module = load_module("""
    fn main(x: i32, mut x: i32) -> i32 {
        return x * x;
    }
    """)

    types_collector = TypesCollector()
    types_collector.visit(module)
    types_registry = types_collector.types_registry

    functions_collector = FunctionsCollector(types_registry)

    with pytest.raises(ParameterRedeclarationError):
        functions_collector.visit(module)


def test_functions_collector__unknown_return_type():
    module = load_module("""
    fn main(x: i32) -> f32 {
        return x * x;
    }
    """)

    types_collector = TypesCollector()
    types_collector.visit(module)
    types_registry = types_collector.types_registry

    functions_collector = FunctionsCollector(types_registry)

    with pytest.raises(UnknownTypeError):
        functions_collector.visit(module)


def test_functions_collector__unknown_parameter_type():
    module = load_module("""
    fn main(x: f32) -> i32 {
        return x * x;
    }
    """)

    types_collector = TypesCollector()
    types_collector.visit(module)
    types_registry = types_collector.types_registry

    functions_collector = FunctionsCollector(types_registry)

    with pytest.raises(UnknownTypeError):
        functions_collector.visit(module)
