from src.common.location import Location
from src.parser.ast.node import Node


class Expression(Node):

    # region Dunder Methods

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Expression) \
            and super().__eq__(other)

    # endregion
