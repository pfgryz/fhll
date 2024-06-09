from src.common.position import Position
from src.interpreter.errors import FunctionRedeclarationError
from src.interpreter.functions.ifunction_implementation import \
    IFunctionImplementation


class FunctionsRegistry:

    # region Dunder Methods

    def __init__(self):
        self._functions: dict[str, IFunctionImplementation] = {}

    # endregion

    # region Methods

    def get_function(self, name: str) -> IFunctionImplementation:
        return self._functions.get(name)

    def register_function(
            self,
            name: str,
            function: IFunctionImplementation,
            position: Position
    ):
        if name in self._functions:
            raise FunctionRedeclarationError(name, position)

        self._functions[name] = function

    # endregion
