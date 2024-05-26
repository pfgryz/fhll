from typing import Optional

from src.parser.ast.expressions.term import Term
from src.parser.ast.name import Name

type AccessParent = Name | 'Access'


class Access(Term):
    name: Name
    parent: Optional[AccessParent]
