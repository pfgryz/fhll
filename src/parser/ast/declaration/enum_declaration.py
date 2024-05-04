from src.common.location import Location
from src.parser.ast.declaration.declaration import Declaration
from src.parser.ast.name import Name
from src.parser.ast.declaration.struct_declaration import StructDeclaration

type Variants = list[StructDeclaration | 'EnumDeclaration']


class EnumDeclaration(Declaration):

    # region Dunder Methods

    def __init__(self, name: Name, variants: Variants, location: Location):
        super().__init__(location)
        self._name = name
        self._variants = variants

    def __eq__(self, other: object) -> bool:
        return isinstance(other, EnumDeclaration) \
            and self.name == other.name \
            and self.variants == other.variants \
            and super().__eq__(other)

    # endregion

    # region Properties

    @property
    def name(self) -> Name:
        return self._name

    @property
    def variants(self) -> Variants:
        return self._variants

    # endregion
