from src.common.location import Location
from src.parser.ast.node import Node
from src.parser.ast.statements.statement import Statement


class Block(Node):

    # region Dunder Methods

    def __init__(self, body: list[Statement], location: Location):
        super().__init__(location)

        self._body = body

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Block) \
            and self.body == other.body \
            and super().__eq__(other)

    # endregion

    # region Properties

    @property
    def body(self) -> list[Statement]:
        return self._body

    # endregion
