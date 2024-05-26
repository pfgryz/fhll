from abc import ABC, abstractmethod


class IVisitor(ABC):

    @abstractmethod
    def visit(self, node: 'IVisitable') -> None:
        pass


class IVisitable(ABC):
    pass
