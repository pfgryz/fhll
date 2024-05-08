from abc import abstractmethod, ABC

from src.common.location import Location
from src.parser.ast.expressions.expression import Expression
from src.parser.interface.ifrom_token_kind import IFromTokenKind


class ITreeLikeExpression(ABC):

    @abstractmethod
    def __init__(
            self, left: Expression, right: Expression, op: IFromTokenKind,
            location: Location
    ):
        pass
