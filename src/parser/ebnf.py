from typing import Callable


def ebnf(symbol: str, production: str) -> Callable:
    def decorator(func):
        func.ebnf = (symbol, production)
        return func

    return decorator
