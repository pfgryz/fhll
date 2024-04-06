from dataclasses import dataclass


@dataclass
class Position:
    line: int
    column: int

    def __post_init__(self):
        if not isinstance(self.line, int):
            raise TypeError("Line number must be an integer")

        if not isinstance(self.column, int):
            raise TypeError("Line column must be an integer")

        if self.line < 1:
            raise ValueError("Line number must be greater than zero")

        if self.column < 1:
            raise ValueError("Column number must be greater than zero")
