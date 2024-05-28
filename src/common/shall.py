from typing import Any, Type


def shall(value: Any, error: Type[Exception], *error_args: Any):
    if value:
        return value
    raise error(*error_args)
