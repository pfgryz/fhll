from src.common.location import Location
from src.parser.ast.common import Parameters, Type
from src.parser.ast.name import Name
from src.parser.ast.node import Node


class FunctionDeclaration(Node):
    # region Dunder Methods
    def __init__(self, name: Name, parameters: Parameters, returns: Type,
                 location: Location):
        super().__init__(location)

        self._name = name
        self._parameters = parameters
        self._returns = returns

    def __repr__(self) -> str:
        return "FunctionDeclaration(name={}, parameters={}, location={})".format(
            repr(self.name),
            repr(self.parameters),
            repr(self.location)
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FunctionDeclaration) \
            and self.name == other.name \
            and self.parameters == other._parameters

    # endregion

    # region Properties

    @property
    def name(self) -> Name:
        return self._name

    @property
    def parameters(self) -> Parameters:
        return self._parameters

    @property
    def returns(self) -> Type:
        return self._returns

    # endregion
