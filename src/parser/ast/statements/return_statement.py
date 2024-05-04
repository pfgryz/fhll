from typing import Optional

from src.common.location import Location
from src.parser.ast.expressions.expression import Expression
from src.parser.ast.statements.statement import Statement


class ReturnStatement(Statement):

    # region Dunder Methods

    def __init__(self, value: Optional[Expression], location: Location):
        super().__init__(location)

        self._value = value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ReturnStatement) \
            and self.value == other.value \
            and super().__eq__(other)

    # endregion

    # region Properties

    @property
    def value(self) -> Optional['Expression']:
        return self._value

    # endregion
