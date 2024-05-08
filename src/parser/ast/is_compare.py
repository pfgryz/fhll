from src.common.location import Location
from src.parser.ast.common import Type
from src.parser.ast.expressions.expression import Expression
from src.parser.ast.expressions.term import Term


class IsCompare(Term):

    # region Dunder Methods

    def __init__(self, value: Expression, is_type: Type,
                 location: Location):
        super().__init__(location)

        self._value = value
        self._type = is_type

    def __eq__(self, other: object) -> bool:
        return isinstance(other, IsCompare) \
            and self.value == other.value \
            and self.type == other.type \
            and super().__eq__(other)

    # endregion

    # region Properties

    @property
    def value(self) -> Expression:
        return self._value

    @property
    def type(self) -> Type:
        return self._type

    # endregion
