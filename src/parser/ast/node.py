from dataclasses import dataclass

from src.common.location import Location


@dataclass
class Node:
    location: Location
