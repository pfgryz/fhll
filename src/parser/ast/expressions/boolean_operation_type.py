from enum import Enum
from typing import Optional

from src.lexer.token_kind import TokenKind


class BooleanOperationType(Enum):
    And = "And"
    Or = "Or"

    @staticmethod
    def from_token_kind(kind: TokenKind) -> Optional['BooleanOperationType']:
        match kind:
            case TokenKind.And:
                return BooleanOperationType.And
            case TokenKind.Or:
                return BooleanOperationType.Or

        return None
