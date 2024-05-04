from src.common.location import Location
from src.parser.ast.expressions.term import Term

type ConstantValue = int | float | bool | str


class Constant(Term):

    # region Dunder Methods

    def __init__(self, value: ConstantValue, location: Location):
        super().__init__(location)
        self._value = value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Constant) \
            and self.value == other.value \
            and super().__eq__(other)

    # endregion

    # region Properties

    @property
    def value(self) -> ConstantValue:
        return self._value

    # endregion
