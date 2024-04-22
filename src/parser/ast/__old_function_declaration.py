from src.interface.inode import INode


class FunctionDeclaration(INode):

    def __init__(self, name: str, parameters: list, returns: 'rtype',
                 block: 'block'):
        self._name = name
        self._parameters = parameters
        self._returns = returns
        self._block = block

    def __repr__(self) -> str:
        return ("FunctionDeclaration"
                "(name={}, parameters={}, returns={}, block={}").format(
            repr(self._name),
            repr(self._parameters),
            repr(self._returns),
            repr(self._block)
        )

    @property
    def name(self) -> str:
        return self._name

    @property
    def parameters(self) -> list:
        return self._parameters

    @property
    def returns(self) -> 'rtype':
        return self._returns

    @property
    def block(self) -> 'block':
        return self._block
