import pytest

from src.common.location import Location
from src.common.position import Position
from src.parser.ast.access import Access
from src.parser.ast.cast import Cast
from src.parser.ast.constant import Constant, ConstantValueType
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
    parser = create_parser("9")

    term = parser.parse_expression()
    expected = Constant(
        value=9,
        type=ConstantValueType.I32,
        location=Location(Position(1, 1), Position(1, 1))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_or_expression__or():
    parser = create_parser("3 || 0")

    term = parser.parse_expression()
    expected = BoolOperation(
        left=Constant(
            value=3,
            type=ConstantValueType.I32,
            location=Location(Position(1, 1), Position(1, 1))
        ),
        right=Constant(
            value=0,
            type=ConstantValueType.I32,
            location=Location(Position(1, 6), Position(1, 6))
        ),
        op=EBoolOperationType.Or,
        location=Location(Position(1, 1), Position(1, 6))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_or_expression__nested():
    parser = create_parser("0 || 2 || false")

    term = parser.parse_expression()
    expected = BoolOperation(
        left=BoolOperation(
            left=Constant(
                value=0,
                type=ConstantValueType.I32,
                location=Location(Position(1, 1), Position(1, 1))
            ),
            right=Constant(
                value=2,
                type=ConstantValueType.I32,
                location=Location(Position(1, 6), Position(1, 6))
            ),
            op=EBoolOperationType.Or,
            location=Location(Position(1, 1), Position(1, 6))
        ),
        right=Constant(
            value=False,
            type=ConstantValueType.Bool,
            location=Location(Position(1, 11), Position(1, 15))
        ),
        op=EBoolOperationType.Or,
        location=Location(Position(1, 1), Position(1, 15))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_or_expression__expression_expected():
    parser = create_parser("10 || ")

    with pytest.raises(ExpressionExpectedError):
        parser.parse_expression()


# endregion

# region Parse And Expression

def test_parse_and_expression__base():
    parser = create_parser("1.23")

    term = parser.parse_and_expression()
    expected = Constant(
        value=1.23,
        type=ConstantValueType.F32,
        location=Location(Position(1, 1), Position(1, 4))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_and_expression__and():
    parser = create_parser("7 && 9")

    term = parser.parse_and_expression()
    expected = BoolOperation(
        left=Constant(
            value=7,
            type=ConstantValueType.I32,
            location=Location(Position(1, 1), Position(1, 1))
        ),
        right=Constant(
            value=9,
            type=ConstantValueType.I32,
            location=Location(Position(1, 6), Position(1, 6))
        ),
        op=EBoolOperationType.And,
        location=Location(Position(1, 1), Position(1, 6))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_and_expression__nested():
    parser = create_parser("0 && 4 && 5")

    term = parser.parse_and_expression()
    expected = BoolOperation(
        BoolOperation(
            Constant(
                value=0,
                type=ConstantValueType.I32,
                location=Location(Position(1, 1), Position(1, 1))
            ),
            Constant(
                value=4,
                type=ConstantValueType.I32,
                location=Location(Position(1, 6), Position(1, 6))
            ),
            EBoolOperationType.And,
            location=Location(Position(1, 1), Position(1, 6))
        ),
        Constant(
            value=5,
            type=ConstantValueType.I32,
            location=Location(Position(1, 11), Position(1, 11))
        ),
        EBoolOperationType.And,
        location=Location(Position(1, 1), Position(1, 11))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_and_expression__expression_expected():
    parser = create_parser("10 && ")

    with pytest.raises(ExpressionExpectedError):
        parser.parse_and_expression()


# endregion

# region Parse Relation Expression

def test_parse_relation_expression__base():
    parser = create_parser("false")

    term = parser.parse_relation_expression()
    expected = Constant(
        value=False,
        type=ConstantValueType.Bool,
        location=Location(Position(1, 1), Position(1, 5))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_relation_expression__equal():
    parser = create_parser("2 == 6")

    term = parser.parse_relation_expression()
    expected = Compare(
        left=Constant(
            value=2,
            type=ConstantValueType.I32,
            location=Location(Position(1, 1), Position(1, 1))
        ),
        right=Constant(
            value=6,
            type=ConstantValueType.I32,
            location=Location(Position(1, 6), Position(1, 6))
        ),
        op=ECompareType.Equal,
        location=Location(Position(1, 1), Position(1, 6))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_relation_expression__not_equal():
    parser = create_parser("9 != 1")

    term = parser.parse_relation_expression()
    expected = Compare(
        left=Constant(
            value=9,
            type=ConstantValueType.I32,
            location=Location(Position(1, 1), Position(1, 1))
        ),
        right=Constant(
            value=1,
            type=ConstantValueType.I32,
            location=Location(Position(1, 6), Position(1, 6))
        ),
        op=ECompareType.NotEqual,
        location=Location(Position(1, 1), Position(1, 6))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_relation_expression__greater():
    parser = create_parser("8 > 4")

    term = parser.parse_relation_expression()
    expected = Compare(
        left=Constant(
            value=8,
            type=ConstantValueType.I32,
            location=Location(Position(1, 1), Position(1, 1))
        ),
        right=Constant(
            value=4,
            type=ConstantValueType.I32,
            location=Location(Position(1, 5), Position(1, 5))
        ),
        op=ECompareType.Greater,
        location=Location(Position(1, 1), Position(1, 5))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_relation_expression__less():
    parser = create_parser("3 < 4")

    term = parser.parse_relation_expression()
    expected = Compare(
        left=Constant(
            value=3,
            type=ConstantValueType.I32,
            location=Location(Position(1, 1), Position(1, 1))
        ),
        right=Constant(
            value=4,
            type=ConstantValueType.I32,
            location=Location(Position(1, 5), Position(1, 5))
        ),
        op=ECompareType.Less,
        location=Location(Position(1, 1), Position(1, 5))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_relation_expression__expression_expected():
    parser = create_parser("10 == ")

    with pytest.raises(ExpressionExpectedError):
        parser.parse_relation_expression()


# endregion

# region Parse Additive Term


def test_parse_additive_term__base():
    parser = create_parser("true")

    term = parser.parse_multiplicative_term()
    expected = Constant(
        value=True,
        type=ConstantValueType.Bool,
        location=Location(Position(1, 1), Position(1, 4))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_additive_term__add():
    parser = create_parser("7 + 9")

    term = parser.parse_additive_term()
    expected = BinaryOperation(
        left=Constant(
            value=7,
            type=ConstantValueType.I32,
            location=Location(Position(1, 1), Position(1, 1))
        ),
        right=Constant(
            value=9,
            type=ConstantValueType.I32,
            location=Location(Position(1, 5), Position(1, 5))
        ),
        op=EBinaryOperationType.Add,
        location=Location(Position(1, 1), Position(1, 5))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_additive_term__sub():
    parser = create_parser("0 - 4")

    term = parser.parse_additive_term()
    expected = BinaryOperation(
        left=Constant(
            value=0,
            type=ConstantValueType.I32,
            location=Location(Position(1, 1), Position(1, 1))
        ),
        right=Constant(
            value=4,
            type=ConstantValueType.I32,
            location=Location(Position(1, 5), Position(1, 5))
        ),
        op=EBinaryOperationType.Sub,
        location=Location(Position(1, 1), Position(1, 5))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_additive_term__nested():
    parser = create_parser("0 - 4 + 5")

    term = parser.parse_additive_term()
    expected = BinaryOperation(
        left=BinaryOperation(
            left=Constant(
                value=0,
                type=ConstantValueType.I32,
                location=Location(Position(1, 1), Position(1, 1))
            ),
            right=Constant(
                value=4,
                type=ConstantValueType.I32,
                location=Location(Position(1, 5), Position(1, 5))
            ),
            op=EBinaryOperationType.Sub,
            location=Location(Position(1, 1), Position(1, 5))
        ),
        right=Constant(
            value=5,
            type=ConstantValueType.I32,
            location=Location(Position(1, 9), Position(1, 9))
        ),
        op=EBinaryOperationType.Add,
        location=Location(Position(1, 1), Position(1, 9))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_additive_term__expression_expected():
    parser = create_parser("10 - ")

    with pytest.raises(ExpressionExpectedError):
        parser.parse_additive_term()


# endregion

# region Parse Multiplicative Term

def test_parse_multiplicative_term__base():
    parser = create_parser("4.5")

    term = parser.parse_multiplicative_term()
    expected = Constant(
        value=4.5,
        type=ConstantValueType.F32,
        location=Location(Position(1, 1), Position(1, 3))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_multiplicative_term__multiply():
    parser = create_parser("3 * 4")

    term = parser.parse_multiplicative_term()
    expected = BinaryOperation(
        left=Constant(
            value=3,
            type=ConstantValueType.I32,
            location=Location(Position(1, 1), Position(1, 1))
        ),
        right=Constant(
            value=4,
            type=ConstantValueType.I32,
            location=Location(Position(1, 5), Position(1, 5))
        ),
        op=EBinaryOperationType.Multiply,
        location=Location(Position(1, 1), Position(1, 5))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_multiplicative_term__divide():
    parser = create_parser("10 / 5")

    term = parser.parse_multiplicative_term()
    expected = BinaryOperation(
        left=Constant(
            value=10,
            type=ConstantValueType.I32,
            location=Location(Position(1, 1), Position(1, 2))
        ),
        right=Constant(
            value=5,
            type=ConstantValueType.I32,
            location=Location(Position(1, 6), Position(1, 6))
        ),
        op=EBinaryOperationType.Divide,
        location=Location(Position(1, 1), Position(1, 6))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_multiplicative_term__nested():
    parser = create_parser("10 / 5 * 2")

    term = parser.parse_multiplicative_term()
    expected = BinaryOperation(
        left=BinaryOperation(
            Constant(
                value=10,
                type=ConstantValueType.I32,
                location=Location(Position(1, 1), Position(1, 2))
            ),
            Constant(
                value=5,
                type=ConstantValueType.I32,
                location=Location(Position(1, 6), Position(1, 6))
            ),
            EBinaryOperationType.Divide,
            location=Location(Position(1, 1), Position(1, 6))
        ),
        right=Constant(
            value=2,
            type=ConstantValueType.I32,
            location=Location(Position(1, 10), Position(1, 10))
        ),
        op=EBinaryOperationType.Multiply,
        location=Location(Position(1, 1), Position(1, 10))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_multiplicative_term__expected_expression():
    parser = create_parser("10 * ")

    with pytest.raises(ExpressionExpectedError):
        parser.parse_multiplicative_term()


# endregion

# region Parse Unary Term

def test_parse_unary_term__base():
    parser = create_parser("34")

    term = parser.parse_unary_term()
    expected = Constant(
        value=34,
        type=ConstantValueType.I32,
        location=Location(Position(1, 1), Position(1, 2))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_unary_term__minus():
    parser = create_parser("- 4")

    term = parser.parse_unary_term()
    expected = UnaryOperation(
        operand=Constant(
            value=4,
            type=ConstantValueType.I32,
            location=Location(Position(1, 3), Position(1, 3))
        ),
        op=EUnaryOperationType.Minus,
        location=Location(Position(1, 1), Position(1, 3))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_unary_term__negate():
    parser = create_parser("! true")

    term = parser.parse_unary_term()
    expected = UnaryOperation(
        operand=Constant(
            value=True,
            type=ConstantValueType.Bool,
            location=Location(Position(1, 3), Position(1, 6))
        ),
        op=EUnaryOperationType.Negate,
        location=Location(Position(1, 1), Position(1, 6))
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
    parser = create_parser(f"{operator} ")

    with pytest.raises(ExpressionExpectedError):
        parser.parse_unary_term()


# endregion

# region Parse Casted Term

def test_parse_casted_term__base():
    parser = create_parser("name")

    term = parser.parse_casted_term()
    expected = Name(
        identifier="name",
        location=Location(Position(1, 1), Position(1, 4))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_casted_term__cast():
    parser = create_parser("name as Name")

    term = parser.parse_casted_term()
    expected = Cast(
        value=Name(
            identifier="name",
            location=Location(Position(1, 1), Position(1, 4))
        ),
        to_type=Name(
            identifier="Name",
            location=Location(Position(1, 9), Position(1, 12))
        ),
        location=Location(Position(1, 1), Position(1, 12))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_casted_term__is_compare():
    parser = create_parser("name is Name")

    term = parser.parse_casted_term()
    expected = IsCompare(
        value=Name(
            identifier="name",
            location=Location(Position(1, 1), Position(1, 4))
        ),
        is_type=Name(
            identifier="Name",
            location=Location(Position(1, 9), Position(1, 12))
        ),
        location=Location(Position(1, 1), Position(1, 12))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_term__cast_expected_type():
    parser = create_parser("name as ")

    with pytest.raises(TypeExpectedError):
        parser.parse_casted_term()


def test_parse_term__is_compare_expected_type():
    parser = create_parser("name is ")

    with pytest.raises(TypeExpectedError):
        parser.parse_casted_term()


# endregion

# region Parse Term

def test_parse_term__integer_literal():
    parser = create_parser("134")

    term = parser.parse_term()
    expected = Constant(
        value=134,
        type=ConstantValueType.I32,
        location=Location(Position(1, 1), Position(1, 3))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_term__float_literal():
    parser = create_parser("3.14")

    term = parser.parse_term()
    expected = Constant(
        value=3.14,
        type=ConstantValueType.F32,
        location=Location(Position(1, 1), Position(1, 4))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_term__string_literal():
    parser = create_parser("\"Hello World\"")

    term = parser.parse_term()
    expected = Constant(
        value="Hello World",
        type=ConstantValueType.Str,
        location=Location(Position(1, 1), Position(1, 13))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_term__boolean_literal():
    parser = create_parser("false")

    term = parser.parse_term()
    expected = Constant(
        value=False,
        type=ConstantValueType.Bool,
        location=Location(Position(1, 1), Position(1, 5))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_term__access():
    parser = create_parser("user.name")

    term = parser.parse_term()
    expected = Access(
        name=Name(
            identifier="name",
            location=Location(Position(1, 6), Position(1, 9))
        ),
        parent=Name(
            identifier="user",
            location=Location(Position(1, 1), Position(1, 4))
        ),
        location=Location(Position(1, 1), Position(1, 9))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_term__fn_call():
    parser = create_parser("main()")

    term = parser.parse_term()
    expected = FnCall(
        name=Name(
            identifier="main",
            location=Location(Position(1, 1), Position(1, 4))
        ),
        arguments=[],
        location=Location(Position(1, 1), Position(1, 6))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_term__new_struct():
    parser = create_parser("Item {}")

    term = parser.parse_term()
    expected = NewStruct(
        variant=Name(
            identifier="Item",
            location=Location(Position(1, 1), Position(1, 4))
        ),
        assignments=[],
        location=Location(Position(1, 1), Position(1, 7))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_term__parentheses():
    parser = create_parser("( 5 )")

    term = parser.parse_term()
    expected = Constant(
        value=5,
        type=ConstantValueType.I32,
        location=Location(Position(1, 3), Position(1, 3))
    )

    assert term is not None
    assert term == expected
    assert term.location == expected.location


def test_parse_term__parentheses_expected_close_parenthesis():
    parser = create_parser("( 5 ")

    with pytest.raises(ParenthesisExpectedError):
        parser.parse_term()


def test_parse_term__parentheses_expected_expression():
    parser = create_parser("( )")

    with pytest.raises(ExpressionExpectedError):
        parser.parse_term()

# endregion
