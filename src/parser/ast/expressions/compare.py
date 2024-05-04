from src.common.location import Location
from src.parser.ast.expressions.compare_type import ECompareType
from src.parser.ast.expressions.expression import Expression


class Compare(Expression):

    # region Dunder Methods
    def __init__(self, left: Expression, right: Expression,
                 mode: ECompareType, location: Location):
        super().__init__(location)
        self._left = left
        self._right = right
        self._mode = mode

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Compare) \
            and self.left == other.left \
            and self.right == other.right \
            and self.mode == other.mode \
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
    def mode(self) -> ECompareType:
        return self._mode

    # endregion
