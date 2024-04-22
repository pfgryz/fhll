from src.common.location import Location
from src.parser.ast.node import Node


class Name(Node):

    # region Dunder Methods

    def __init__(self, identifier: str, location: Location):
        super().__init__(location)

        self._identifier = identifier

    def __repr__(self) -> str:
        return "Name(identifier={}, location={})".format(
            repr(self.identifier),
            repr(self.location)
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other,
                          Name) and self.identifier == other.identifier

    # endregion

    # region Properties

    @property
    def identifier(self) -> str:
        return self._identifier

    # endregion
