from multimethod import multimethod

from src.interface.ivisitor import IVisitor
from src.interpreter.box import Box
from src.interpreter.typing.builtin import I32, F32
from src.interpreter.types_old.type import HTypeProxy, Type, HType
from src.parser.ast.access import Access
from src.parser.ast.declaration.enum_declaration import EnumDeclaration
from src.parser.ast.declaration.function_declaration import FunctionDeclaration
from src.parser.ast.declaration.struct_declaration import StructDeclaration
from src.parser.ast.module import Module
from src.parser.ast.name import Name
from src.parser.ast.variant_access import VariantAccess


class Interpreter(IVisitor):

    # region Dunder Methods

    def __init__(self):
        self._type = Box[Type]()

        self._types: dict[Type, HType] = {
            Type("i32"): I32(), # @TODO: Add constructors to builtin types_old
            Type("f32"): F32() # @TODO: Add function to register new types_old
        }
        self._resolve_table: dict[HTypeProxy, Type] = {}
        ...

    # endregion

    # region Context Manager

    # endregion

    # region Types

    def try_resolve_type(self, typ: Type) -> HTypeProxy:
        if existing := self._types.get(typ):
            return HTypeProxy(existing)

        response = HTypeProxy(None)
        self._resolve_table[response] = typ
        return response

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

        print('RT', self._resolve_table)
        print('T', self._types)

        # @TODO: 4. Process resolve table
        # @TODO:    a) take entry from resolve_table
        # @TODO:    b) check if entry type exists in type_table, if not raise Error
        # @TODO:    c) fill resolve target
        ...

    # endregion

    # region Struct Declaration

    @multimethod
    def visit(self, struct_declaration: StructDeclaration) -> None:
        fields = {}

        for field in struct_declaration.fields:
            name = field.name.identifier

            if name in fields:
                raise RuntimeError("Duplicate field name")
                # @TODO: Add final exception type

            self.visit(field.type)
            typ = self._type.take()

            fields[name] = self.try_resolve_type(typ)

        self.visit(struct_declaration.name)
        name = self._type.take().path[0]

        print(name, fields)
        # @TODO: register struct as type
        # constr = StructConstructor(name, fields)
        self._types[Type(name)] = None

    # endregion

    # region Enum Declaration
    @multimethod
    def visit(self, enum_declaration: EnumDeclaration) -> None:
        # @TODO: 2. Parse enum declarations
        # @TODO:    a) register enum as type in type_table
        # @TODO:    b) register enum in enum_table
        # @TODO:    c) register enum variants (structs / enums, recursion)
        ...

    # endregion

    # region Function Declaration

    @multimethod
    def visit(self, function_declaration: FunctionDeclaration) -> None:
        # @TODO: 3. Parse function declarations
        # @TODO:    a) register function in functions_table
        # @TODO:        - check if function name exists, if not create entry
        # @TODO:        - get entry
        # @TODO:        - check if function return type match return type of entry, if not raise Error
        # @TODO:        - check if function signature is in entry, if is raise Error
        # @TODO:        - add function signature to entry and save the entry
        # @TODO:    b) collect parameter types_old and return type and add to resolve_table
        ...

    # endregion

    # region Access

    @multimethod
    def visit(self, name: Name) -> None:
        if self._type:
            self._type.put(
                self._type.take().extend(name.identifier)
            )
        else:
            self._type.put(Type(name.identifier))

    @multimethod
    def visit(self, access: Access) -> None:
        raise NotImplementedError()

    @multimethod
    def visit(self, variant_access: VariantAccess) -> None:
        self.visit(variant_access.parent)
        self.visit(variant_access.name)

    # endregion
