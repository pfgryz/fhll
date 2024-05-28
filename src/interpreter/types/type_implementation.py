from abc import ABC, abstractmethod

from src.interpreter.types.type import Type


class TypeImplementation(ABC):

    @abstractmethod
    def as_type(self) -> Type:
        ...

    @abstractmethod
    def create(self, *args, **kwargs) -> 'TypeImplementation':
        ...
