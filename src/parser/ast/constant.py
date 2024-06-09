from dataclasses import dataclass
from enum import Enum

from src.lexer.token_kind import TokenKind
from src.parser.ast.expressions.term import Term

type ConstantValue = int | float | bool | str


class ConstantValueType(Enum):
    I32 = "i32"
    F32 = "f32"
    Str = "str"
    Bool = "bool"

    @classmethod
    def from_token_kind(cls, token_kind: TokenKind) -> 'ConstantValueType':
        match token_kind:
            case TokenKind.Integer:
                return cls.I32
            case TokenKind.Float:
                return cls.F32
            case TokenKind.String:
                return cls.Str
            case TokenKind.Boolean:
                return cls.Bool
            case _:
                raise ValueError(f"Unknown token kind {token_kind}")

    def to_name(self) -> str:
        return self.value


@dataclass
class Constant(Term):
    value: ConstantValue
    type: ConstantValueType
