from src.common.location import Location
from src.parser.ast.node import Node


class Block(Node):
    # region Dunder Methods
    def __init__(self, body: list['Statement'], location: Location):
        super().__init__(location)

        self._body = body

    def __repr__(self) -> str:
        return "Block(body={}, location={})".format(
            repr(self.body),
            repr(self.location)
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Block) \
            and self.body == other.body

    # endregion

    # region Properties

    @property
    def body(self) -> list['Statement']:
        return self._body

    # endregion
