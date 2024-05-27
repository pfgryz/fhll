from dataclasses import dataclass

from src.parser.ast.expressions.binary_operation_type import \
    EBinaryOperationType
from src.parser.ast.expressions.expression import Expression
from src.parser.interface.itree_like_expression import ITreeLikeExpression


@dataclass
class BinaryOperation(Expression, ITreeLikeExpression):
    left: Expression
    right: Expression
    op: EBinaryOperationType
