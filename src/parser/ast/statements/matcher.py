from dataclasses import dataclass

from src.parser.ast.common import Type
from src.parser.ast.name import Name
from src.parser.ast.node import Node
from src.parser.ast.statements.block import Block


@dataclass
class Matcher(Node):
    checked_type: Type
    name: Name
    block: Block
