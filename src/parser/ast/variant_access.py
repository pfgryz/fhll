from src.common.location import Location
from src.parser.ast.name import Name
from src.parser.ast.node import Node

type VariantAccessParent = Name | 'VariantAccess'


class VariantAccess(Node):

    # region Dunder Methods
    def __init__(self, name: Name, parent: VariantAccessParent):
        super().__init__(Location(
            parent.location.begin,
            name.location.end
        ))

        self._name = name
        self._parent = parent

    def __repr__(self) -> str:
        return "VariantAccess(name={}, parent={}, location={})".format(
            repr(self.name),
            repr(self.parent),
            repr(self.location)
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, VariantAccess) \
            and self._name == other._name \
            and self._parent == other._parent

    # endregion

    # region Properties

    @property
    def name(self) -> Name:
        return self._name

    @property
    def parent(self) -> VariantAccessParent:
        return self._parent

    # endregion
