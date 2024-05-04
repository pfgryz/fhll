from src.common.location import Location
from src.parser.ast.expressions.expression import Expression
from src.parser.ast.statements.block import Block
from src.parser.ast.statements.statement import Statement


class WhileStatement(Statement):

    # region Dunder Methods

    def __init__(self, condition: Expression, block: Block,
                 location: Location):
        super().__init__(location)

        self._condition = condition
        self._block = block

    def __eq__(self, other: object) -> bool:
        return isinstance(other, WhileStatement) \
            and self.condition == other.condition \
            and self.block == other.block \
            and super().__eq__(other)

    # endregion

    # region Properties

    @property
    def condition(self) -> Expression:
        return self._condition

    @property
    def block(self) -> Block:
        return self._block

    # endregion
