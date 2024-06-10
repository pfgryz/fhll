from enum import Enum

from src.interpreter.types.typename import TypeName


class BuiltinTypes:
    I32 = TypeName("i32")
    F32 = TypeName("f32")
    STR = TypeName("str")
    BOOL = TypeName("bool")
