from abc import abstractmethod, ABC

from src.interface.ivisitor import IVisitor


class IVisitable(ABC):

    @abstractmethod
    def accept(self, visitor: IVisitor) -> None:
        pass
