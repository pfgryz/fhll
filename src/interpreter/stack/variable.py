from dataclasses import dataclass
from multiprocessing import Value


@dataclass
class Variable:
    mutable: bool
    value: Value
