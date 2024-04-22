from src.common.location import Location
from src.parser.ast.name import Name
from src.parser.ast.node import Node

type AccessParent = Name | 'Access'


class Access(Node):

    # region Dunder Methods
    def __init__(self, name: Name, parent: AccessParent):
        super().__init__(Location(
            parent.location.begin,
            name.location.end
        ))

        self._name = name
        self._parent = parent

    def __repr__(self) -> str:
        return "Access(name={}, parent={}, location={})".format(
            repr(self.name),
            repr(self.parent),
            repr(self.location)
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Access) \
            and self._name == other._name \
            and self._parent == other._parent

    # endregion

    # region Properties

    @property
    def name(self) -> Name:
        return self._name

    @property
    def parent(self) -> AccessParent:
        return self._parent

    # endregion
