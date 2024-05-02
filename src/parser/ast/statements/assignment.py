from typing import Optional

from src.common.location import Location
from src.parser.ast.access import Access
from src.parser.ast.name import Name
from src.parser.ast.node import Node


class Assignment(Node):

    # region Dunder Methods
    def __init__(self, access: Name | Access, value: 'Expression',
                 location: Location):
        super().__init__(location)

        self._access = access
        self._value = value

    def __repr__(self) -> str:
        return "Assignment(access={}, value={}, location={})".format(
            repr(self.access),
            repr(self.value),
            repr(self.location)
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Assignment) \
            and self.access == other.access \
            and self.value == other.value

    # endregion

    # region Properties

    @property
    def access(self) -> Access:
        return self._access

    @property
    def value(self) -> 'Expression':
        return self._value

    # endregion
