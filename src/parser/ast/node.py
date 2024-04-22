from abc import abstractmethod

from src.common.location import Location
from src.interface.inode import INode
from src.interface.ivisitor import IVisitor


class Node(INode):

    # region Dunder Methods
    def __init__(self, location: Location):
        self._location = location

    @abstractmethod
    def __repr__(self) -> str:
        return "Node(location={})".format(
            repr(self._location)
        )

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Node) and self.location == other.location

    # endregion

    # region Properties

    @property
    def location(self) -> Location:
        return self._location

    # endregion

    # region Methods

    def accept(self, visitor: IVisitor) -> None:
        visitor.visit(self)

    # endregion
