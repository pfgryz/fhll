from dataclasses import dataclass

from src.parser.ast.common import Type
from src.parser.ast.expressions.expression import Expression
from src.parser.ast.expressions.term import Term


@dataclass
class IsCompare(Term):
    value: Expression
    is_type: Type
