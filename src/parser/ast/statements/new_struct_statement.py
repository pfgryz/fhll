from dataclasses import dataclass

from src.parser.ast.expressions.term import Term
from src.parser.ast.name import Name
from src.parser.ast.statements.assignment import Assignment
from src.parser.ast.statements.statement import Statement
from src.parser.ast.variant_access import VariantAccess


@dataclass
class NewStruct(Statement, Term):
    variant: Name | VariantAccess | Assignment
    assignments: list[Assignment]
