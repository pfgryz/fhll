from dataclasses import dataclass


@dataclass
class Flags:
    """
    Interpreter flags
    """

    maximum_identifier_length: int = 128
    maximum_string_length: int = 128
    maximum_integer_value: int = 2 ** 64 - 1
