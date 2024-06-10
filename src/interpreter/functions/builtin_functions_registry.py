from src.interpreter.errors import PanicBreak
from src.interpreter.functions.functions_registry import FunctionsRegistry, \
    function_impl
from src.interpreter.stack.value import Value
from src.interpreter.types.builtin_types import BuiltinTypes


class BuiltinFunctionsRegistry(FunctionsRegistry):

    # region Dunder Methods

    def __init__(self):
        super().__init__()

    # endregion

    # region Builtin functions

    @staticmethod
    @function_impl("print", [("value", BuiltinTypes.STR)], None)
    def print(interpreter: 'Interpreter', value: Value[str]):
        print('STDOUT', value.value, end="")

    @staticmethod
    @function_impl("readStr", [], None)
    def read_str(*args):
        return Value(
            type_name=BuiltinTypes.STR,
            value=input()
        )

    @staticmethod
    @function_impl("panic", [("message", BuiltinTypes.STR)], None)
    def panic(_, message: Value[str], *args):
        raise PanicBreak(message.value)

    # endregion
