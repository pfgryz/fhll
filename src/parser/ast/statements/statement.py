from src.parser.ast.node import Node


class Statement(Node):

    # region Dunder Methods

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Statement) \
            and super().__eq__(other)

    # endregion
