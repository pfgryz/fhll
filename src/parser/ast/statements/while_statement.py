from src.common.location import Location
from src.parser.ast.node import Node
from src.parser.ast.statements.block import Block


class WhileStatement(Node):

    # region Dunder Methods
    def __init__(self, condition: 'Expression', block: Block,
                 location: Location):
        super().__init__(location)

        self._condition = condition
        self._block = block

    def __repr__(self) -> str:
        return "WhileStatement(condition={}, block={}, location={})".format(
            repr(self.condition),
            repr(self.block),
            repr(self.location)
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, WhileStatement) \
            and self.condition == other.condition \
            and self.block == other.block

    # endregion

    # region Properties

    @property
    def condition(self) -> 'Expression':
        return self._condition

    @property
    def block(self) -> Block:
        return self._block

    # endregion
