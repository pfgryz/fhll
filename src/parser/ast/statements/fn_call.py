from dataclasses import dataclass

from src.parser.ast.expressions.expression import Expression
from src.parser.ast.expressions.term import Term
from src.parser.ast.name import Name
from src.parser.ast.statements.statement import Statement


@dataclass
class FnCall(Statement, Term):
    name: Name
    arguments: list[Expression]
