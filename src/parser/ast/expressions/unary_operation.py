from src.common.location import Location
from src.parser.ast.access import Access
from src.parser.ast.cast import Cast
from src.parser.ast.constant import Constant
from src.parser.ast.expressions.unary_operation_type import EUnaryOperationType
from src.parser.ast.is_compare import IsCompare
from src.parser.ast.node import Node

type Term = Constant | Access | IsCompare | Cast


class UnaryOperation(Node):

    # region Dunder Methods
    def __init__(self, operand: Term, op: EUnaryOperationType, location: Location):
        super().__init__(location)
        self._operand = operand
        self._op = op

    def __repr__(self) -> str:
        return "UnaryOperation(operand={}, op={}, location={})".format(
            repr(self.operand),
            repr(self.op),
            repr(self.location)
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, UnaryOperation) \
            and self.operand == other.operand \
            and self.op == other.op

    # endregion

    # region Properties

    @property
    def operand(self) -> Term:
        return self._operand

    @property
    def op(self) -> EUnaryOperationType:
        return self._op

        # endregion
