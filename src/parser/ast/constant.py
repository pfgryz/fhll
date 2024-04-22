from src.common.location import Location
from src.parser.ast.node import Node

type ConstantValue = int | float | bool | str


class Constant(Node):

    # region Dunder Methods
    def __init__(self, value: ConstantValue, location: Location):
        super().__init__(location)
        self._value = value

    def __repr__(self) -> str:
        return "Constant(value={}, location={})".format(
            repr(self.value),
            repr(self.location)
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Constant) \
            and self.value == other.value

    # endregion

    # region Properties

    @property
    def value(self) -> ConstantValue:
        return self._value

    # endregion
