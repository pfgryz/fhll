from src.common.location import Location
from src.parser.ast.access import Access
from src.parser.ast.common import Type
from src.parser.ast.node import Node


class Cast(Node):

    # region Dunder Methods
    def __init__(self, value: Access, typ: Type):
        super().__init__(Location(
            value.location.begin, typ.location.end
        ))

        self._value = value
        self._type = typ

    def __repr__(self) -> str:
        return "Cast(value={}, typ={})".format(
            repr(self.value),
            repr(self.type)
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Cast) \
            and self.value == other.value \
            and self.type == other.type

    # endregion

    # region Properties

    @property
    def value(self) -> Access:
        return self._value

    @property
    def type(self) -> Type:
        return self._type

    # endregion
