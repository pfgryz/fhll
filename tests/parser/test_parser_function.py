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


# region Parse Function Declaration

def test_parse_function_declaration__empty():
    parser = create_parser("fn m() {}", True)

    function = parser.parse_function_declaration()
    expected = FunctionDeclaration(
        name=Name(
            identifier="m",
            location=Location(Position(1, 4), Position(1, 4))
        ),
        parameters=[],
        return_type=None,
        block=Block(
            body=[],
            location=Location(Position(1, 8), Position(1, 9)),
        ),
        location=Location(Position(1, 1), Position(1, 6)),
    )

    assert function is not None
    assert function == expected
    assert function.location == expected.location


def test_parse_function_declaration__with_parameters():
    parser = create_parser("fn main(argc: i32, mut argv: str) {}", True)

    function = parser.parse_function_declaration()
    expected = FunctionDeclaration(
        name=Name(
            identifier="main",
            location=Location(Position(1, 4), Position(1, 7))
        ),
        parameters=[
            Parameter(
                name=Name(
                    identifier="argc",
                    location=Location(Position(1, 9), Position(1, 12))
                ),
                declared_type=Name(
                    identifier="i32",
                    location=Location(Position(1, 15), Position(1, 17))
                ),
                mutable=False,
                location=Location(Position(1, 9), Position(1, 17))
            ),
            Parameter(
                name=Name(
                    identifier="argv",
                    location=Location(Position(1, 24), Position(1, 27))
                ),
                declared_type=Name(
                    identifier="str",
                    location=Location(Position(1, 30), Position(1, 32))
                ),
                mutable=True,
                location=Location(Position(1, 20), Position(1, 32))
            )
        ],
        return_type=None,
        block=Block(
            body=[],
            location=Location(Position(1, 35), Position(1, 36)),
        ),
        location=Location(Position(1, 1), Position(1, 33)),
    )

    assert function is not None
    assert function == expected
    assert function.location == expected.location
    assert function.parameters[1].location == expected.parameters[1].location


def test_parse_function_declaration__return_type():
    parser = create_parser("fn get_name() -> str {}", True)

    function = parser.parse_function_declaration()
    expected = FunctionDeclaration(
        name=Name(
            identifier="get_name",
            location=Location(Position(1, 4), Position(1, 11))
        ),
        parameters=[],
        return_type=Name(
            identifier="str",
            location=Location(Position(1, 18), Position(1, 20))
        ),
        block=Block(
            body=[],
            location=Location(Position(1, 22), Position(1, 23)),
        ),
        location=Location(Position(1, 1), Position(1, 20)),
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


# endregion

# region Parse Parameters

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


# endregion

# region Parse Parameter

def test_parse_parameter__simple():
    parser = create_parser("x: i32", True)

    parameter = parser.parse_parameter()
    expected = Parameter(
        name=Name(
            identifier="x",
            location=Location(Position(1, 1), Position(1, 1))
        ),
        declared_type=Name(
            identifier="i32",
            location=Location(Position(1, 4), Position(1, 6))
        ),
        mutable=False,
        location=Location(Position(1, 1), Position(1, 6))
    )

    assert parameter is not None
    assert parameter == expected
    assert parameter.location == expected.location
    assert parameter.name.location == expected.name.location
    assert parameter.declared_type.location == expected.declared_type.location


def test_parse_parameter__mutable():
    parser = create_parser("mut y: Item", True)

    parameter = parser.parse_parameter()
    expected = Parameter(
        name=Name(
            identifier="y",
            location=Location(Position(1, 5), Position(1, 5))
        ),
        declared_type=Name(
            identifier="Item",
            location=Location(Position(1, 8), Position(1, 11))
        ),
        mutable=True,
        location=Location(Position(1, 1), Position(1, 11))
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

# endregion
