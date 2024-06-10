from dataclasses import dataclass
from src.interpreter.stack.value import Value


@dataclass
class Variable:
    mutable: bool
    value: Value
