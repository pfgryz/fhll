import pytest

from src.interpreter.errors import MissingReturnStatementError, \
    MissingReturnValueError, ReturnValueInVoidFunctionError
from src.interpreter.visitors.semantic.return_validator import ReturnValidator
from tests.interpreter.helpers import load_module


def test_return_validator__simple():
    module = load_module("""
    fn main() {
        return;
    }""")

    return_validator = ReturnValidator()
    return_validator.visit(module)


def test_return_validator__nested():
    module = load_module("""
    fn main() {
        {
            return;
        }
    }""")

    return_validator = ReturnValidator()
    return_validator.visit(module)


def test_return_validator__if_statement():
    module = load_module("""
    fn main() {
        if (x) {
            return;
        } 
        else {
            return;
        }
    }""")

    return_validator = ReturnValidator()
    return_validator.visit(module)


def test_return_validator__match_statement():
    module = load_module("""
    fn main() {
        match (x) {
            _ y => { return; };
        }
    }""")

    return_validator = ReturnValidator()
    return_validator.visit(module)


def test_return_validator__missing_in_block():
    module = load_module("""
    fn main() -> i32 {
    }""")

    return_validator = ReturnValidator()

    with pytest.raises(MissingReturnStatementError):
        return_validator.visit(module)


def test_return_validator__single_if_return():
    module = load_module("""
    fn main() -> i32 {
        if (x) {
            return 3;
        }
    }""")

    return_validator = ReturnValidator()

    with pytest.raises(MissingReturnStatementError):
        return_validator.visit(module)


def test_return_validator__single_else_return():
    module = load_module("""
    fn main() -> i32 {
        if (x) {
        }
        else {
            return 3;
        }
    }""")

    return_validator = ReturnValidator()

    with pytest.raises(MissingReturnStatementError):
        return_validator.visit(module)


def test_return_validator__no_default_matcher():
    module = load_module("""
    fn main() -> i32 {
        match (x) {
            i32 y => { return 3; };
        }
    }""")

    return_validator = ReturnValidator()

    with pytest.raises(MissingReturnStatementError):
        return_validator.visit(module)


def test_return_validator__no_all_matchers():
    module = load_module("""
    fn main() -> i32 {
        match (x) {
            i32 y => { return 3; };
            i32 z => {};
        }
    }""")

    return_validator = ReturnValidator()

    with pytest.raises(MissingReturnStatementError):
        return_validator.visit(module)


def test_return_validator__no_return_value():
    module = load_module("""
    fn main() -> i32 {
        return;
    }""")

    return_validator = ReturnValidator()

    with pytest.raises(MissingReturnValueError):
        return_validator.visit(module)


def test_return_validator__return_value_in_void():
    module = load_module("""
    fn main() {
        return 3;
    }""")

    return_validator = ReturnValidator()

    with pytest.raises(ReturnValueInVoidFunctionError):
        return_validator.visit(module)
