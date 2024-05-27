from abc import ABC, abstractmethod


class IVisitor[Visitable](ABC):

    @abstractmethod
    def visit(self, node: Visitable) -> None:
        ...
