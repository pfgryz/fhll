from typing import Callable, Optional

from src.interpreter.stack.value import Value

from src.interpreter.types.typename import TypeName

type Operations[X] = dict[
    X, dict[TypeName | str, dict[TypeName | str, Callable[..., Value]]]
]


class OperationRegistry[O]:

    # region Dunder Methods

    def __init__(self):
        self._star = TypeName("*")
        self._anchor = TypeName("&")
        self._operations: Operations[O | str] = {}

    # endregion

    # region Methods

    def get_operation(
            self,
            operator: O,
            base: TypeName,
            second: Optional[TypeName] = None,
    ) -> Optional[Callable[..., Value]]:
        operator_level = self._operations.get(operator, None) \
                         or self._operations.get("", None) \
                         or {}

        if (first_level := operator_level.get(self._star)) \
                and (result := first_level.get(self._anchor)) \
                and base == second:
            return result

        first_level = operator_level.get(base, None) \
                      or operator_level.get(self._star, None) \
                      or {}

        result = first_level.get(second, None) \
                 or first_level.get(self._star, None)

        return result

    def register_operation(
            self,
            operator: O,
            base: TypeName,
            second: Optional[TypeName],
            implementation: Callable[..., Value]
    ):
        if operator not in self._operations:
            self._operations[operator] = {}
        if base not in self._operations[operator]:
            self._operations[operator][base] = {}

        self._operations[operator][base][second] = implementation

# endregion
