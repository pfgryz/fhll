from typing import Optional

from src.interpreter.stack.value import Value
from src.interpreter.types.type_implementation import TypeImplementation
from src.interpreter.types.typename import TypeName


class BuiltinI32Implementation(TypeImplementation):
    def as_type(self) -> TypeName:
        return TypeName("i32")

    def instantiate(self, value: Optional[int]) -> Value:
        return Value(
            type_name=self.as_type(),
            value=0 if value is None else value
        )
