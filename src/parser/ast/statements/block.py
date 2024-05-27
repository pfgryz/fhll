from dataclasses import dataclass

from src.parser.ast.node import Node
from src.parser.ast.statements.statement import Statement


@dataclass
class Block(Node):
    body: list[Statement]
