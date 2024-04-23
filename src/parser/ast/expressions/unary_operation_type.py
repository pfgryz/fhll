from enum import Enum
from typing import Optional

from src.lexer.token_kind import TokenKind


class EUnaryOperationType(Enum):
    Minus = "Minus"
    Negate = "Negate"

    @staticmethod
    def from_token_kind(kind: TokenKind) -> Optional['EUnaryOperationType']:
        match kind:
            case TokenKind.Minus:
                return EUnaryOperationType.Minus
            case TokenKind.Negate:
                return EUnaryOperationType.Negate

        return None
