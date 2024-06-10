from typing import Optional

from multimethod import multimethod

from src.common.shall import shall
from src.interface.ivisitor import IVisitor
from src.common.box import Box
from src.interpreter.errors import InternalError, ParameterRedeclarationError, \
    UnknownTypeError
from src.interpreter.functions.functions_registry import FunctionsRegistry
from src.interpreter.functions.user_function_implementation import \
    UserFunctionImplementation
from src.interpreter.types.typename import TypeName
from src.interpreter.types.types_registry import TypesRegistry
from src.interpreter.visitors.name_visitor import NameVisitor
from src.parser.ast.declaration.function_declaration import FunctionDeclaration
from src.parser.ast.declaration.parameter import Parameter
from src.parser.ast.module import Module
from src.parser.ast.node import Node


class FunctionsCollector(IVisitor[Node]):

    # region Dunder Methods

    def __init__(
            self,
            types_registry: TypesRegistry,
            functions_registry: Optional[FunctionsRegistry] = None
    ):
        self._name_visitor = NameVisitor()
        self._types_registry = types_registry

        # region States
        self._parameter: Box[tuple[str, bool, TypeName]] = \
            Box[tuple[str, bool, TypeName]]()
        # endregion

        # region Registry
        self._functions_registry = FunctionsRegistry() \
            if not functions_registry else functions_registry
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
        # Get name of function
        self._name_visitor.visit(function_declaration.name)
        name = shall(
            self._name_visitor.name.take(),
            InternalError,
            "Cannot collect name for function"
        )

        # Get return type of function
        if function_declaration.return_type:
            self._name_visitor.visit(function_declaration.return_type)
            return_type = shall(
                self._name_visitor.type.take(),
                InternalError,
                "Cannot collect return type for function"
            )

            if self._types_registry.get_type(return_type) is None:
                raise UnknownTypeError(
                    return_type,
                    function_declaration.return_type.location.begin
                )
        else:
            return_type = None

        # Create implementation
        implementation = UserFunctionImplementation(
            name,
            {},
            return_type,
            function_declaration.block
        )

        # Collect parameters for function
        for parameter in function_declaration.parameters:
            self.visit(parameter)
            (name, mutable, declared_type) = shall(
                self._parameter.take(),
                InternalError,
                "Cannot collect parameter for function"
            )

            if name in implementation.parameters:
                raise ParameterRedeclarationError(
                    name,
                    parameter.location.begin
                )

            if self._types_registry.get_type(declared_type) is None:
                raise UnknownTypeError(
                    declared_type,
                    parameter.declared_type.location.begin
                )

            implementation.parameters[name] = (mutable, declared_type)

        self._functions_registry.register_function(
            implementation.name,
            implementation,
            function_declaration.location.begin
        )

    @multimethod
    def visit(self, parameter: Parameter) -> None:
        self._name_visitor.visit(parameter.name)
        name = shall(
            self._name_visitor.name.take(),
            InternalError,
            "Cannot collect name for parameter"
        )

        self._name_visitor.visit(parameter.declared_type)
        declared_type = shall(
            self._name_visitor.type.take(),
            InternalError,
            "Cannot collect declared type for parameter"
        )

        mutable = parameter.mutable
        self._parameter.put((name, mutable, declared_type))

    # endregion
