import pytest

from src.common.location import Location
from src.common.position import Position
from src.parser.ast.declaration.function_declaration import FunctionDeclaration
from src.parser.ast.declaration.parameter import Parameter
from src.parser.ast.name import Name
from src.parser.ast.statements.block import Block
from src.parser.errors import BlockExpectedError, ParenthesisExpectedError, \
    NameExpectedError, TypeExpectedError, ParameterExpectedError, \
    ColonExpectedError
from tests.parser.test_parser import create_parser


def test_parse_function_declaration__empty():
    parser = create_parser("fn m() {}", True)

    function = parser.parse_function_declaration()
    expected = FunctionDeclaration(
        Name("m", Location(Position(1, 4), Position(1, 5))),
        [],
        None,
        Block(
            [],
            Location(Position(1, 8), Position(1, 9)),
        ),
        Location(Position(1, 1), Position(1, 6)),
    )

    assert function is not None
    assert function == expected
    assert function.location == expected.location


def test_parse_function_declaration__with_parameters():
    parser = create_parser("fn main(argc: i32, mut argv: str) {}", True)

    function = parser.parse_function_declaration()
    expected = FunctionDeclaration(
        Name("main", Location(Position(1, 4), Position(1, 7))),
        [
            Parameter(
                Name("argc", Location(Position(1, 9), Position(1, 12))),
                Name("i32", Location(Position(1, 15), Position(1, 17))),
                False,
                Location(Position(1, 9), Position(1, 17))
            ),
            Parameter(
                Name("argv", Location(Position(1, 24), Position(1, 27))),
                Name("str", Location(Position(1, 30), Position(1, 32))),
                True,
                Location(Position(1, 20), Position(1, 32))
            )
        ],
        None,
        Block(
            [],
            Location(Position(1, 35), Position(1, 36)),
        ),
        Location(Position(1, 1), Position(1, 33)),
    )

    assert function is not None
    assert function == expected
    assert function.location == expected.location
    assert function.parameters[1].location == expected.parameters[1].location


def test_parse_function_declaration__return_type():
    parser = create_parser("fn get_name() -> str {}", True)

    function = parser.parse_function_declaration()
    expected = FunctionDeclaration(
        Name("get_name", Location(Position(1, 4), Position(1, 11))),
        [],
        Name("str", Location(Position(1, 18), Position(1, 20))),
        Block(
            [],
            Location(Position(1, 22), Position(1, 23)),
        ),
        Location(Position(1, 1), Position(1, 20)),
    )

    assert function is not None
    assert function == expected
    assert function.location == expected.location
    assert function.return_type.location == expected.return_type.location


def test_parse_function_declaration__missing_identifier():
    parser = create_parser("fn () -> ", True)

    with pytest.raises(NameExpectedError):
        parser.parse_function_declaration()


def test_parse_function_declaration__missing_parenthesis():
    parser = create_parser("fn where_is(", True)

    with pytest.raises(ParenthesisExpectedError):
        parser.parse_function_declaration()


def test_parse_function_declaration__missing_block():
    parser = create_parser("fn where_is()", True)

    with pytest.raises(BlockExpectedError):
        parser.parse_function_declaration()


def test_parse_function_declaration__missing_return_type():
    parser = create_parser("fn where_is() ->", True)

    with pytest.raises(TypeExpectedError):
        parser.parse_function_declaration()


def test_parse_parameters__empty():
    parser = create_parser("", True)

    parameters = parser.parse_parameters()
    expected = []

    assert parameters is not None
    assert parameters == expected


def test_parse_parameters__single():
    parser = create_parser("x: i32", True)

    parameters = parser.parse_parameters()

    assert parameters is not None
    assert len(parameters) == 1


def test_parse_parameters__many():
    parser = create_parser("x: i32, mut y: Entity::Item", True)

    parameters = parser.parse_parameters()

    assert parameters is not None
    assert len(parameters) == 2


def test_parse_parameters__parameter_expected():
    parser = create_parser("x: i32, ", True)

    with pytest.raises(ParameterExpectedError):
        parser.parse_parameters()


def test_parse_parameter__simple():
    parser = create_parser("x: i32", True)

    parameter = parser.parse_parameter()
    expected = Parameter(
        Name("x", Location(Position(1, 1), Position(1, 1))),
        Name("i32", Location(Position(1, 4), Position(1, 6))),
        False,
        Location(Position(1, 1), Position(1, 6))
    )

    assert parameter is not None
    assert parameter == expected
    assert parameter.location == expected.location
    assert parameter.name.location == expected.name.location
    assert parameter.type.location == expected.type.location


def test_parse_parameter__mutable():
    parser = create_parser("mut y: Item", True)

    parameter = parser.parse_parameter()
    expected = Parameter(
        Name("y", Location(Position(1, 5), Position(1, 5))),
        Name("Item", Location(Position(1, 8), Position(1, 11))),
        True,
        Location(Position(1, 1), Position(1, 11))
    )

    assert parameter is not None
    assert parameter == expected
    assert parameter.location == expected.location


def test_parse_parameter__colon_expected():
    parser = create_parser("mut y f32", True)

    with pytest.raises(ColonExpectedError):
        parser.parse_parameter()


def test_parse_parameter__name_expected():
    parser = create_parser("mut : f32", True)

    with pytest.raises(NameExpectedError):
        parser.parse_parameter()


def test_parse_parameter_junk():
    parser = create_parser(": f32", True)

    parameter = parser.parse_parameter()

    assert parameter is None
