from dataclasses import dataclass

from src.interpreter.types.typename import TypeName


@dataclass
class Value:
    type_name: TypeName
    value: object
