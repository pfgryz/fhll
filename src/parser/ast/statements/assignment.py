from dataclasses import dataclass

from src.parser.ast.access import Access
from src.parser.ast.expressions.expression import Expression
from src.parser.ast.name import Name
from src.parser.ast.statements.statement import Statement


@dataclass
class Assignment(Statement):
    access: Name | Access
    value: Expression
