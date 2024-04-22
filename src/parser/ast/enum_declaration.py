from src.common.location import Location
from src.parser.ast.name import Name
from src.parser.ast.node import Node
from src.parser.ast.struct_declaration import StructDeclaration

type Variants = list[StructDeclaration | 'EnumDeclaration']


class EnumDeclaration(Node):

    # region Dunder Methods
    def __init__(self, name: Name, variants: Variants, location: Location):
        super().__init__(location)
        self._name = name
        self._variants = variants

    def __repr__(self) -> str:
        return "EnumDeclaration(name={}, variants={}, location={})".format(
            repr(self.name),
            repr(self.variants),
            repr(self.location)
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, EnumDeclaration) \
            and self.name == other.name \
            and self.variants == other.variants

    # endregion

    # region Properties

    @property
    def name(self) -> Name:
        return self._name

    @property
    def variants(self) -> Variants:
        return self._variants

    # endregion
