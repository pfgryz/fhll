from multimethod import multimethod

from src.common.shall import shall
from src.interface.ivisitor import IVisitor
from src.interpreter.box import Box
from src.interpreter.types.struct_implementation import StructImplementation
from src.interpreter.types.type import Type
from src.interpreter.types.type_implementation import TypeImplementation
from src.parser.ast.declaration.field_declaration import FieldDeclaration
from src.parser.ast.declaration.struct_declaration import StructDeclaration
from src.parser.ast.module import Module
from src.parser.ast.name import Name
from src.parser.ast.node import Node
from src.parser.ast.variant_access import VariantAccess
from typing import Optional


class TypesCollector(IVisitor[Node]):

    # region Dunder Methods

    def __init__(self):
        # Visitor State
        self._name: Box[str] = Box[str]()
        self._type: Box[Type] = Box[Type]()
        self._name.add_mutually_exclusive(self._type)
        self._type.add_mutually_exclusive(self._name)

        self._field: Box = Box()

        self._struct_implementation: Box[StructImplementation] = \
            Box[StructImplementation]()

        # Resolve table
        self._fields_to_resolve: \
            list[tuple[FieldDeclaration, str, Type, StructImplementation]] = []

        # Persistent state
        self._struct_implementations: dict[str, StructImplementation] = {}
        self._enum_implementations: dict[str, 'EnumImplementation'] = {}
        self._function_implementations: \
            dict[str, 'FunctionImplementation'] = {}

        self._types: dict[Type, TypeImplementation] = {
            Type("i32"): 3,
            Type("f32"): 4,
            Type("str"): 5,
            Type("bool"): 6
        }

    # endregion

    # region Types

    def _resolve_types(self):
        self._resolve_fields()

        for impl in self._struct_implementations.values():
            print(impl)

    def _resolve_type(self, typ: Type) -> Optional[TypeImplementation]:
        if typ in self._types:
            return self._types[typ]
        return None

    def _resolve_fields(self):
        for field_declaration, name, declared_type, struct_implementation in self._fields_to_resolve:
            resolved_type = shall(
                self._resolve_type(declared_type),
                RuntimeError, "@TODO 9"
            )

            struct_implementation.fields[name] = resolved_type

    # endregion

    # region Main Visits

    @multimethod
    def visit(self, module: Module) -> None:
        for struct_declaration in module.struct_declarations:
            self.visit(struct_declaration)
            struct_implementation = shall(
                self._struct_implementation.take(),
                RuntimeError,
                "@TODO 5"
            )
            self._struct_implementations[struct_implementation.name] = \
                struct_implementation
            self._types[struct_implementation.as_type()] = \
                struct_implementation

        self._resolve_types()

    @multimethod
    def visit(self, struct_declaration: StructDeclaration) -> None:
        # Get name of struct
        self.visit(struct_declaration.name)
        name = shall(self._name.take(), RuntimeError, "@TODO 1")

        # Create struct implementation
        implementation = StructImplementation(name)

        # Collect all field of struct
        fields = set()
        for field_declaration in struct_declaration.fields:
            # Get field
            self.visit(field_declaration)
            (name, declared_type) = shall(self._field.take(), RuntimeError,
                                          "@TODO 2")

            # Check if field name is unique
            if name in fields:
                raise RuntimeError("@TODO 6")
            fields.add(name)

            # Add field to resolve table
            self._fields_to_resolve.append(
                (field_declaration, name, declared_type, implementation)
            )

        # Put visited struct as visitor store
        self._struct_implementation.put(implementation)

    @multimethod
    def visit(self, field_declaration: FieldDeclaration) -> None:
        # Get name of field
        self.visit(field_declaration.name)
        name = shall(self._name.take(), RuntimeError, "@TODO 3")

        # Get type of field
        self.visit(field_declaration.declared_type)
        declared_type = shall(self._type.take(), RuntimeError, "@TODO 4")

        # Put visited field as visitor state
        self._field.put((name, declared_type))

    # endregion

    # region Helper Visits

    @multimethod
    def visit(self, name: Name) -> None:
        self._name.put(name.identifier)

        if self._type:
            self._type.put(
                self._type.take().extend(name.identifier)
            )
        else:
            self._type.put(Type(name.identifier))

    @multimethod
    def visit(self, variant_access: VariantAccess) -> None:
        self.visit(variant_access.parent)
        self.visit(variant_access.name)

    # endregion
