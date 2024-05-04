from src.common.location import Location
from src.parser.ast.access import Access
from src.parser.ast.expressions.expression import Expression
from src.parser.ast.name import Name
from src.parser.ast.statements.statement import Statement


class Assignment(Statement):

    # region Dunder Methods

    def __init__(self, access: Name | Access, value: Expression,
                 location: Location):
        super().__init__(location)

        self._name = access
        self._value = value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Assignment) \
            and self.name == other.name \
            and self.value == other.value \
            and super().__eq__(other)

    # endregion

    # region Properties

    @property
    def name(self) -> Name | Access:
        return self._name

    @property
    def value(self) -> Expression:
        return self._value

    # endregion
