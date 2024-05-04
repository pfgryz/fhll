from src.common.location import Location
from src.parser.ast.access import Access
from src.parser.ast.expressions.expression import Expression
from src.parser.ast.statements.statement import Statement


class Assignment(Statement):

    # region Dunder Methods

    def __init__(self, access: Access, value: Expression,
                 location: Location):
        super().__init__(location)

        self._access = access
        self._value = value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Assignment) \
            and self.access == other.access \
            and self.value == other.value \
            and super().__eq__(other)

    # endregion

    # region Properties

    @property
    def access(self) -> Access:
        return self._access

    @property
    def value(self) -> Expression:
        return self._value

    # endregion
