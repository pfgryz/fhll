from src.common.location import Location
from src.parser.ast.common import Type
from src.parser.ast.declaration.declaration import Declaration
from src.parser.ast.name import Name
from src.parser.ast.declaration.parameter import Parameter

type Parameters = list[Parameter]


class FunctionDeclaration(Declaration):

    # region Dunder Methods

    def __init__(self, name: Name, parameters: Parameters, return_type: Type,
                 location: Location):
        super().__init__(location)

        self._name = name
        self._parameters = parameters
        self._return_type = return_type

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FunctionDeclaration) \
            and self.name == other.name \
            and self.parameters == other._parameters \
            and self.return_type == other.return_type \
            and super().__eq__(other)

    # endregion

    # region Properties

    @property
    def name(self) -> Name:
        return self._name

    @property
    def parameters(self) -> Parameters:
        return self._parameters

    @property
    def return_type(self) -> Type:
        return self._return_type

    # endregion
