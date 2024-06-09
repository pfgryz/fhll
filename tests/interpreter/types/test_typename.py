from src.interpreter.types.typename import TypeName


def test_typename__eq():
    typename = TypeName("i32")

    assert typename == TypeName("i32")


def test_typename__hash():
    typename = TypeName("i32")
    mapping = {typename: 3}
    assert mapping[TypeName("i32")] == 3


def test_typename__repr():
    typename = TypeName("i32")
    assert repr(typename) == "TypeName('i32')"


def test_typename__str():
    typename = TypeName("Main", "Ui")
    assert str(typename) == "Main::Ui"


def test_typename__path():
    typename = TypeName("Main", "Ui")
    assert typename.path == ("Main", "Ui")


def test_typename__extend():
    typename = TypeName("Main", "Ui")
    typename_child = typename.extend("Btn")

    assert typename_child.path == ("Main", "Ui", "Btn")
