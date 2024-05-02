from typing import Optional

from src.common.location import Location
from src.parser.ast.name import Name
from src.parser.ast.node import Node
from src.parser.ast.statements.assignment import Assignment
from src.parser.ast.variant_access import VariantAccess


class NewStructStatement(Node):

    # region Dunder Methods
    def __init__(self, variant: Name | VariantAccess,
                 field_assignments: list[Assignment], location: Location):
        super().__init__(location)

        self._variant = variant
        self._assignments = field_assignments

    def __repr__(self) -> str:
        return "NewStructStatement(value={}, location={})".format(
            repr(self.variant),
            repr(self.assignments),
            repr(self.location)
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, NewStructStatement) \
            and self.variant == other.variant \
            and self.assignments == other.assignments

    # endregion

    # region Properties

    @property
    def variant(self) -> Name | VariantAccess:
        return self._variant

    @property
    def assignments(self) -> list[Assignment]:
        return self._assignments

    # endregion
