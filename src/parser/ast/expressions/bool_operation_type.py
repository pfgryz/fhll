from enum import Enum
from typing import Optional

from src.lexer.token_kind import TokenKind


class EBoolOperationType(Enum):
    And = "And"
    Or = "Or"

    @staticmethod
    def from_token_kind(kind: TokenKind) -> Optional['EBoolOperationType']:
        match kind:
            case TokenKind.And:
                return EBoolOperationType.And
            case TokenKind.Or:
                return EBoolOperationType.Or

        return None
