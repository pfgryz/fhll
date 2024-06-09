from typing import Any


class TypeName:

    def __init__(self, *args: str):
        self._path = args

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, TypeName) \
            and self._path == other._path

    def __hash__(self) -> int:
        return hash(self._path)

    def __repr__(self) -> str:
        return f"TypeName({', '.join(map(repr, self._path))})"

    def __str__(self) -> str:
        return "::".join(self._path)

    @property
    def path(self) -> tuple[str, ...]:
        return self._path

    def extend(self, element: str) -> 'TypeName':
        path = (*self._path, element)
        return TypeName(*path)

    @classmethod
    def parse(cls, name: str) -> 'TypeName':
        path = name.split("::")

        for element in path:
            if element[0].isdigit():
                raise ValueError("Following number")
            if any(not char.isalnum() for char in element):
                raise ValueError("Invalid character in TypeName")

        return TypeName(*path)
