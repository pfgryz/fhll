from dataclasses import dataclass


@dataclass
class Flags:
    """
    Interpreter flags
    """

    # region Lexer
    maximum_identifier_length: int = 128
    maximum_string_length: int = 128
    maximum_integer_value: int = 2 ** 64 - 1
    minimum_integer_value: int = - (2 ** 63)
    # endregion

    # region Interpreter
    maximum_recursion: int = 10
    # endregion
