from dataclasses import dataclass
from typing import Optional

from src.parser.ast.expressions.expression import Expression
from src.parser.ast.statements.statement import Statement


@dataclass
class ReturnStatement(Statement):
    value: Optional[Expression]
