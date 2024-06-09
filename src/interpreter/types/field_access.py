from src.interpreter.types.pathlike import PathLike


class FieldAccess(PathLike):
    symbol = "."

    def to_name(self) -> str:
        if len(self._path) == 0:
            raise ValueError("Access is empty")

        return self._path[0]

    def is_access(self) -> bool:
        return len(self._path) > 1
