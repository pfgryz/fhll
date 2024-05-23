from src.interpreter.typing.type import HType


class I32(HType):

    def __call__(self, *args):
        if len(args) == 0:
            return 0

        return int(args[0])


class F32(HType):
    def __call__(self, *args):
        if len(args) == 0:
            return 0.0

        return float(args[0])


class Str(HType):
    def __call__(self, *args):
        if len(args) == 0:
            return ""

        return str(args[0])


class Bool(HType):
    def __call__(self, *args):
        if len(args) == 0:
            return False

        return bool(args[0])
