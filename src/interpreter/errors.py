from src.common.position import Position
from src.interpreter.types.typename import TypeName


# region Semantic Errors

class SemanticError(Exception):
    def __init__(self, message: str, position: Position):
        self.message = message
        self.position = position

        super().__init__(message)


class FieldRedeclarationError(SemanticError):
    def __init__(self, name: str, position: Position):
        message = f"Field \"{name}\" is already declared in this struct"
        super().__init__(message, position)


class UnknownTypeError(SemanticError):
    def __init__(self, name: TypeName, position: Position):
        message = f"Type {name} is not defined"
        super().__init__(message, position)


# endregion

# region Interpreter

class InterpreterError(Exception):
    def __init__(self, message: str):
        self.message = message

        super().__init__(self.message)


class InternalError(InterpreterError):
    def __init__(self, message: str):
        self.message = f"Internal error: {message}"
        super().__init__(self.message)

# endregion
