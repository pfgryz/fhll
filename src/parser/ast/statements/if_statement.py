from typing import Optional

from src.common.location import Location
from src.parser.ast.node import Node
from src.parser.ast.statements.block import Block


class IfStatement(Node):

    # region Dunder Methods
    def __init__(self, condition: 'Expression', block: Block,
                 else_block: Optional[Block], location: Location):
        super().__init__(location)

        self._condition = condition
        self._block = block
        self._else_block = else_block

    def __repr__(self) -> str:
        return "IfStatement(condition={}, body={}, else_body={}, location={})".format(
            repr(self.condition),
            repr(self.block),
            repr(self.else_block),
            repr(self.location)
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, IfStatement) \
            and self.condition == other.condition \
            and self.block == other.block \
            and self.else_block == other.else_block

    # endregion

    # region Properties

    @property
    def condition(self) -> 'Expression':
        return self._condition

    @property
    def block(self) -> Block:
        return self._block

    @property
    def else_block(self) -> Block:
        return self._else_block

    # endregion
