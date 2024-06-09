from typing import Optional

from src.lexer.token_kind import TokenKind
from src.parser.interface.ifrom_token_kind import IFromTokenKind


class EBoolOperationType(IFromTokenKind):
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

    def to_operator(self) -> str:
        match self:
            case EBoolOperationType.And:
                return "&&"
            case EBoolOperationType.Or:
                return "||"
