from enum import Enum
from typing import Optional

from src.lexer.token_kind import TokenKind


class ECompareMode(Enum):
    Equal = "Equal"
    NotEqual = "NotEqual"
    Less = "Less"
    Greater = "Greater"

    @staticmethod
    def from_token_kind(kind: TokenKind) -> Optional['ECompareMode']:
        match kind:
            case TokenKind.Equal:
                return ECompareMode.Equal
            case TokenKind.NotEqual:
                return ECompareMode.NotEqual
            case TokenKind.Less:
                return ECompareMode.Less
            case TokenKind.Greater:
                return ECompareMode.Greater

        return None
