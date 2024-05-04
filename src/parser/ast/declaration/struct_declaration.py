from src.common.location import Location
from src.parser.ast.declaration.declaration import Declaration
from src.parser.ast.declaration.field_declaration import FieldDeclaration
from src.parser.ast.name import Name
from src.parser.ast.node import Node

type Fields = list[FieldDeclaration]


class StructDeclaration(Declaration):

    # region Dunder Methods

    def __init__(self, name: Name, fields: Fields, location: Location):
        super().__init__(location)
        self._name = name
        self._fields = fields

    def __eq__(self, other: object) -> bool:
        return isinstance(other, StructDeclaration) \
            and self.name == other.name \
            and self.fields == other.fields \
            and super().__eq__(other)

    # endregion

    # region Properties

    @property
    def name(self) -> Name:
        return self._name

    @property
    def fields(self) -> Fields:
        return self._fields

    # endregion
