from abc import ABC, abstractmethod

from src.interpreter.types.typename import TypeName
from src.interpreter.types_old.type_implementation import TypeImplementation


class TypeImplementation(ABC):

    @abstractmethod
    def as_type(self) -> TypeName:
        ...

    @abstractmethod
    def instantiate(self, *args, **kwargs) -> TypeImplementation:
        ...
