from src.common.location import Location
from src.parser.ast.expressions.compare_type import ECompareMode
from src.parser.ast.node import Node


class Compare(Node):

    # region Dunder Methods
    def __init__(self, left: 'Expression', right: 'Expression',
                 mode: ECompareMode, location: Location):
        super().__init__(location)
        self._left = left
        self._right = right
        self._mode = mode

    def __repr__(self) -> str:
        return ("CompareOperation"
                "(left={}, right={}, mode={}, location={})").format(
            repr(self.left),
            repr(self.right),
            repr(self.mode),
            repr(self.location)
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Compare) \
            and self.left == other.left \
            and self.right == other.right \
            and self.mode == other.mode

    # endregion

    # region Properties

    @property
    def left(self) -> 'Expression':
        return self._left

    @property
    def right(self) -> 'Expression':
        return self._right

    @property
    def mode(self) -> ECompareMode:
        return self._mode

    # endregion
