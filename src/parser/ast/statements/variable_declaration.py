from dataclasses import dataclass
from typing import Optional

from src.parser.ast.expressions.expression import Expression
from src.parser.ast.name import Name
from src.parser.ast.common import Type
from src.parser.ast.statements.statement import Statement


@dataclass
class VariableDeclaration(Statement):
    name: Name
    mutable: bool
    declared_type: Optional[Type]
    value: Optional[Expression]
