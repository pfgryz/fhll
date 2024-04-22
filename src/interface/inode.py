from abc import abstractmethod, ABC

from src.interface.ivisitable import IVisitable


class INode(IVisitable):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass
