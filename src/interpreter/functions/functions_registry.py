from typing import Optional

from src.common.position import Position
from src.common.registrable import Registrable
from src.interpreter.errors import FunctionRedeclarationError
from src.interpreter.functions.built_function_implementation import \
    BuiltinFunctionImplementation
from src.interpreter.functions.ifunction_implementation import \
    IFunctionImplementation
from src.interpreter.types.typename import TypeName

Functions = dict[str, IFunctionImplementation]


def function_impl(
        name: str,
        parameters: list[tuple[str, TypeName]],
        return_type: Optional[TypeName]
):
    def decorator(func):
        Registrable.register_func(
            func,
            lambda x: x.register_function(
                name,
                BuiltinFunctionImplementation(
                    name,
                    {
                        parameter_name: (True, parameter_type)
                        for (parameter_name, parameter_type) in parameters
                    },
                    return_type,
                    func
                ),
                Position(1, 1)
            )
        )
        return func

    return decorator


class FunctionsRegistry(Registrable):

    # region Dunder Methods

    def __init__(self):
        self._functions: Functions = {}

        super().__init__()

    # endregion

    # region Properties

    @property
    def functions(self) -> Functions:
        return self._functions

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
