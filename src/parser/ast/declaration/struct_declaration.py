from dataclasses import dataclass

from src.parser.ast.declaration.declaration import Declaration
from src.parser.ast.declaration.field_declaration import FieldDeclaration
from src.parser.ast.name import Name

type Fields = list[FieldDeclaration]


@dataclass
class StructDeclaration(Declaration):
    name: Name
    fields: Fields
