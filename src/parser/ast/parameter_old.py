from src.interface.inode import INode


class Parameter(INode):
    def __init__(self, name: str, types: 'types', mutable: bool = False):
        super().__init__()
        self._name = name
        self._types = types
        self._mutable = mutable

    def __repr__(self) -> str:
        return "Parameter(name={}, types={}, mutable={}".format(
            repr(self._name),
            repr(self._types),
            repr(self._mutable)
        )

    @property
    def name(self) -> str:
        return self._name

    @property
    def types(self) -> 'types':
        return self._types

    @property
    def mutable(self) -> bool:
        return self._mutable
