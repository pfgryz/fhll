import pytest

from src.common.position import Position
from src.interpreter.errors import FunctionRedeclarationError
from src.interpreter.functions.functions_registry import FunctionsRegistry
from src.interpreter.functions.ifunction_implementation import \
    IFunctionImplementation


def test_functions_registry__empty():
    functions_registry = FunctionsRegistry()

    assert functions_registry.get_function("main") is None


def test_function_registry__registering():
    functions_registry = FunctionsRegistry()

    functions_registry.register_function(
        "main",
        IFunctionImplementation(),
        Position(1, 1)
    )
    assert functions_registry.get_function("main") is not None
    assert "main" in functions_registry.functions


def test_function_registry__registering_twice():
    functions_registry = FunctionsRegistry()

    functions_registry.register_function(
        "main",
        IFunctionImplementation(),
        Position(1, 1)
    )

    with pytest.raises(FunctionRedeclarationError):
        functions_registry.register_function(
            "main",
            IFunctionImplementation(),
            Position(1, 1)
        )