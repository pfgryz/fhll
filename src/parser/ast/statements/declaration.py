from src.common.location import Location
from src.parser.ast.name import Name
from src.parser.ast.common import Type
from src.parser.ast.node import Node


class Declaration(Node):

    # region Dunder Methods
    def __init__(self, name: Name, mutable: bool, typ: Type,
                 value: 'Expression', location: Location):
        super().__init__(location)

        self._name = name
        self._mutable = mutable
        self._type = typ
        self._value = value

    def __repr__(self) -> str:
        return "Declacaration(name={}, mutable={}, typ={}, value={}, location={})".format(
            repr(self.name),
            repr(self.mutable),
            repr(self.type),
            repr(self.value),
            repr(self.location)
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Declaration) \
            and self.value == other.value

    # endregion

    # region Properties

    @property
    def name(self) -> Name:
        return self._name

    @property
    def mutable(self) -> bool:
        return self._mutable

    @property
    def type(self) -> Type:
        return self._type

    @property
    def value(self) -> 'Expression':
        return self._value

    # endregion
