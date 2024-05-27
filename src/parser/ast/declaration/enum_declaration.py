from dataclasses import dataclass

from src.parser.ast.declaration.declaration import Declaration
from src.parser.ast.name import Name
from src.parser.ast.declaration.struct_declaration import StructDeclaration

type Variants = list[StructDeclaration | 'EnumDeclaration']


@dataclass
class EnumDeclaration(Declaration):
    name: Name
    variants: Variants
