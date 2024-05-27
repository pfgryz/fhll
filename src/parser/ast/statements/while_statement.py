from dataclasses import dataclass

from src.parser.ast.expressions.expression import Expression
from src.parser.ast.statements.block import Block
from src.parser.ast.statements.statement import Statement


@dataclass
class WhileStatement(Statement):
    condition: Expression
    block: Block
