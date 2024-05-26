from dataclasses import dataclass

from src.parser.ast.expressions.compare_type import ECompareType
from src.parser.ast.expressions.expression import Expression


@dataclass
class Compare(Expression):
    left: Expression
    right: Expression
    mode: ECompareType
