from src.interface.ivisitor import IVisitor
from src.interpreter.functions.ifunction_implementation import \
    IFunctionImplementation, Parameters
from src.interpreter.types.typename import TypeName
from src.parser.ast.statements.block import Block


class UserFunctionImplementation(IFunctionImplementation):

    # region Dunder Methods

    def __init__(
            self,
            name: str,
            parameters: Parameters,
            return_type: TypeName,
            block: Block
    ):
        self._name = name
        self._parameters = parameters
        self._return_type = return_type
        self._block = block

    # endregion

    # region Properties

    @property
    def name(self) -> str:
        return self._name

    @property
    def parameters(self) -> Parameters:
        return self._parameters

    @property
    def return_type(self) -> TypeName:
        return self._return_type

    @property
    def block(self) -> Block:
        return self._block

    # endregion

    # region Methods

    def call(self, visitor: IVisitor) -> None:
        visitor.visit(self._block)

    # endregion
