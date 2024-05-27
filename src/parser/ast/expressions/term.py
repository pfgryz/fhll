from abc import ABC

from src.parser.ast.expressions.expression import Expression


class Term(Expression, ABC):
    ...
