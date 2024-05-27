from dataclasses import dataclass

from src.parser.ast.expressions.expression import Expression
from src.parser.ast.statements.matcher import Matcher
from src.parser.ast.statements.statement import Statement


@dataclass
class MatchStatement(Statement):
    expression: Expression
    matchers: list[Matcher]
