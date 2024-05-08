from src.common.location import Location
from src.parser.ast.expressions.expression import Expression
from src.parser.ast.expressions.term import Term
from src.parser.ast.expressions.unary_operation_type import EUnaryOperationType


class UnaryOperation(Expression):

    # region Dunder Methods

    def __init__(self, operand: Term, op: EUnaryOperationType,
                 location: Location):
        super().__init__(location)
        self._operand = operand
        self._op = op

    def __eq__(self, other: object) -> bool:
        return isinstance(other, UnaryOperation) \
            and self.operand == other.operand \
            and self.op == other.op \
            and super().__eq__(other)

    # endregion

    # region Properties

    @property
    def operand(self) -> Term:
        return self._operand

    @property
    def op(self) -> EUnaryOperationType:
        return self._op

    # endregion
