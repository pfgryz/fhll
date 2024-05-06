from src.common.location import Location
from src.parser.ast.expressions.term import Term
from src.parser.ast.node import Node


class Name(Term):

    # region Dunder Methods

    def __init__(self, identifier: str, location: Location):
        super().__init__(location)

        self._identifier = identifier

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Name) \
            and self.identifier == other.identifier \
            and super().__eq__(other)

    # endregion

    # region Properties

    @property
    def identifier(self) -> str:
        return self._identifier

    # endregion
