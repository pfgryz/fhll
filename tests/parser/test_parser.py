import pytest

from src.lexer.lexer import Lexer
from src.parser.errors import SyntaxExpectedTokenException, SyntaxException
from src.parser.parser import Parser
from src.utils.buffer import StreamBuffer


# region Utils

def create_parser(content: str, consume_first: bool = False) -> Parser:
    buffer = StreamBuffer.from_str(content)
    lexer = Lexer(buffer)
    parser = Parser(lexer)

    # Read first token
    if consume_first:
        parser.consume()

    return parser


# endregion

# region Parse Function
def test_parse_function_simple():
    parser = create_parser("fn main() {}", consume_first=True)

    function = parser.parse_function()

    assert function is not None
    assert function.name == "main"
    assert len(function.parameters) == 0
    assert function.returns is None


def test_parse_function_with_parameter():
    parser = create_parser("fn main(x: i32) {}", consume_first=True)

    function = parser.parse_function()

    assert function is not None
    assert len(function.parameters) == 1
    assert function.parameters[0].name == "x"
    assert function.parameters[0].types == "i32"
    assert not function.parameters[0].mutable


def test_parse_function_with_mutable_parameter():
    parser = create_parser("fn main(mut x: i32) {}", consume_first=True)

    function = parser.parse_function()

    assert function is not None
    assert len(function.parameters) == 1
    assert function.parameters[0].mutable


def test_parse_function_with_many_parameters():
    parser = create_parser("fn main(x: i32, mut y: f32, c: str) {}",
                           consume_first=True)

    function = parser.parse_function()

    assert function is not None
    assert len(function.parameters) == 3
    assert function.parameters[0].name == "x"
    assert function.parameters[2].name == "c"
    assert function.parameters[2].types == "str"


def test_parse_function_with_return_type():
    parser = create_parser("fn main() -> i32 {}", consume_first=True)

    function = parser.parse_function()

    assert function is not None
    assert function.returns == "i32"


def test_parse_function_missing_parenthesis():
    parser = create_parser("fn main x: i32) {}", consume_first=True)

    with pytest.raises(SyntaxExpectedTokenException):
        parser.parse_function()


def test_parse_parameters():
    parser = create_parser("x: i32", consume_first=True)

    parameters = parser.parse_parameters()
    assert len(parameters) == 1


def test_parse_parameters_multiple():
    parser = create_parser("x: i32, mut y: f32", consume_first=True)

    parameters = parser.parse_parameters()

    assert len(parameters) == 2


def test_parse_parameters_expected_parameter_after_comma():
    parser = create_parser("x: i32, ", consume_first=True)

    with pytest.raises(SyntaxException):
        parameters = parser.parse_parameters()


def test_parse_parameter():
    parser = create_parser("x: i32", consume_first=True)

    parameter = parser.parse_parameter()

    assert parameter is not None
    assert parameter.name == "x"
    assert parameter.types == "i32"
    assert not parameter.mutable


def test_parse_parameter_mutable():
    parser = create_parser("mut x: i32", consume_first=True)

    parameter = parser.parse_parameter()

    assert parameter is not None
    assert parameter.mutable


def test_parse_parameter_junk():
    parser = create_parser("()", consume_first=True)

    parameter = parser.parse_parameter()

    assert parameter is None


def test_parse_parameter_missing_identifier():
    parser = create_parser("mut ()", consume_first=True)

    with pytest.raises(SyntaxExpectedTokenException):
        parser.parse_parameter()


def test_parse_parameter_missing_colon():
    parser = create_parser("x i32", consume_first=True)

    with pytest.raises(SyntaxExpectedTokenException):
        parser.parse_parameter()

# endregion
