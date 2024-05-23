from typing import Optional


class Box[T]:

    def __init__(self, default: Optional[T] = None):
        self._value = default

    def __bool__(self) -> bool:
        return self._value is not None

    def put(self, value: T) -> None:
        self._value = value

    def take(self) -> T:
        value, self._value = self._value, None
        return value
