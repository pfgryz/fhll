from dataclasses import dataclass
from functools import total_ordering


@dataclass
@total_ordering
class Position:
    """
    Class for storing character position in stream
    """
    line: int
    column: int

    def __str__(self) -> str:
        return f"{self.line}:{self.column}"

    def __eq__(self, other):
        return isinstance(other, Position) \
            and self.line == other.line \
            and self.column == other.column

    def __lt__(self, other):
        if not isinstance(other, Position):
            return False

        if self.line < other.line:
            return True

        if self.line == other.line:
            if self.column < other.column:
                return True

        return False

    def __le__(self, other):
        return self == other or self < other

    def __post_init__(self):
        if not isinstance(self.line, int):
            raise TypeError("Line number must be an integer")

        if not isinstance(self.column, int):
            raise TypeError("Line column must be an integer")

        if self.line < 1:
            raise ValueError("Line number must be greater than zero")

        if self.column < 1:
            raise ValueError("Column number must be greater than zero")
