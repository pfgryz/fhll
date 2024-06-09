import pytest

from src.lexer.token_kind import TokenKind
from src.parser.ast.expressions.binary_operation_type import \
    EBinaryOperationType
from src.parser.ast.expressions.bool_operation_type import EBoolOperationType
from src.parser.ast.expressions.compare_type import ECompareType
from src.parser.ast.expressions.unary_operation_type import EUnaryOperationType


# region EBinaryOperationType

@pytest.mark.parametrize(
    "operation, operator",
    (
            (EBinaryOperationType.Add, "+"),
            (EBinaryOperationType.Sub, "-"),
            (EBinaryOperationType.Multiply, "*"),
            (EBinaryOperationType.Divide, "/")
    )
)
def test_binary_operation_type_to_operator(
        operation: EBinaryOperationType,
        operator: str
):
    assert operation.to_operator() == operator


def test_binary_operation_type_from_invalid_token():
    assert EBinaryOperationType.from_token_kind(TokenKind.Identifier) is None


# endregion

# region EBoolOperationType

@pytest.mark.parametrize(
    "operation, operator",
    (
            (EBoolOperationType.And, "&&"),
            (EBoolOperationType.Or, "||")
    )
)
def test_bool_operation_type_to_operator(
        operation: EBoolOperationType,
        operator: str
):
    assert operation.to_operator() == operator


def test_bool_operation_type_from_invalid_token():
    assert EBoolOperationType.from_token_kind(TokenKind.Identifier) is None


# endregion

# region ECompareType

@pytest.mark.parametrize(
    "operation, operator",
    (
            (ECompareType.Equal, "=="),
            (ECompareType.NotEqual, "!="),
            (ECompareType.Less, "<"),
            (ECompareType.Greater, ">")
    )
)
def test_compare_type_to_operator(
        operation: ECompareType,
        operator: str
):
    assert operation.to_operator() == operator


def test_compare_type_from_invalid_token():
    assert ECompareType.from_token_kind(TokenKind.Identifier) is None


# endregion

# region EUnaryOperationType

@pytest.mark.parametrize(
    "operation, operator",
    (
            (EUnaryOperationType.Minus, "-"),
            (EUnaryOperationType.Negate, "!")
    )
)
def test_unary_operation_type_to_operator(
        operation: ECompareType,
        operator: str
):
    assert operation.to_operator() == operator


def test_unary_operation_type_from_invalid_token():
    assert EUnaryOperationType.from_token_kind(TokenKind.Identifier) is None

# endregion
