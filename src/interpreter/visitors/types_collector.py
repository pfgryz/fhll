from multimethod import multimethod

from src.common.position import Position
from src.common.shall import shall
from src.interface.ivisitor import IVisitor
from src.common.box import Box
from src.interpreter.errors import InternalError, FieldRedeclarationError, \
    UnknownTypeError
from src.interpreter.types.builtin_types_implementation import \
    BuiltinI32Implementation
from src.interpreter.types.builtin_types import BuiltinTypes
from src.interpreter.types.enum_implementation import EnumImplementation
from src.interpreter.types.struct_implementation import StructImplementation
from src.interpreter.types.typename import TypeName
from src.interpreter.types.types_registry import TypesRegistry
from src.interpreter.visitors.name_visitor import NameVisitor
from src.parser.ast.declaration.enum_declaration import EnumDeclaration
from src.parser.ast.declaration.field_declaration import FieldDeclaration
from src.parser.ast.declaration.struct_declaration import StructDeclaration
from src.parser.ast.module import Module
from src.parser.ast.node import Node


class TypesCollector(IVisitor[Node]):

    # region Dunder Methods

    def __init__(self):
        self._name_visitor = NameVisitor()

        # region Visitor states
        # > Structs & Enums
        self._namespace_type: Box[TypeName] = Box[TypeName]()

        self._struct_implementation: Box[StructImplementation] = \
            Box[StructImplementation]()
        self._enum_implementation: Box[EnumImplementation] = \
            Box[EnumImplementation]()

        self._field: Box[tuple[str, TypeName]] = Box[tuple[str, TypeName]]()

        # > Resolve tables
        self._fields_resolve_table: list[
            tuple[FieldDeclaration, str, TypeName, StructImplementation]
        ] = []
        # endregion

        # region Registry
        self._types_registry = TypesRegistry()

        # @TODO: Fill with real implementation of standard types
        self._types_registry.register_type(
            BuiltinTypes.I32, BuiltinI32Implementation(), Position(1, 1),
        )
        self._types_registry.register_type(
            BuiltinTypes.F32, BuiltinI32Implementation(), Position(1, 1),
        )
        self._types_registry.register_type(
            BuiltinTypes.STR, BuiltinI32Implementation(), Position(1, 1),
        )
        self._types_registry.register_type(
            BuiltinTypes.BOOL, BuiltinI32Implementation(), Position(1, 1),
        )
        # endregion

    # endregion

    # region Properties

    @property
    def types_registry(self) -> TypesRegistry:
        return self._types_registry

    # endregion

    # region Resolve Tables

    def _resolve(self):
        self._resolve_fields()

    def _resolve_fields(self):
        for field_declaration, name, declared_type, struct_implementation \
                in self._fields_resolve_table:
            resolve_type = shall(
                self._types_registry.get_type(declared_type),
                UnknownTypeError,
                declared_type,
                field_declaration.location.begin
            )

            struct_implementation.fields[name] = resolve_type

    # endregion

    # region Main Visits

    @multimethod
    def visit(self, module: Module) -> None:
        for struct_declaration in module.struct_declarations:
            self.visit(struct_declaration)

            struct_implementation = shall(
                self._struct_implementation.take(),
                InternalError,
                "Cannot collect struct implementation after visiting"
            )

            self._types_registry.register_struct(
                struct_implementation.as_type(),
                struct_implementation,
                struct_declaration.name.location.begin
            )

        for enum_declaration in module.enum_declarations:
            self.visit(enum_declaration)

            enum_implementation = shall(
                self._enum_implementation.take(),
                InternalError,
                "Cannot collect enum implementation after visiting"
            )

            self._types_registry.register_enum(
                enum_implementation.as_type(),
                enum_implementation,
                enum_declaration.name.location.begin
            )

        self._resolve()

    @multimethod
    def visit(self, struct_declaration: StructDeclaration) -> None:
        # Get name of struct
        self._name_visitor.visit(struct_declaration.name)
        name = shall(
            self._name_visitor.name.take(),
            InternalError,
            "Cannot collect name for struct"
        )

        # Create struct implementation
        namespace = self._namespace_type.value()
        implementation = StructImplementation(
            name,
            TypeName(name) if namespace is None else namespace.extend(name)
        )

        # Collect all field of struct
        fields = set()
        for field_declaration in struct_declaration.fields:
            # Get field
            self.visit(field_declaration)
            (name, declared_type) = shall(
                self._field.take(),
                InternalError,
                "Cannot collect field declaration after visiting"
            )

            # Check if field is unique
            if name in fields:
                raise FieldRedeclarationError(
                    name,
                    field_declaration.location.begin
                )
            fields.add(name)

            # Add field to resolve table
            self._fields_resolve_table.append(
                (field_declaration, name, declared_type, implementation)
            )

        self._struct_implementation.put(implementation)

    @multimethod
    def visit(self, field_declaration: FieldDeclaration) -> None:
        # Get name of field
        self._name_visitor.visit(field_declaration.name)
        name = shall(
            self._name_visitor.name.take(),
            InternalError,
            "Cannot collect name for field"
        )

        # Get type of field
        self._name_visitor.visit(field_declaration.declared_type)
        declared_type = shall(
            self._name_visitor.type.take(),
            InternalError,
            "Cannot collect type for field"
        )

        # Put visited field as visitor state
        self._field.put((name, declared_type))

    @multimethod
    def visit(self, enum_declaration: EnumDeclaration) -> None:
        # Get name of enum
        self._name_visitor.visit(enum_declaration.name)
        name = shall(
            self._name_visitor.name.take(),
            InternalError,
            "Cannot collect name for enum"
        )

        # Save current namespace
        namespace = self._namespace_type.value()

        # Create enum implementation
        implementation = EnumImplementation(
            name,
            TypeName(name) if namespace is None else namespace.extend(name)
        )
        # Update namespace to include current enum
        self._namespace_type.put(implementation.as_type())

        # Collect all variants
        for variant in enum_declaration.variants:
            # Get variant
            self.visit(variant)

            # Check if variant is struct
            if self._struct_implementation:
                struct_implementation = self._struct_implementation.take()
                self._types_registry.register_struct(
                    struct_implementation.as_type(),
                    struct_implementation,
                    variant.name.location.begin
                )

                name = struct_implementation.name
                implementation.variants[name] = struct_implementation
                continue

            # Check if variant is enum
            if self._enum_implementation:
                enum_implementation = self._enum_implementation.take()
                self._types_registry.register_enum(
                    enum_implementation.as_type(),
                    enum_implementation,
                    variant.name.location.begin
                )

                name = enum_implementation.name
                implementation.variants[name] = enum_implementation
                continue

            raise InternalError("Cannot collect variant after visiting")

        # Pop namespace to previous state
        self._namespace_type.put(namespace)
        self._enum_implementation.put(implementation)

    # endregion
