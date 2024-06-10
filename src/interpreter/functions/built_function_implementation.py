from typing import Optional, Callable

from src.interpreter.functions.ifunction_implementation import \
    IFunctionImplementation, Parameters
from src.interpreter.stack.value import Value
from src.interpreter.types.typename import TypeName


class BuiltinFunctionImplementation(IFunctionImplementation):

    # region Dunder Methods

    def __init__(
            self,
            name: str,
            parameters: Parameters,
            return_type: Optional[TypeName],
            implementation: Callable[['Interpreter', ...], Optional[Value]]
    ):
        self._name = name
        self._parameters = parameters
        self._return_type = return_type
        self._implementation = implementation

    # endregion

    # region Properties

    @property
    def name(self) -> str:
        return self._name

    @property
    def parameters(self) -> Parameters:
        return self._parameters

    @property
    def return_type(self) -> Optional[TypeName]:
        return self._return_type

    # endregion

    # region Methods

    def call(self, visitor: 'Interpreter') -> None:
        arguments = []

        for parameter in self._parameters:
            arguments.append(visitor.frame.get(parameter).value)

        visitor.value.put(
            self._implementation(visitor, *arguments)
        )

    # endregion
