from abc import abstractmethod

from src.common.location import Location
from src.interface.inode import INode
from src.interface.ivisitor import IVisitor


class Node(INode):

    # region Dunder Methods
    def __init__(self, location: Location):
        self._location = location

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Node)

    # endregion

    # region Properties

    @property
    def location(self) -> Location:
        return self._location

    # endregion
