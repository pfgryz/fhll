from dataclasses import dataclass

from src.parser.ast.common import Type
from src.parser.ast.declaration.declaration import Declaration
from src.parser.ast.name import Name


@dataclass
class FieldDeclaration(Declaration):
    name: Name
    declared_type: Type
