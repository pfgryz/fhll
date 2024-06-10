from abc import ABC, abstractmethod

from src.interpreter.stack.value import Value
from src.interpreter.types.typename import TypeName


class TypeImplementation(ABC):

    @abstractmethod
    def as_type(self) -> TypeName:
        ...

    @abstractmethod
    def can_instantiate(self) -> bool:
        ...

    @abstractmethod
    def instantiate(self, *args, **kwargs) -> Value:
        ...
