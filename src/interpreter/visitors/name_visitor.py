from multimethod import multimethod

from src.interface.ivisitor import IVisitor
from src.interpreter.box import Box
from src.interpreter.types.typename import TypeName
from src.parser.ast.name import Name
from src.parser.ast.node import Node
from src.parser.ast.variant_access import VariantAccess


class NameVisitor(IVisitor[Node]):

    # region Dunder Methods

    def __init__(self):
        self._name: Box[str] = Box[str]()
        self._type: Box[TypeName] = Box[TypeName]()
        self._name.add_mutually_exclusive(self._type)
        self._type.add_mutually_exclusive(self._name)

    # endregion

    # region Properties

    @property
    def name(self) -> Box[str]:
        return self._name

    @property
    def type(self) -> Box[TypeName]:
        return self._type

    # endregion

    # region Visits

    @multimethod
    def visit(self, name: Name) -> None:
        self._name.put(name.identifier)

        if self._type:
            self._type.put(
                self._type.value().extend(name.identifier)
            )
        else:
            self._type.put(TypeName(name.identifier))

    @multimethod
    def visit(self, variant_access: VariantAccess) -> None:
        self.visit(variant_access.parent)
        self.visit(variant_access.name)

    # endregion
