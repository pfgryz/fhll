from dataclasses import dataclass

from src.parser.ast.common import Type
from src.parser.ast.expressions.expression import Expression
from src.parser.ast.expressions.term import Term


@dataclass
class Cast(Term):
    value: Expression
    to_type: Type
