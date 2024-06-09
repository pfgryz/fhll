from typing import Any


class PathLike:
    symbol = "/"

    def __init__(self, *args: str):
        self._path = args

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, PathLike) and \
            self._path == other._path

    def __hash__(self) -> int:
        return hash(self._path)

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"{name}({', '.join(map(repr, self._path))})"

    def __str__(self) -> str:
        return f"{self.symbol}".join(self._path)

    @property
    def path(self) -> tuple[str, ...]:
        return self._path

    def extend(self, element: str) -> 'PathLike':
        path = (*self._path, element)
        return self.__class__(*path)

    @classmethod
    def parse(cls, name: str) -> 'PathLike':
        path = name.split(cls.symbol)

        for element in path:
            if element[0].isdigit():
                raise ValueError("Following number")
            if any(not (char.isalnum() or char == "_") for char in element):
                raise ValueError("Invalid character in TypeName")

        return cls(*path)
