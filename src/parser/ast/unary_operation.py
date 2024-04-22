from src.parser.ast.node import Node


class UnaryOperation(Node):

    # region Dunder Methods
    def __init__(self, operand: Term, op: UOperation):
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
