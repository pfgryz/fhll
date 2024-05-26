from dataclasses import dataclass

from src.common.location import Location
from src.interface.inode import INode


@dataclass
class Node(INode):
    location: Location
