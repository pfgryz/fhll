from abc import ABC

from src.parser.ast.expressions.term import Term


class Expression(Term, ABC):
    pass
