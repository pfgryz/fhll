from typing import Callable


class Registrable:

    def __init__(self):
        self.register()

    def register(self):
        for attribute_name in dir(self):
            attribute = getattr(self, attribute_name)
            if callable(attribute) and hasattr(attribute, "__register"):
                getattr(attribute, "__register")(self)

    @staticmethod
    def register_func(func: Callable, trigger: Callable):
        def both(x, previous: Callable):
            trigger(x)
            previous(x)

        if hasattr(func, "__register"):
            last = getattr(func, "__register")
            setattr(func, "__register", lambda x: both(x, last))
        else:
            setattr(func, "__register", trigger)
