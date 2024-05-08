from src.common.location import Location
from src.parser.ast.expressions.expression import Expression
from src.parser.ast.statements.matcher import Matcher
from src.parser.ast.statements.statement import Statement


class MatchStatement(Statement):

    # region Dunder Methods

    def __init__(self, expression: Expression, matchers: list[Matcher],
                 location: Location):
        super().__init__(location)

        self._expression = expression
        self._matchers = matchers

    def __eq__(self, other):
        return isinstance(other, MatchStatement) \
            and self.expression == other.expression \
            and self.matchers == other.matchers

    # endregion

    # region Properties

    @property
    def expression(self) -> Expression:
        return self._expression

    @property
    def matchers(self) -> list[Matcher]:
        return self._matchers

    # endregion
