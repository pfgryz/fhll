from dataclasses import dataclass

from src.parser.ast.common import Type
from src.parser.ast.name import Name
from src.parser.ast.node import Node


@dataclass
class Parameter(Node):
    name: Name
    declared_type: Type
    mutable: bool
