from typing import Optional

from src.common.location import Location
from src.parser.ast.expressions.term import Term
from src.parser.ast.name import Name

type AccessParent = Name | 'Access'


class Access(Term):

    # region Dunder Methods

    def __init__(self, name: Name, parent: Optional[AccessParent],
                 location: Location):
        super().__init__(location)

        self._name = name
        self._parent = parent

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Access) \
            and self.name == other.name \
            and self.parent == other.parent \
            and super().__eq__(other)

    # endregion

    # region Properties

    @property
    def name(self) -> Name:
        return self._name

    @property
    def parent(self) -> Optional[AccessParent]:
        return self._parent

    # endregion
