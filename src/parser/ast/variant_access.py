from src.common.location import Location
from src.parser.ast.name import Name
from src.parser.ast.node import Node

type VariantAccessParent = Name | 'VariantAccess'


class VariantAccess(Node):

    # region Dunder Methods

    def __init__(self, name: Name, parent: VariantAccessParent,
                 location: Location):
        super().__init__(location)

        self._name = name
        self._parent = parent

    def __eq__(self, other: object) -> bool:
        return isinstance(other, VariantAccess) \
            and self.name == other.name \
            and self.parent == other.parent \
            and super().__eq__(other)

    # endregion

    # region Properties

    @property
    def name(self) -> Name:
        return self._name

    @property
    def parent(self) -> VariantAccessParent:
        return self._parent

    # endregion
