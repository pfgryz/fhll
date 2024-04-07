from typing import Optional

from src.location import Location
from src.token_kind import TokenKind


class Token[T: (int, float, bool, str, None)]:

    # region Dunder Methods

    def __init__(self, kind: TokenKind, location: Location,
                 value: Optional[T] = None):
        self._kind = kind
        self._value = value
        self._location = location

    def __str__(self) -> str:
        position = f"{self._location.begin.line}:{self._location.begin.column}"
        return f"{self._kind.value}({repr(self._value)}) at <{position}>"

    def __repr__(self) -> str:
        return (f"Token(kind={self._kind}, "
                f"location={repr(self._location)}, "
                f"value={repr(self._value)})")

    # endregion

    # region Properties

    @property
    def kind(self) -> TokenKind:
        return self._kind

    @property
    def value(self) -> Optional[T]:
        return self._value

    @property
    def location(self):
        return self._location

    # endregion
