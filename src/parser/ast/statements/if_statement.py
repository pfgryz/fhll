from dataclasses import dataclass
from typing import Optional

from src.parser.ast.expressions.expression import Expression
from src.parser.ast.statements.block import Block
from src.parser.ast.statements.statement import Statement


@dataclass
class IfStatement(Statement):
    condition: Expression
    block: Block
    else_block: Optional[Block]
