from src.common.location import Location
from src.parser.ast.expressions.binary_operation_type import \
    EBinaryOperationType
from src.parser.ast.node import Node


class BinaryOperation(Node):

    # region Dunder Methods
    def __init__(self, left: 'Expression', right: 'Expression',
                 op: EBinaryOperationType, location: Location):
        super().__init__(location)
        self._left = left
        self._right = right
        self._op = op

    def __repr__(self) -> str:
        return "BinaryOperation(left={}, right={}, op={}, location={})".format(
            repr(self.left),
            repr(self.right),
            repr(self.op),
            repr(self.location)
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BinaryOperation) \
            and self.left == other.left \
            and self.right == other.right \
            and self.op == other.op

    # endregion

    # region Properties

    @property
    def left(self) -> 'Expression':
        return self._left

    @property
    def right(self) -> 'Expression':
        return self._right

    @property
    def op(self) -> EBinaryOperationType:
        return self._op

        # endregion
