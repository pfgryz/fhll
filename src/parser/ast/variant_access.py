from dataclasses import dataclass

from src.parser.ast.name import Name
from src.parser.ast.node import Node

type VariantAccessParent = Name | 'VariantAccess'


@dataclass
class VariantAccess(Node):
    name: Name
    parent: VariantAccessParent
