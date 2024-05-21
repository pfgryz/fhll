from typing import Optional

from multimethod import multimethod

from src.interface.ivisitor import IVisitor
from src.parser.ast.common import Type
from src.parser.ast.declaration.enum_declaration import EnumDeclaration
from src.parser.ast.declaration.function_declaration import FunctionDeclaration
from src.parser.ast.declaration.struct_declaration import StructDeclaration
from src.parser.ast.module import Module


class Interpreter(IVisitor):

    # region Dunder Methods

    def __init__(self):
        ...

    # endregion

    # region Context Manager

    # endregion

    # region Module

    @multimethod
    def visit(self, module: Module) -> None:
        for struct_declaration in module.struct_declarations:
            self.visit(struct_declaration)

        for enum_declaration in module.enum_declarations:
            self.visit(enum_declaration)

        for function_declaration in module.function_declarations:
            self.visit(function_declaration)

        # @TODO: 4. Process resolve table
        # @TODO:    a) take entry from resolve_table
        # @TODO:    b) check if entry type exists in type_table, if not raise Error
        # @TODO:    c) fill resolve target
        ...

    @multimethod
    def visit(self, struct_declaration: StructDeclaration) -> None:
        # @TODO: 1. Parse struct declarations
        # @TODO:    a) register struct as type in type_table
        # @TODO:    b) register struct in struct_table
        # @TODO:    c) collect struct field types and add to resolve_table
        ...

    @multimethod
    def visit(self, enum_declaration: EnumDeclaration) -> None:
        # @TODO: 2. Parse enum declarations
        # @TODO:    a) register enum as type in type_table
        # @TODO:    b) register enum in enum_table
        # @TODO:    c) register enum variants (structs / enums, recursion)
        ...

    @multimethod
    def visit(self, function_declaration: FunctionDeclaration) -> None:
        # @TODO: 3. Parse function declarations
        # @TODO:    a) register function in functions_table
        # @TODO:        - check if function name exists, if not create entry
        # @TODO:        - get entry
        # @TODO:        - check if function return type match return type of entry, if not raise Error
        # @TODO:        - check if function signature is in entry, if is raise Error
        # @TODO:        - add function signature to entry and save the entry
        # @TODO:    b) collect parameter types and return type and add to resolve_table
        ...

    # endregion
