from dataclasses import dataclass

from src.parser.ast.expressions.expression import Expression
from src.parser.ast.expressions.term import Term
from src.parser.ast.expressions.unary_operation_type import EUnaryOperationType


@dataclass
class UnaryOperation(Expression):
    operand: Term
    op: EUnaryOperationType
