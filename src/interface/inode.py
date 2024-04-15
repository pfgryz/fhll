from abc import abstractmethod, ABC


class INode(ABC):

    @abstractmethod
    def __repr__(self) -> str:
        pass
