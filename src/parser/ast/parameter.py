from src.common.location import Location
from src.parser.ast.common import Type
from src.parser.ast.name import Name
from src.parser.ast.node import Node


class Parameter(Node):

    # region Dunder Methods

    def __init__(self, name: Name, typ: Type, mutable: bool,
                 location: Location):
        super().__init__(location)

        self._name = name
        self._type = typ
        self._mutable = mutable

    def __repr__(self) -> str:
        return "Parameter(name={}, typ={}, mutable={}, location={}".format(
            repr(self.name),
            repr(self.type),
            repr(self.mutable),
            repr(self.location)
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Parameter) \
            and self.name == other.name \
            and self.type == other.type \
            and self.mutable == other.mutable

    # endregion

    # region Properties

    @property
    def name(self) -> Name:
        return self._name

    @property
    def type(self) -> Type:
        return self._type

    @property
    def mutable(self) -> bool:
        return self._mutable

    # endregion
