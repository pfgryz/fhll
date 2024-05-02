from src.common.location import Location
from src.parser.ast.name import Name
from src.parser.ast.node import Node


class FnCall(Node):

    # region Dunder Methods
    def __init__(self, name: Name, arguments: list['Expression'],
                 location: Location):
        super().__init__(location)

        self._name = name
        self._arguments = arguments

    def __repr__(self) -> str:
        return "FnCall(name={}, arguments={}, location={})".format(
            repr(self.name),
            repr(self.arguments),
            repr(self.location)
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FnCall) \
            and self.name == other.name \
            and self.arguments == other.arguments

    # endregion

    # region Properties

    @property
    def name(self) -> Name:
        return self._name

    @property
    def arguments(self) -> list['Expression']:
        return self._arguments

    # endregion
