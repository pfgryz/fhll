from typing import Optional

from src.interpreter.stack.value import Value
from src.interpreter.types.builtin_types import BuiltinTypes
from src.interpreter.types.type_implementation import TypeImplementation
from src.interpreter.types.typename import TypeName


class BuiltinI32Implementation(TypeImplementation):
    def as_type(self) -> TypeName:
        return BuiltinTypes.I32

    def can_instantiate(self) -> bool:
        return True

    def instantiate(self, value: Optional[int] = None) -> Value[int]:
        return Value(
            type_name=self.as_type(),
            value=0 if value is None else value
        )


class BuiltinF32Implementation(TypeImplementation):
    def as_type(self) -> TypeName:
        return BuiltinTypes.F32

    def can_instantiate(self) -> bool:
        return True

    def instantiate(self, value: Optional[float] = None) -> Value[float]:
        return Value(
            type_name=self.as_type(),
            value=0.0 if value is None else value
        )


class BuiltinStrImplementation(TypeImplementation):
    def as_type(self) -> TypeName:
        return BuiltinTypes.STR

    def can_instantiate(self) -> bool:
        return True

    def instantiate(self, value: Optional[str] = None) -> Value[str]:
        return Value(
            type_name=self.as_type(),
            value="" if value is None else value
        )


class BuiltinBoolImplementation(TypeImplementation):
    def as_type(self) -> TypeName:
        return BuiltinTypes.BOOL

    def can_instantiate(self) -> bool:
        return True

    def instantiate(self, value: Optional[bool] = None) -> Value[bool]:
        return Value(
            type_name=self.as_type(),
            value=False if value is None else value
        )
