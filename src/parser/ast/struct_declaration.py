from src.common.location import Location
from src.parser.ast.common import Type
from src.parser.ast.field_declaration import FieldDeclaration
from src.parser.ast.name import Name
from src.parser.ast.node import Node

type Fields = list[FieldDeclaration]


class StructDeclaration(Node):

    # region Dunder Methods
    def __init__(self, name: Name, fields: Fields, location: Location):
        super().__init__(location)
        self._name = name
        self._fields = fields

    def __repr__(self) -> str:
        return "StructDeclaration(name={}, fields={}, location={})".format(
            repr(self.name),
            repr(self.fields),
            repr(self.location)
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, StructDeclaration) \
            and self.name == other.name \
            and self.fields == other.fields

    # endregion

    # region Properties

    @property
    def name(self) -> Name:
        return self._name

    @property
    def fields(self) -> Fields:
        return self._fields

    # endregion
