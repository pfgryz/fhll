from abc import abstractmethod
from enum import Enum
from typing import Optional

from src.lexer.token_kind import TokenKind


class IFromTokenKind(Enum):

    @staticmethod
    @abstractmethod
    def from_token_kind(kind: TokenKind) -> Optional['IFromTokenKind']:
        ...
