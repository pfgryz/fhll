from dataclasses import dataclass

from src.lexer.position import Position


@dataclass
class Location:
    """
    Class for storing token location in stream
    """
    begin: Position
    end: Position

    def __post_init__(self):
        if not isinstance(self.begin, Position):
            raise TypeError("Begin position must be an instance of Position")

        if not isinstance(self.end, Position):
            raise TypeError("End position must be an instance of Position")

        if self.begin.line > self.end.line:
            raise ValueError("Begin position must be before end position")

        if self.begin.line == self.end.line:
            if self.begin.column > self.end.column:
                raise ValueError("Begin position must be before end position")

    @classmethod
    def at(cls, position: Position) -> 'Location':
        """
        Location begins and ends in same position
        :param position: begin position
        :return: location
        """
        return cls(position, position)
