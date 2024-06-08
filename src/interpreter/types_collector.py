from multimethod import multimethod

from src.common.shall import shall
from src.interface.ivisitor import IVisitor
from src.interpreter.box import Box
from src.interpreter.types.enum_implementation import EnumImplementation
from src.interpreter.types.struct_implementation import StructImplementation
from src.interpreter.types.typename import TypeName
from src.interpreter.types.types_registry import TypesRegistry
from src.parser.ast.declaration.enum_declaration import EnumDeclaration
from src.parser.ast.declaration.field_declaration import FieldDeclaration
from src.parser.ast.declaration.struct_declaration import StructDeclaration
from src.parser.ast.module import Module
from src.parser.ast.name import Name
from src.parser.ast.node import Node
from src.parser.ast.variant_access import VariantAccess


class TypesCollector(IVisitor[Node]):

    # region Dunder Methods

    def __init__(self):
        # region Visitor states
        # > Name and type
        self._name: Box[str] = Box[str]()
        self._type: Box[TypeName] = Box[TypeName]()
        self._name.add_mutually_exclusive(self._type)
        self._type.add_mutually_exclusive(self._name)

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

        # region Types Registry

        self._types_registry = TypesRegistry()  # @TODO: Allow to provide basic types (builting)

        self._types_registry.register_type(
            TypeName("i32"), 123  # @TODO: Provider builtin implementation
        )

        # endregion

    # endregion

    # region Resolve Tables

    def _resolve(self):
        self._resolve_fields()

    def _resolve_fields(self):
        for field_declaration, name, declared_type, struct_implementation \
                in self._fields_resolve_table:
            resolve_type = shall(
                self._types_registry.get_type(declared_type),
                RuntimeError,
                f"@TODO: Unknown type for field {declared_type}",
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
                RuntimeError,
                "@TODO: Internal error, no struct"
            )

            self._types_registry.register_struct(
                struct_implementation.as_type(),
                struct_implementation
            )

        for enum_declaration in module.enum_declarations:
            self.visit(enum_declaration)

            enum_implementation = shall(
                self._enum_implementation.take(),
                RuntimeError,
                "@TODO: Internal error, no enum"
            )

            self._types_registry.register_enum(
                enum_implementation.as_type(),
                enum_implementation
            )

        self._resolve()

    @multimethod
    def visit(self, struct_declaration: StructDeclaration) -> None:
        # Get name of struct
        self.visit(struct_declaration.name)
        name = shall(
            self._name.take(),
            RuntimeError,
            "@TODO: No name for struct"
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
                RuntimeError,
                "@TODO: No internal state for field"
            )

            # Check if field is unique
            if name in fields:
                raise RuntimeError("@TODO: Field with name alredy exists")
            fields.add(name)

            # Add field to resolve table
            self._fields_resolve_table.append(
                (field_declaration, name, declared_type, implementation)
            )

        self._struct_implementation.put(implementation)

    @multimethod
    def visit(self, field_declaration: FieldDeclaration) -> None:
        # Get name of field
        self.visit(field_declaration.name)
        name = shall(
            self._name.take(),
            RuntimeError,
            "@TODO: No name for field"
        )

        # Get type of field
        self.visit(field_declaration.declared_type)
        declared_type = shall(
            self._type.take(),
            RuntimeError,
            "@TODO: No type for field"
        )

        # Put visited field as visitor state
        self._field.put((name, declared_type))

    @multimethod
    def visit(self, enum_declaration: EnumDeclaration) -> None:
        # Get name of enum
        self.visit(enum_declaration.name)
        name = shall(
            self._name.take(),
            RuntimeError,
            "@TODO: No name for enum"
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
            if not self._struct_implementation.empty:
                struct_implementation = shall(
                    self._struct_implementation.take(),
                    RuntimeError,
                    "@TODO: No internal state for struct"
                )
                self._types_registry.register_struct(
                    struct_implementation.as_type(),
                    struct_implementation
                )

                name = struct_implementation.name
                implementation.variants[name] = struct_implementation

            # Check if variant is enum
            elif not self._enum_implementation.empty:
                enum_implementation = shall(
                    self._enum_implementation.take(),
                    RuntimeError,
                    "@TODO: No internal state for enum"
                )
                self._types_registry.register_enum(
                    enum_implementation.as_type(),
                    enum_implementation
                )

                name = enum_implementation.name
                implementation.variants[name] = enum_implementation
            else:
                raise RuntimeError("@TODO: Unknown variant for enum")

        # Pop namespace to previous state
        self._namespace_type.put(namespace)
        self._enum_implementation.put(implementation)

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
            self._type.put(TypeName(name.identifier))

    @multimethod
    def visit(self, variant_access: VariantAccess) -> None:
        self.visit(variant_access.parent)
        self.visit(variant_access.name)

    # endregion
