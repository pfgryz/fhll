from functools import wraps


def ebnf(rule: str):
    def decorator(func):
        func.ebnf = rule

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator
