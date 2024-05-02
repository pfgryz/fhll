from typing import Optional

from src.common.location import Location
from src.parser.ast.node import Node


class ReturnStatement(Node):

    # region Dunder Methods
    def __init__(self, value: Optional['Expression'], location: Location):
        super().__init__(location)

        self._value = value

    def __repr__(self) -> str:
        return "ReturnStatement(value={}, location={})".format(
            repr(self.value),
            repr(self.location)
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ReturnStatement) \
            and self.value == other.value

    # endregion

    # region Properties

    @property
    def value(self) -> Optional['Expression']:
        return self._value

    # endregion
