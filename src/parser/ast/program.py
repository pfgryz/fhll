from src.interface.inode import INode


class Program(INode):

    def __init__(self, functions: dict, structs):
        self._functions = functions
        self._structs = structs

    def __repr__(self) -> str:
        return "Program(functions={}, structs={})".format(
            repr(self._functions),
            repr(self._structs)
        )

    @property
    def functions(self) -> dict:
        return self._functions
