from dataclasses import dataclass

from src.parser.ast.expressions.bool_operation_type import EBoolOperationType
from src.parser.ast.expressions.expression import Expression
from src.parser.interface.itree_like_expression import ITreeLikeExpression


@dataclass
class BoolOperation(Expression, ITreeLikeExpression):
    left: Expression
    right: Expression
    op: EBoolOperationType
