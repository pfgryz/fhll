import pytest

from src.interpreter.errors import UndefinedFunctionCallError, \
    TooFewArgumentsError, TooManyArgumentsError
from src.interpreter.visitors.functions_collector import FunctionsCollector
from src.interpreter.visitors.semantic.fn_call_validator import FnCallValidator
from src.interpreter.visitors.types_collector import TypesCollector
from src.parser.ast.module import Module
from tests.interpreter.visitors.helpers import load_module


def get_functions_registry(module: Module):
    types_collector = TypesCollector()
    types_collector.visit(module)
    types_registry = types_collector.types_registry

    functions_collector = FunctionsCollector(types_registry)
    functions_collector.visit(module)
    return functions_collector.functions_registry


def test_fn_call_visitor__simple():
    module = load_module("""
    struct List {}
    enum UI {
        struct Window {};
        enum Components {
            struct Btn {};
            struct Input {};
        };
    }
    
    fn render_ui(window: UI::Window) {
        let x = 3 * 4;
        x = !4;
        let y = List {};
        return y;
    }
    
    fn main(x: i32, l: List) {
        render_ui(UI::Window {});
        
        if (x == x as i32) {
            x = -x + 1;
            boot();
        } 
        else {
            boot();
        }
        
        while (boot() is i32) {
            boot();
        }
        
        match (x) {
            i32 x => {
                boot();
            };
        }
    }
    
    fn boot() {
        main(1, List {});
    }
    """)

    fn_call_validator = FnCallValidator(
        get_functions_registry(module)
    )
    fn_call_validator.visit(module)


def test_fn_call_visitor__undefined_function():
    module = load_module("""
    fn boot() {
        let x = 3;
        main(x);
    }
    """)

    fn_call_validator = FnCallValidator(
        get_functions_registry(module)
    )
    with pytest.raises(UndefinedFunctionCallError):
        fn_call_validator.visit(module)


def test_fn_call_visitor__too_few_arguments():
    module = load_module("""
    fn boot() {
        let x = 3;
        main(x);
    }
    
    fn main(x: i32, y: i32) {
    
    }
    """)

    fn_call_validator = FnCallValidator(
        get_functions_registry(module)
    )
    with pytest.raises(TooFewArgumentsError):
        fn_call_validator.visit(module)


def test_fn_call_visitor__too_many_arguments():
    module = load_module("""
    fn boot() {
        let x = 3;
        main(x, x, x);
    }

    fn main(x: i32, y: i32) {

    }
    """)

    fn_call_validator = FnCallValidator(
        get_functions_registry(module)
    )
    with pytest.raises(TooManyArgumentsError):
        fn_call_validator.visit(module)
