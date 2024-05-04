from abc import abstractmethod, ABC

from src.interface.ivisitor import IVisitable


class INode(IVisitable):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass
