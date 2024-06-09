from typing import Optional

from src.lexer.token_kind import TokenKind
from src.parser.interface.ifrom_token_kind import IFromTokenKind


class EUnaryOperationType(IFromTokenKind):
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

    def to_operator(self) -> str:
        match self:
            case EUnaryOperationType.Minus:
                return "-"
            case EUnaryOperationType.Negate:
                return "!"
