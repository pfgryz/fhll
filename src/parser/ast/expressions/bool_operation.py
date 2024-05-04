from src.common.location import Location
from src.parser.ast.expressions.bool_operation_type import EBoolOperationType
from src.parser.ast.expressions.expression import Expression


class BoolOperation(Expression):

    # region Dunder Methods
    def __init__(self, left: Expression, right: Expression,
                 op: EBoolOperationType, location: Location):
        super().__init__(location)
        self._left = left
        self._right = right
        self._op = op

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BoolOperation) \
            and self.left == other.left \
            and self.right == other.right \
            and self.op == other.op \
            and super().__eq__(other)

    # endregion

    # region Properties

    @property
    def left(self) -> Expression:
        return self._left

    @property
    def right(self) -> Expression:
        return self._right

    @property
    def op(self) -> EBoolOperationType:
        return self._op

    # endregion
