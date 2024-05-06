from typing import Optional

from src.common.location import Location
from src.parser.ast.expressions.expression import Expression
from src.parser.ast.name import Name
from src.parser.ast.common import Type
from src.parser.ast.statements.statement import Statement


class VariableDeclaration(Statement):

    # region Dunder Methods

    def __init__(self, name: Name, mutable: bool, declared_type: Optional[Type],
                 value: Optional[Expression], location: Location):
        super().__init__(location)

        self._name = name
        self._mutable = mutable
        self._type = declared_type
        self._value = value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, VariableDeclaration) \
            and self.name == other.name \
            and self.mutable == other.mutable \
            and self.type == other.type \
            and self.value == other.value \
            and super().__eq__(other)

    # endregion

    # region Properties

    @property
    def name(self) -> Name:
        return self._name

    @property
    def mutable(self) -> bool:
        return self._mutable

    @property
    def type(self) -> Optional[Type]:
        return self._type

    @property
    def value(self) -> Optional[Expression]:
        return self._value

    # endregion
