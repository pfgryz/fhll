from src.common.location import Location
from src.parser.ast.common import Type
from src.parser.ast.node import Node
from src.parser.ast.statements.block import Block


class Matcher(Node):

    # region Dunder Methods

    def __init__(self, checked_type: Type, block: Block, location: Location):
        super().__init__(location)

        self._type = checked_type
        self._block = block

    def __eq__(self, other) -> bool:
        return isinstance(other, Matcher) \
            and self.type == other.type \
            and self.block == other.block

    # endregion

    # region Properties

    @property
    def type(self) -> Type:
        return self._type

    @property
    def block(self) -> Block:
        return self._block

    # endregion
