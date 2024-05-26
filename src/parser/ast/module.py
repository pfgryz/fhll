from dataclasses import dataclass

from src.parser.ast.declaration.enum_declaration import EnumDeclaration
from src.parser.ast.declaration.function_declaration import FunctionDeclaration
from src.parser.ast.declaration.struct_declaration import StructDeclaration
from src.parser.ast.node import Node


@dataclass
class Module(Node):
    name: str
    path: str
    function_declarations: list[FunctionDeclaration]
    struct_declarations: list[StructDeclaration]
    enum_declarations: list[EnumDeclaration]
