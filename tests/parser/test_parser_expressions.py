import pytest

from src.common.location import Location
from src.common.position import Position
from src.parser.ast.access import Access
from src.parser.ast.cast import Cast
from src.parser.ast.constant import Constant
from src.parser.ast.expressions.binary_operation import BinaryOperation
from src.parser.ast.expressions.binary_operation_type import \
    EBinaryOperationType
from src.parser.ast.expressions.bool_operation import BoolOperation
from src.parser.ast.expressions.bool_operation_type import EBoolOperationType
from src.parser.ast.expressions.compare import Compare
from src.parser.ast.expressions.compare_type import ECompareType
from src.parser.ast.expressions.unary_operation import UnaryOperation
from src.parser.ast.expressions.unary_operation_type import EUnaryOperationType
from src.parser.ast.is_compare import IsCompare
from src.parser.ast.name import Name
from src.parser.ast.statements.fn_call import FnCall
from src.parser.ast.statements.new_struct_statement import NewStruct
from src.parser.errors import TypeExpectedError, ParenthesisExpectedError, \
    ExpressionExpectedError
from tests.parser.test_parser import create_parser


# region Parse Or Expression

def test_parse_or_expression__base():
    parser = create_parser("9", True)

    term = parser.parse_expression()
    expected = Constant(
        9,
        Location(Position(1, 1), Position(1, 1))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_or_expression__or():
    parser = create_parser("3 || 0", True)

    term = parser.parse_expression()
    expected = BoolOperation(
        Constant(3, Location(Position(1, 1), Position(1, 1))),
        Constant(0, Location(Position(1, 6), Position(1, 6))),
        EBoolOperationType.Or,
        Location(Position(1, 1), Position(1, 6))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_or_expression__nested():
    parser = create_parser("0 || 2 || false", True)

    term = parser.parse_expression()
    expected = BoolOperation(
        BoolOperation(
            Constant(0, Location(Position(1, 1), Position(1, 1))),
            Constant(2, Location(Position(1, 6), Position(1, 6))),
            EBoolOperationType.Or,
            Location(Position(1, 1), Position(1, 6))
        ),
        Constant(False, Location(Position(1, 11), Position(1, 15))),
        EBoolOperationType.Or,
        Location(Position(1, 1), Position(1, 15))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_or_expression__expression_expected():
    parser = create_parser("10 || ", True)

    with pytest.raises(ExpressionExpectedError):
        parser.parse_expression()


# endregion

# region Parse And Expression

def test_parse_and_expression__base():
    parser = create_parser("1.23", True)

    term = parser.parse_and_expression()
    expected = Constant(
        1.23,
        Location(Position(1, 1), Position(1, 4))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_and_expression__and():
    parser = create_parser("7 && 9", True)

    term = parser.parse_and_expression()
    expected = BoolOperation(
        Constant(7, Location(Position(1, 1), Position(1, 1))),
        Constant(9, Location(Position(1, 6), Position(1, 6))),
        EBoolOperationType.And,
        Location(Position(1, 1), Position(1, 6))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_and_expression__nested():
    parser = create_parser("0 && 4 && 5", True)

    term = parser.parse_and_expression()
    expected = BoolOperation(
        BoolOperation(
            Constant(0, Location(Position(1, 1), Position(1, 1))),
            Constant(4, Location(Position(1, 6), Position(1, 6))),
            EBoolOperationType.And,
            Location(Position(1, 1), Position(1, 6))
        ),
        Constant(5, Location(Position(1, 11), Position(1, 11))),
        EBoolOperationType.And,
        Location(Position(1, 1), Position(1, 11))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_and_expression__expression_expected():
    parser = create_parser("10 && ", True)

    with pytest.raises(ExpressionExpectedError):
        parser.parse_and_expression()


# endregion

# region Parse Relation Expression

def test_parse_relation_expression__base():
    parser = create_parser("false", True)

    term = parser.parse_relation_expression()
    expected = Constant(
        False,
        Location(Position(1, 1), Position(1, 5))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_relation_expression__equal():
    parser = create_parser("2 == 6", True)

    term = parser.parse_relation_expression()
    expected = Compare(
        Constant(2, Location(Position(1, 1), Position(1, 1))),
        Constant(6, Location(Position(1, 6), Position(1, 6))),
        ECompareType.Equal,
        Location(Position(1, 1), Position(1, 6))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_relation_expression__not_equal():
    parser = create_parser("9 != 1", True)

    term = parser.parse_relation_expression()
    expected = Compare(
        Constant(9, Location(Position(1, 1), Position(1, 1))),
        Constant(1, Location(Position(1, 6), Position(1, 6))),
        ECompareType.NotEqual,
        Location(Position(1, 1), Position(1, 6))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_relation_expression__greater():
    parser = create_parser("8 > 4", True)

    term = parser.parse_relation_expression()
    expected = Compare(
        Constant(8, Location(Position(1, 1), Position(1, 1))),
        Constant(4, Location(Position(1, 5), Position(1, 5))),
        ECompareType.Greater,
        Location(Position(1, 1), Position(1, 5))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_relation_expression__less():
    parser = create_parser("3 < 4", True)

    term = parser.parse_relation_expression()
    expected = Compare(
        Constant(3, Location(Position(1, 1), Position(1, 1))),
        Constant(4, Location(Position(1, 5), Position(1, 5))),
        ECompareType.Less,
        Location(Position(1, 1), Position(1, 5))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_relation_expression__expression_expected():
    parser = create_parser("10 == ", True)

    with pytest.raises(ExpressionExpectedError):
        parser.parse_relation_expression()


# endregion

# region Parse Additive Term


def test_parse_additive_term__base():
    parser = create_parser("true", True)

    term = parser.parse_multiplicative_term()
    expected = Constant(
        True,
        Location(Position(1, 1), Position(1, 4))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_additive_term__add():
    parser = create_parser("7 + 9", True)

    term = parser.parse_additive_term()
    expected = BinaryOperation(
        Constant(7, Location(Position(1, 1), Position(1, 1))),
        Constant(9, Location(Position(1, 5), Position(1, 5))),
        EBinaryOperationType.Add,
        Location(Position(1, 1), Position(1, 5))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_additive_term__sub():
    parser = create_parser("0 - 4", True)

    term = parser.parse_additive_term()
    expected = BinaryOperation(
        Constant(0, Location(Position(1, 1), Position(1, 1))),
        Constant(4, Location(Position(1, 5), Position(1, 5))),
        EBinaryOperationType.Sub,
        Location(Position(1, 1), Position(1, 5))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_additive_term__nested():
    parser = create_parser("0 - 4 + 5", True)

    term = parser.parse_additive_term()
    expected = BinaryOperation(
        BinaryOperation(
            Constant(0, Location(Position(1, 1), Position(1, 1))),
            Constant(4, Location(Position(1, 5), Position(1, 5))),
            EBinaryOperationType.Sub,
            Location(Position(1, 1), Position(1, 5))
        ),
        Constant(5, Location(Position(1, 9), Position(1, 9))),
        EBinaryOperationType.Add,
        Location(Position(1, 1), Position(1, 9))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_additive_term__expression_expected():
    parser = create_parser("10 - ", True)

    with pytest.raises(ExpressionExpectedError):
        parser.parse_additive_term()


# endregion

# region Parse Multiplicative Term

def test_parse_multiplicative_term__base():
    parser = create_parser("4.5", True)

    term = parser.parse_multiplicative_term()
    expected = Constant(
        4.5,
        Location(Position(1, 1), Position(1, 3))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_multiplicative_term__multiply():
    parser = create_parser("3 * 4", True)

    term = parser.parse_multiplicative_term()
    expected = BinaryOperation(
        Constant(3, Location(Position(1, 1), Position(1, 1))),
        Constant(4, Location(Position(1, 5), Position(1, 5))),
        EBinaryOperationType.Multiply,
        Location(Position(1, 1), Position(1, 5))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_multiplicative_term__divide():
    parser = create_parser("10 / 5", True)

    term = parser.parse_multiplicative_term()
    expected = BinaryOperation(
        Constant(10, Location(Position(1, 1), Position(1, 2))),
        Constant(5, Location(Position(1, 6), Position(1, 6))),
        EBinaryOperationType.Divide,
        Location(Position(1, 1), Position(1, 6))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_multiplicative_term__nested():
    parser = create_parser("10 / 5 * 2", True)

    term = parser.parse_multiplicative_term()
    expected = BinaryOperation(
        BinaryOperation(
            Constant(10, Location(Position(1, 1), Position(1, 2))),
            Constant(5, Location(Position(1, 6), Position(1, 6))),
            EBinaryOperationType.Divide,
            Location(Position(1, 1), Position(1, 6))
        ),
        Constant(2, Location(Position(1, 10), Position(1, 10))),
        EBinaryOperationType.Multiply,
        Location(Position(1, 1), Position(1, 10))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_multiplicative_term__expected_expression():
    parser = create_parser("10 * ", True)

    with pytest.raises(ExpressionExpectedError):
        parser.parse_multiplicative_term()


# endregion

# region Parse Unary Term

def test_parse_unary_term__base():
    parser = create_parser("34", True)

    term = parser.parse_unary_term()
    expected = Constant(
        34,
        Location(Position(1, 1), Position(1, 2))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_unary_term__minus():
    parser = create_parser("- 4", True)

    term = parser.parse_unary_term()
    expected = UnaryOperation(
        Constant(4, Location(Position(1, 3), Position(1, 3))),
        EUnaryOperationType.Minus,
        Location(Position(1, 1), Position(1, 3))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_unary_term__negate():
    parser = create_parser("! true", True)

    term = parser.parse_unary_term()
    expected = UnaryOperation(
        Constant(True, Location(Position(1, 3), Position(1, 6))),
        EUnaryOperationType.Negate,
        Location(Position(1, 1), Position(1, 6))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


@pytest.mark.parametrize(
    "operator",
    (
            pytest.param("!", id="logical not"),
            pytest.param("-", id="unary minus")
    )
)
def test_parse_unary_term__expression_expected(operator: str):
    parser = create_parser(f"{operator} ", True)

    with pytest.raises(ExpressionExpectedError):
        parser.parse_unary_term()


# endregion

# region Parse Casted Term

def test_parse_casted_term__base():
    parser = create_parser("name", True)

    term = parser.parse_casted_term()
    expected = Name("name", Location(Position(1, 1), Position(1, 4)))

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_casted_term__cast():
    parser = create_parser("name as Name", True)

    term = parser.parse_casted_term()
    expected = Cast(
        Name("name", Location(Position(1, 1), Position(1, 4))),
        Name("Name", Location(Position(1, 9), Position(1, 12))),
        Location(Position(1, 1), Position(1, 12))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_casted_term__is_compare():
    parser = create_parser("name is Name", True)

    term = parser.parse_casted_term()
    expected = IsCompare(
        Name("name", Location(Position(1, 1), Position(1, 4))),
        Name("Name", Location(Position(1, 9), Position(1, 12))),
        Location(Position(1, 1), Position(1, 12))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_term__cast_expected_type():
    parser = create_parser("name as ", True)

    with pytest.raises(TypeExpectedError):
        parser.parse_casted_term()


def test_parse_term__is_compare_expected_type():
    parser = create_parser("name is ", True)

    with pytest.raises(TypeExpectedError):
        parser.parse_casted_term()


# endregion

# region Parse Term

def test_parse_term__integer_literal():
    parser = create_parser("134", True)

    term = parser.parse_term()
    expected = Constant(
        134,
        Location(Position(1, 1), Position(1, 3))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_term__float_literal():
    parser = create_parser("3.14", True)

    term = parser.parse_term()
    expected = Constant(
        3.14,
        Location(Position(1, 1), Position(1, 4))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_term__string_literal():
    parser = create_parser("\"Hello World\"", True)

    term = parser.parse_term()
    expected = Constant(
        "Hello World",
        Location(Position(1, 1), Position(1, 13))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_term__boolean_literal():
    parser = create_parser("false", True)

    term = parser.parse_term()
    expected = Constant(
        False,
        Location(Position(1, 1), Position(1, 5))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_term__access():
    parser = create_parser("user.name", True)

    term = parser.parse_term()
    expected = Access(
        Name("name", Location(Position(1, 6), Position(1, 9))),
        Name("user", Location(Position(1, 1), Position(1, 4))),
        Location(Position(1, 1), Position(1, 9))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_term__fn_call():
    parser = create_parser("main()", True)

    term = parser.parse_term()
    expected = FnCall(
        Name("main", Location(Position(1, 1), Position(1, 4))),
        [],
        Location(Position(1, 1), Position(1, 6))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_term__new_struct():
    parser = create_parser("Item {}", True)

    term = parser.parse_term()
    expected = NewStruct(
        Name("Item", Location(Position(1, 1), Position(1, 4))),
        [],
        Location(Position(1, 1), Position(1, 7))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_term__parentheses():
    parser = create_parser("( 5 )", True)

    term = parser.parse_term()
    expected = Constant(
        5,
        Location(Position(1, 3), Position(1, 3))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_term__parentheses_expected_close_parenthesis():
    parser = create_parser("( 5 ", True)

    with pytest.raises(ParenthesisExpectedError):
        parser.parse_term()


def test_parse_term__parentheses_expected_expression():
    parser = create_parser("( )", True)

    with pytest.raises(ExpressionExpectedError):
        parser.parse_term()

# endregion
