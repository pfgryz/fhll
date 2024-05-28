from multimethod import multimethod

from src.common.shall import shall
from src.interface.ivisitor import IVisitor
from src.interpreter.box import Box
from src.interpreter.types.struct_implementation import StructImplementation
from src.interpreter.typing.type import Type
from src.parser.ast.declaration.struct_declaration import StructDeclaration
from src.parser.ast.module import Module
from src.parser.ast.name import Name
from src.parser.ast.node import Node
from src.parser.ast.variant_access import VariantAccess


class TypesCollector(IVisitor[Node]):

    # region Dunder Methods

    def __init__(self):
        self._name: Box[str] = Box[str]()
        self._type: Box[Type] = Box[Type]()
        self._name.add_mutually_exclusive(self._type)
        self._type.add_mutually_exclusive(self._name)

        self._struct = Box()

        self._structs: dict[str, StructImplementation] = {}

        self._types = {
            Type("i32"): 3,
            Type("f32"): 4,
            Type("str"): 5,
            Type("bool"): 6
        }

    # endregion

    # region Types

    # endregion

    # region Types

    def _register_struct(self) -> None:
        (name, fields) = shall(self._struct.take(), RuntimeError, "ER1")
        # @TODO: Replace to custom error

        struct_implementation = StructImplementation(name, fields)

        if struct_implementation.as_type() in self._types:
            raise RuntimeError("ER2")
            # @TODO: Replace to custom error

        self._structs[struct_implementation.name] = struct_implementation
        self._types[struct_implementation.as_type()] = struct_implementation

    def _resolve_type(self, typ: Type) -> int:
        if typ in self._types:
            return self._types[typ]
        print(typ, self._types)
        raise RuntimeError("ER4")
        # @TODO: Replace to custom error

    def _resolve_types(self) -> None:
        for struct_implementation in self._structs.values():
            for name, raw_type in struct_implementation.fields.items():
                resolve_type = self._resolve_type(raw_type)

    # endregion

    # region Main Visits

    @multimethod
    def visit(self, module: Module) -> None:
        for struct_declaration in module.struct_declarations:
            self.visit(struct_declaration)
            self._register_struct()

        self._resolve_types()

    @multimethod
    def visit(self, struct_declaration: StructDeclaration) -> None:
        fields = {}

        for field in struct_declaration.fields:
            self.visit(field.name)

            name = shall(self._name.take(), RuntimeError, "1")
            # @TODO: Replace to custom error

            if name in fields:
                raise RuntimeError("2")
                # @TODO: Replace to custom error

            self.visit(field.declared_type)
            declared_type = shall(self._type.take(), RuntimeError, "3")

            fields[name] = declared_type

        self.visit(struct_declaration.name)
        name = shall(self._name.take(), RuntimeError, "4")
        # @TODO: Replace to custom error

        self._struct.put(
            (name, fields)
        )

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
