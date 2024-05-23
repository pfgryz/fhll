from typing import Optional, Any


class Type:

    def __init__(self, *args: str):
        self._path = args

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Type) \
            and self._path == other._path

    def __hash__(self) -> int:
        return hash(self._path)

    def __repr__(self) -> str:
        return f"Type({', '.join(map(repr, self._path))})"

    @property
    def path(self) -> tuple[str, ...]:
        return self._path

    def extend(self, element: str) -> 'Type':
        self._path = (*self._path, element)
        return self


class HType:
    ...


class HTypeProxy:

    def __init__(self, typ: Optional[HType]) -> None:
        self._typ = typ

    def get(self) -> HType:
        if self._typ is None:
            raise RuntimeError("Unresolved type")

        return self._typ
