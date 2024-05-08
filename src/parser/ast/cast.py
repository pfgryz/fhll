from src.common.location import Location
from src.parser.ast.access import Access
from src.parser.ast.common import Type
from src.parser.ast.expressions.term import Term
from src.parser.ast.name import Name


class Cast(Term):

    # region Dunder Methods

    def __init__(self, value: Name | Access, to_type: Type,
                 location: Location):
        super().__init__(location)

        self._value = value
        self._type = to_type

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Cast) \
            and self.value == other.value \
            and self.type == other.type \
            and super().__eq__(other)

    # endregion

    # region Properties

    @property
    def value(self) -> Access:
        return self._value

    @property
    def type(self) -> Type:
        return self._type

    # endregion
