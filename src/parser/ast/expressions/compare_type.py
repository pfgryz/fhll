from typing import Optional

from src.lexer.token_kind import TokenKind
from src.parser.interface.ifrom_token_kind import IFromTokenKind


class ECompareType(IFromTokenKind):
    Equal = "Equal"
    NotEqual = "NotEqual"
    Less = "Less"
    Greater = "Greater"

    @staticmethod
    def from_token_kind(kind: TokenKind) -> Optional['ECompareType']:
        match kind:
            case TokenKind.Equal:
                return ECompareType.Equal
            case TokenKind.NotEqual:
                return ECompareType.NotEqual
            case TokenKind.Less:
                return ECompareType.Less
            case TokenKind.Greater:
                return ECompareType.Greater

        return None

    def to_operator(self) -> str:
        match self:
            case ECompareType.Equal:
                return "=="
            case ECompareType.NotEqual:
                return "!="
            case ECompareType.Less:
                return "<"
            case ECompareType.Greater:
                return ">"
