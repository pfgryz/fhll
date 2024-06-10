from typing import Optional

from src.common.position import Position
from src.interpreter.types.typename import TypeName


# region Semantic Errors

class SemanticError(Exception):
    def __init__(self, message: str, position: Position):
        self.message = message
        self.position = position

        super().__init__(message)


# region Types

class UnknownTypeError(SemanticError):
    def __init__(self, name: TypeName, position: Position):
        message = f"Type \"{name}\" at {position} is not defined"
        super().__init__(message, position)


class TypeRedeclarationError(SemanticError):
    def __init__(self, name: TypeName, position: Position):
        message = f"Type \"{name}\" at {position} is already declared"
        super().__init__(message, position)


# endregion

# region Structs

class FieldRedeclarationError(SemanticError):
    def __init__(self, name: str, position: Position):
        message = (f"Field \"{name}\" is already declared "
                   f"in struct at {position}")
        super().__init__(message, position)


# endregion

# region Functions

class FunctionRedeclarationError(SemanticError):
    def __init__(self, name: str, position: Position):
        message = f"Function \"{name}\" is already declared"
        super().__init__(message, position)


class ParameterRedeclarationError(SemanticError):
    def __init__(self, name: str, position: Position):
        message = f"Parameter \"{name}\" is already declared"
        super().__init__(message, position)


# endregion


# region Function Call

class UndefinedFunctionError(SemanticError):
    def __init__(self, name: str, position: Position):
        message = f"Function {name} is not defined: {position}"
        super().__init__(message, position)


class TooFewArgumentsError(SemanticError):
    def __init__(self, name: str, position: Position):
        message = f"Too few arguments for {name}: {position}"
        super().__init__(message, position)


class TooManyArgumentsError(SemanticError):
    def __init__(self, name: str, position: Position):
        message = f"Too many arguments for {name}: {position}"
        super().__init__(message, position)


class MissingReturnStatementError(SemanticError):
    def __init__(self, name: str, position: Position):
        message = f"Missing return statement for {name}: {position}"
        super().__init__(message, position)


class MissingReturnValueError(SemanticError):
    def __init__(self, name: str, position: Position):
        message = f"Missing return value for {name}: {position}"
        super().__init__(message, position)


class ReturnValueInVoidFunctionError(SemanticError):
    def __init__(self, name: str, position: Position):
        message = f"Returning value from void for {name}: {position}"
        super().__init__(message, position)


# endregion

# region New Struct

class UndefinedStructError(SemanticError):
    def __init__(self, name: str, position: Position):
        message = f"Undefined struct {name}: {position}"
        super().__init__(message, position)


class AssignmentToUndefinedFieldError(SemanticError):
    def __init__(self, name: str, struct_name: str, position: Position):
        message = (f"Assignment to undefined "
                   f"field {name} in {struct_name}: {position}")
        super().__init__(message, position)


class InvalidFieldAssignmentError(SemanticError):
    def __init__(self, name: str, position: Position):
        message = f"Invalid assignment for {name}: {position}"
        super().__init__(message, position)


# endregion

# region Operations

class MissingOperationImplementationError(SemanticError):
    def __init__(
            self,
            name: str,
            first: TypeName,
            second: Optional[TypeName] = None,
            position: Optional[Position] = None
    ):
        if position is None:
            position = Position(1, 1)

        if second is not None:
            message = (f"Missing implementation of \"{name}\""
                       f" operation between \"{first}\" and \"{second}\"")
        else:
            message = (f"Missing implementation of \"{name}\""
                       f" operation for \"{first}\"")
        super().__init__(message, position)


class OperationImplementationAlreadyRegisteredError(SemanticError):
    def __init__(
            self,
            name: str,
            first: TypeName,
            second: Optional[TypeName] = None,
            position: Optional[Position] = None
    ):
        if position is None:
            position = Position(1, 1)

        if second is not None:
            message = (f"Operation {name} for types \"{first}\" "
                       f"and \"{second}\" is already registered")
        else:
            message = (f"Operation {name} for type \"{first}\" "
                       f"is already registered")
        super().__init__(message, position)


# endregion

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


class PanicBreak(InterpreterError):
    def __init__(self, message: str):
        self.panic_message = message
        super().__init__("Panicking...!")


class PanicError(InterpreterError):
    def __init__(self, message: str, position: Position):
        if message:
            self.message = (f"Program panicked with "
                            f"message: {message} at {position}")
        else:
            self.message = f"Program panicked at {position}"
        self.position = position
        super().__init__(self.message)


class MaximumRecursionError(InterpreterError):
    def __init__(self):
        super().__init__("Maximum recursion exceeded")

# endregion
