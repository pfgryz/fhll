from typing import Optional


class Context[K, V]:

    # region Dunder Methods

    def __init__(self, parent: Optional['Context[K, V]'] = None,
                 store: dict = None):
        self._store = store if store is not None else {}
        self._parent = parent

    def __len__(self) -> int:
        parent_len = 0 if self._parent is None else len(self._parent)

        return len(self._store) + parent_len

    def __contains__(self, key: K) -> bool:
        if key in self._store:
            return True

        if self._parent is not None:
            return self._parent.__contains__(key)

        return False

    def __getitem__(self, key: K) -> Optional[V]:
        if key not in self:
            raise KeyError(key)

        return self.get(key)

    def __setitem__(self, key: K, value: V) -> None:
        return self.set(key, value)

    # endregion

    # region Methods

    def keys(self, chain: bool = True) -> list[K]:
        if not chain or self._parent is None:
            return list(self._store.keys())

        return list(self._store.keys()) + self._parent.keys()

    def values(self, chain: bool = True) -> list[V]:
        if not chain or self._parent is None:
            return list(self._store.values())

        return list(self._store.values()) + self._parent.values()

    def items(self, chain: bool = True) -> list[tuple[K, V]]:
        if not chain or self._parent is None:
            return list(self._store.items())

        return list(self._store.items()) + self._parent.items()

    def get(self, key: K, default: Optional[V] = None,
            chain: bool = True) -> V:
        if key in self._store or not chain or self._parent is None:
            return self._store.get(key, default)

        return self._parent.get(key, default)

    def set(self, key: K, value: V, chain: bool = True) -> None:
        if self._parent is not None and chain:
            if key in self._parent:
                self._parent.set(key, value)
                return

        self._store[key] = value

    # endregion

