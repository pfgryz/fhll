from dataclasses import dataclass

from src.parser.ast.expressions.term import Term

type ConstantValue = int | float | bool | str


@dataclass
class Constant(Term):
    value: ConstantValue
