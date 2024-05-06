import pytest

from src.common.location import Location
from src.common.position import Position
from src.parser.ast.constant import Constant
from src.parser.ast.expressions.binary_operation import BinaryOperation
from src.parser.ast.expressions.binary_operation_type import \
    EBinaryOperationType
from src.parser.ast.name import Name
from src.parser.ast.statements.assignment import Assignment
from src.parser.ast.statements.fn_call import FnCall
from src.parser.ast.statements.new_struct_statement import NewStruct
from src.parser.ast.statements.variable_declaration import VariableDeclaration
from src.parser.errors import NameExpectedError, TypeExpectedError, \
    ExpressionExpectedError, LetKeywordExpectedError, AssignExpectedError, \
    ParenthesisExpectedError
from tests.parser.test_parser import create_parser


# region Parse Declaration

def test_parse_declaration__empty():
    parser = create_parser("let a", True)

    declaration = parser.parse_declaration()
    expected = VariableDeclaration(
        Name("a", Location(Position(1, 5), Position(1, 5))),
        False,
        None,
        None,
        Location(Position(1, 1), Position(1, 5))
    )

    assert declaration is not None
    assert declaration == expected
    assert declaration.location == expected.location
    assert declaration.name.location == expected.name.location


def test_parse_declaration__mutable():
    parser = create_parser("mut let b", True)

    declaration = parser.parse_declaration()
    expected = VariableDeclaration(
        Name("b", Location(Position(1, 9), Position(1, 9))),
        True,
        None,
        None,
        Location(Position(1, 1), Position(1, 9))
    )

    assert declaration is not None
    assert declaration == expected
    assert declaration.location == expected.location


def test_parse_declaration__value():
    parser = create_parser("let c = 3", True)

    declaration = parser.parse_declaration()
    expected = VariableDeclaration(
        Name("c", Location(Position(1, 5), Position(1, 5))),
        False,
        None,
        Constant(
            3,
            Location(Position(1, 9), Position(1, 9))
        ),
        Location(Position(1, 1), Position(1, 9))
    )

    assert declaration is not None
    assert declaration == expected
    assert declaration.location == expected.location


def test_parse_declaration__type():
    parser = create_parser("let d: i32", True)

    declaration = parser.parse_declaration()
    expected = VariableDeclaration(
        Name("d", Location(Position(1, 5), Position(1, 5))),
        False,
        Name("i32", Location(Position(1, 8), Position(1, 10))),
        None,
        Location(Position(1, 1), Position(1, 10))
    )

    assert declaration is not None
    assert declaration == expected
    assert declaration.location == expected.location


# @TODO: Will fail until parse_expression is not fixed
def test_parse_declaration__complex():
    parser = create_parser("mut let e: Item = Item {}", True)

    declaration = parser.parse_declaration()
    expected = VariableDeclaration(
        Name("e", Location(Position(1, 9), Position(1, 9))),
        False,
        Name("Item", Location(Position(1, 12), Position(1, 15))),
        NewStruct(
            Name("Item", Location(Position(1, 19), Position(1, 22))),
            [],
            Location(Position(1, 19), Position(1, 25))
        ),
        Location(Position(1, 1), Position(1, 25))
    )

    assert declaration is not None
    assert declaration == expected


def test_parse_declaration__name_expected():
    parser = create_parser("let =", True)

    with pytest.raises(NameExpectedError):
        parser.parse_declaration()


def test_parse_declaration__let_expected():
    parser = create_parser("mut e: Item = Item {}", True)

    with pytest.raises(LetKeywordExpectedError):
        parser.parse_declaration()


def test_parse_declaration__type_expected():
    parser = create_parser("let e: = Item {}", True)

    with pytest.raises(TypeExpectedError):
        parser.parse_declaration()


def test_parse_declaration__expression_expected():
    parser = create_parser("mut let e: Item = ", True)

    with pytest.raises(ExpressionExpectedError):
        parser.parse_declaration()


# endregion

# region Parse Assignment

def test_parse_assignment__simple():
    parser = create_parser("a = 3", True)

    assignment = parser.parse_assignment()
    expected = Assignment(
        Name("a", Location(Position(1, 1), Position(1, 1))),
        Constant(3, Location(Position(1, 5), Position(1, 5))),
        Location(Position(1, 1), Position(1, 5))
    )

    assert assignment is not None
    assert assignment == expected
    assert assignment.location == expected.location


def test_parse_assignment__assign_expected():
    parser = create_parser("a ", True)

    with pytest.raises(AssignExpectedError):
        parser.parse_assignment()


def test_parse_assignment__expression_expected():
    parser = create_parser("a = ", True)

    with pytest.raises(ExpressionExpectedError):
        parser.parse_assignment()


# endregion

# region Parse Fn Call

def test_parse_fn_call__zero_arguments():
    parser = create_parser("main()", True)

    fn_call = parser.parse_fn_call()
    expected = FnCall(
        Name("main", Location(Position(1, 1), Position(1, 4))),
        [],
        Location(Position(1, 1), Position(1, 6))
    )

    assert fn_call is not None
    assert fn_call == expected
    assert fn_call.location == expected.location


def test_parse_fn_call__arguments():
    parser = create_parser("boot(4, \"test\")", True)

    fn_call = parser.parse_fn_call()
    expected = FnCall(
        Name("boot", Location(Position(1, 1), Position(1, 4))),
        [
            Constant(4, Location(Position(1, 6), Position(1, 6))),
            Constant("test", Location(Position(1, 10), Position(1, 13))),
        ],
        Location(Position(1, 1), Position(1, 15))
    )

    assert fn_call is not None
    assert fn_call == expected
    assert fn_call.location == expected.location


def test_parse_fn_call__open_parenthesis_expected():
    parser = create_parser("main", True)

    with pytest.raises(ParenthesisExpectedError):
        parser.parse_fn_call()


def test_parse_fn_call__close_parenthesis_expected():
    parser = create_parser("main(", True)

    with pytest.raises(ParenthesisExpectedError):
        parser.parse_fn_call()


# endregion

# region Parse Fn Arguments

def test_parse_fn_arguments__empty():
    parser = create_parser("", True)

    arguments = parser.parse_fn_arguments()
    expected = []

    assert arguments is not None
    assert arguments == expected


def test_parse_fn_arguments__single():
    parser = create_parser("3 + 4", True)

    arguments = parser.parse_fn_arguments()
    expected = [
        BinaryOperation(
            Constant(3, Location(Position(1, 1), Position(1, 1))),
            Constant(4, Location(Position(1, 5), Position(1, 5))),
            EBinaryOperationType.Add,
            Location(Position(1, 1), Position(1, 5))
        )
    ]

    assert arguments is not None
    assert arguments == expected


def test_parse_fn_arguments__many():
    parser = create_parser("3 * 5, 10 / 3 - 3", True)

    arguments = parser.parse_fn_arguments()

    assert arguments is not None
    assert len(arguments) == 2


def test_parse_fn_arguments__expression_expected():
    parser = create_parser("1, ", True)

    with pytest.raises(ExpressionExpectedError):
        parser.parse_fn_arguments()

# endregion
