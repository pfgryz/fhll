from abc import abstractmethod

from src.interface.ivisitor import IVisitor
from src.interpreter.types.typename import TypeName

Mutable = bool
Parameters = dict[str, tuple[Mutable, TypeName]]


class IFunctionImplementation:

    # endregion

    # region Properties

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def parameters(self) -> Parameters:
        ...

    @property
    @abstractmethod
    def return_type(self) -> TypeName:
        ...

    # endregion

    # region Methods

    @abstractmethod
    def call(self, visitor: IVisitor) -> None:
        raise NotImplementedError

    # endregion
