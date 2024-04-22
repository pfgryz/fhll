from abc import ABC, abstractmethod


class IVisitor(ABC):

    @abstractmethod
    def visit(self, node) -> None:
        pass
