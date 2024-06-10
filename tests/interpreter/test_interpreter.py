from src.interpreter.interpreter import Interpreter
from src.interpreter.types.typename import TypeName
from tests.interpreter.helpers import load_module


def test_interpreter__empty_main():
    module = load_module("""
    fn main() -> i32 {
        return 3;
    }""")

    interpreter = Interpreter()
    interpreter.visit(module)
    result = interpreter.run("main")

    assert result.value == 3
    assert result.type_name == TypeName.parse("i32")


def test_interpreter__variable_declaration():
    module = load_module("""
    fn main() -> i32 {
        let z: i32 = 32;
        return z;
    }""")

    interpreter = Interpreter()
    interpreter.visit(module)
    result = interpreter.run("main")

    assert result.value == 32
    assert result.type_name == TypeName.parse("i32")


def test_interpreter__variable_declaration_no_value():
    module = load_module("""
    fn main() -> i32 {
        let z: i32;
        return z;
    }""")

    interpreter = Interpreter()
    interpreter.visit(module)
    result = interpreter.run("main")

    assert result.value == 0
    assert result.type_name == TypeName.parse("i32")


def test_interpreter__variable_declaration_no_type():
    module = load_module("""
    fn main() -> i32 {
        let z = 5;
        return z;
    }""")

    interpreter = Interpreter()
    interpreter.visit(module)
    result = interpreter.run("main")

    assert result.value == 5
    assert result.type_name == TypeName.parse("i32")


def test_interpreter__assignment():
    module = load_module("""
    fn main() -> i32 {
        mut let z = 5;
        z = 3;
        return z;
    }""")

    interpreter = Interpreter()
    interpreter.visit(module)
    result = interpreter.run("main")

    assert result.value == 3
    assert result.type_name == TypeName.parse("i32")


def test_interpreter__new_struct():
    module = load_module("""
    struct Item { amount: i32; }
    
    fn main() -> i32 {
        let item: Item = Item { amount = 5; };
        return item;
    }""")

    interpreter = Interpreter()
    interpreter.visit(module)
    result = interpreter.run("main")

    assert result.value.get("amount").value == 5
    assert result.type_name == TypeName.parse("Item")


def test_interpreter__return_statement():
    module = load_module("""
    fn main() -> i32 {
        mut let i: i32 = 0;

        while (i < 10) {
            if (5 < i) {
                {
                    return i;
                }
            }
             i = i + 1;
        }
        return i;
    }""")

    interpreter = Interpreter()
    interpreter.visit(module)
    result = interpreter.run("main")

    assert result.value == 6
    assert result.type_name == TypeName.parse("i32")


def test_interpreter__if_statement():
    module = load_module("""
    fn main() -> i32 {
        mut let z = 5;
        if (z < 6) {
            return 1;
        } 
        else {
            return 0;
        }
    }""")

    interpreter = Interpreter()
    interpreter.visit(module)
    result = interpreter.run("main")

    assert result.value == 1
    assert result.type_name == TypeName.parse("i32")


def test_interpreter__if_statement_else_block():
    module = load_module("""
    fn main() -> i32 {
        mut let z = 5;
        if (z < 4) {
            return 1;
        } 
        else {
            return 0;
        }
    }""")

    interpreter = Interpreter()
    interpreter.visit(module)
    result = interpreter.run("main")

    assert result.value == 0
    assert result.type_name == TypeName.parse("i32")


def test_interpreter__while_statement():
    module = load_module("""
    fn main() -> i32 {
        mut let i: i32 = 0;
        
        while (i < 10) {
             i = i + 1;
        }
        return i;
    }""")

    interpreter = Interpreter()
    interpreter.visit(module)
    result = interpreter.run("main")

    assert result.value == 10
    assert result.type_name == TypeName.parse("i32")


def test_interpreter__match_statement():
    module = load_module("""
    fn main() -> i32 {
        mut let i: i32 = 0;

        match (i) {
            i32 x => { return 10; };
            _ y => { return 20; };
        }
    }""")

    interpreter = Interpreter()
    interpreter.visit(module)
    result = interpreter.run("main")

    assert result.value == 10
    assert result.type_name == TypeName.parse("i32")


def test_interpreter__match_statement_default_case():
    module = load_module("""
    fn main() -> i32 {
        mut let i = 0 == 1;

        match (i) {
            i32 x => { return 10; };
            _ y => { return 20; };
        }
    }""")

    interpreter = Interpreter()
    interpreter.visit(module)
    result = interpreter.run("main")

    assert result.value == 20
    assert result.type_name == TypeName.parse("i32")


def test_interpreter__fn_call():
    module = load_module("""
    fn double(x: i32) -> i32 {
        return double2(x, x);
    }
    
    fn main() -> i32 {
        return double(3);
    }
    
    fn double2(x: i32, y: i32) -> i32 {
        return x + y;
    }
    """)

    interpreter = Interpreter()
    interpreter.visit(module)
    result = interpreter.run("main")

    assert result.value == 6
    assert result.type_name == TypeName.parse("i32")
