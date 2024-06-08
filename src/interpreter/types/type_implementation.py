from abc import ABC, abstractmethod

from src.interpreter.types.typename import TypeName


class TypeImplementation(ABC):

    @abstractmethod
    def as_type(self) -> TypeName:
        ...

    @abstractmethod
    def instantiate(self, *args, **kwargs) -> 'TypeImplementation':
        ...