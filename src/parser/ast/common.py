from src.parser.ast.name import Name
from src.parser.ast.variant_access import VariantAccess

type Type = Name | VariantAccess
type Parameters = list['Parameter']
