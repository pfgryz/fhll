from abc import abstractmethod, ABC
from dataclasses import dataclass

from src.common.location import Location
from src.parser.ast.expressions.expression import Expression
from src.parser.interface.ifrom_token_kind import IFromTokenKind


@dataclass
class ITreeLikeExpression(ABC):
    left: Expression
    right: Expression
    op: IFromTokenKind
    location: Location
