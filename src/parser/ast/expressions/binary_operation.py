from src.common.location import Location
from src.parser.ast.expressions.binary_operation_type import \
    EBinaryOperationType
from src.parser.ast.expressions.expression import Expression
from src.parser.interface.itree_like_expression import ITreeLikeExpression


class BinaryOperation(Expression, ITreeLikeExpression):

    # region Dunder Methods

    def __init__(self, left: Expression, right: Expression,
                 op: EBinaryOperationType, location: Location):
        super().__init__(location)
        self._left = left
        self._right = right
        self._op = op

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BinaryOperation) \
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
    def op(self) -> EBinaryOperationType:
        return self._op

    # endregion
