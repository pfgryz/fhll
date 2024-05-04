from abc import ABC, abstractmethod


class IVisitor(ABC):

    @abstractmethod
    def visit(self, node: 'IVisitable') -> None:
        pass


class IVisitable(ABC):

    @abstractmethod
    def accept(self, visitor: IVisitor) -> None:
        pass
