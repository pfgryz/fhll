from dataclasses import dataclass

from src.parser.ast.expressions.term import Term


@dataclass
class Name(Term):
    identifier: str
