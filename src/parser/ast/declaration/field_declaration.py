from src.common.location import Location
from src.parser.ast.common import Type
from src.parser.ast.declaration.declaration import Declaration
from src.parser.ast.name import Name


class FieldDeclaration(Declaration):

    # region Dunder Methods

    def __init__(self, name: Name, declared_type: Type, location: Location):
        super().__init__(location)
        self._name = name
        self._type = declared_type

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FieldDeclaration) \
            and self.name == other.name \
            and self.type == other.type \
            and super().__eq__(other)

    # endregion

    # region Properties

    @property
    def name(self) -> Name:
        return self._name

    @property
    def type(self) -> Type:
        return self._type

    # endregion
