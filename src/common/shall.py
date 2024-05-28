from typing import Any, Type, Optional


def shall[T](value: Optional[T], error: Type[Exception],
             *error_args: Any) -> T:
    if value:
        return value
    raise error(*error_args)
