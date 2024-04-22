from src.common.location import Location
from src.parser.ast.common import Type
from src.parser.ast.name import Name
from src.parser.ast.node import Node


class FieldDeclaration(Node):

    # region Dunder Methods
    def __init__(self, name: Name, typ: Type):
        super().__init__(Location(
            name.location.begin,
            typ.location.end
        ))
        self._name = name
        self._type = typ

    def __repr__(self) -> str:
        return "FieldDeclaration(name={}, typ={})".format(
            repr(self.name),
            repr(self.type)
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FieldDeclaration) \
            and self.name == other.name \
            and self.type == other.type

    # endregion

    # region Properties

    @property
    def name(self) -> Name:
        return self._name

    @property
    def type(self) -> Type:
        return self._type

    # endregion
