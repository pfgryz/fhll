from typing import Optional


class Box[T]:

    # region Dunder Methods

    def __init__(self, default: Optional[T] = None):
        self._value = default
        self._group: list[Box] = []

    def __bool__(self) -> bool:
        return self._value is not None

    # endregion

    # region Properties

    @property
    def empty(self):
        return self._value is None

    # endregion

    # region Methods

    def put(self, value: T) -> None:
        self._value = value

    def value(self):
        return self._value

    def take(self) -> T:
        value = self._value

        self.clear()
        for neighbour in self._group:
            neighbour.clear()

        return value

    def clear(self):
        self._value = None

    def add_mutually_exclusive(self, neighbour: 'Box') -> None:
        self._group.append(neighbour)

    # endregion
