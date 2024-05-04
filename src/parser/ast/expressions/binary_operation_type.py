from typing import Optional

from src.lexer.token_kind import TokenKind
from src.parser.ast.ifrom_token_kind import IFromTokenKind


class EBinaryOperationType(IFromTokenKind):
    Add = "Add"
    Sub = "Sub"
    Multiply = "Multiply"
    Divide = "Divide"

    @staticmethod
    def from_token_kind(kind: TokenKind) -> Optional['EBinaryOperationType']:
        match kind:
            case TokenKind.Plus:
                return EBinaryOperationType.Add
            case TokenKind.Minus:
                return EBinaryOperationType.Sub
            case TokenKind.Multiply:
                return EBinaryOperationType.Multiply
            case TokenKind.Divide:
                return EBinaryOperationType.Divide

        return None
