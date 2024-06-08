from multimethod import multimethod

from src.interface.ivisitor import IVisitor
from src.interpreter.functions.functions_registry import FunctionsRegistry
from src.interpreter.types.types_registry import TypesRegistry
from src.interpreter.visitors.name_visitor import NameVisitor
from src.parser.ast.declaration.function_declaration import FunctionDeclaration
from src.parser.ast.module import Module
from src.parser.ast.node import Node


class FunctionsCollector(IVisitor[Node]):

    # region Dunder Methods

    def __init__(self, types_registry: TypesRegistry):
        self._name_visitor = NameVisitor()
        self._types_registry = types_registry

        # region Registry

        self._functions_registry = FunctionsRegistry()

        # endregion

    # endregion

    # region Properties

    @property
    def functions_registry(self) -> FunctionsRegistry:
        return self._functions_registry

    # endregion

    # region Main Visits

    @multimethod
    def visit(self, module: Module) -> None:
        for function_declaration in module.function_declarations:
            self.visit(function_declaration)

    @multimethod
    def visit(self, function_declaration: FunctionDeclaration) -> None:
        ...

    # endregion
