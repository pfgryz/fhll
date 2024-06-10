from dataclasses import dataclass

from src.interpreter.types.typename import TypeName


@dataclass
class Value[T: object]:
    type_name: TypeName
    value: T
