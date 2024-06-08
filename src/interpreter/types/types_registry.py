from typing import Optional

from src.interpreter.types.enum_implementation import EnumImplementation
from src.interpreter.types.struct_implementation import StructImplementation
from src.interpreter.types.typename import TypeName
from src.interpreter.types.type_implementation import TypeImplementation


class TypesRegistry:

    # region Dunder Methods

    def __init__(self):
        self._types: dict[TypeName, TypeImplementation] = {}
        self._structs: dict[TypeName, StructImplementation] = {}
        self._enums: dict[TypeName, EnumImplementation] = {}

    # endregion

    # region Methods

    def get_type(self, type_name: TypeName) -> Optional[TypeImplementation]:
        return self._types.get(type_name, None)

    def get_struct(self, struct_name: TypeName) \
            -> Optional[StructImplementation]:
        return self._structs.get(struct_name, None)

    def get_enum(self, enum_name: TypeName) -> Optional[EnumImplementation]:
        return self._enums.get(enum_name, None)

    def register_type(self, type_name: TypeName,
                      implementation: TypeImplementation):
        if type_name in self._types:
            raise RuntimeError("@TODO: Type with this name already declared")

        self._types[type_name] = implementation

    def register_struct(self, struct_name: TypeName,
                        implementation: StructImplementation):
        if struct_name in self._structs:
            raise RuntimeError("@TODO: Struct with this name already declared")

        self.register_type(struct_name, implementation)
        self._structs[struct_name] = implementation

    def register_enum(self, enum_name: TypeName,
                      implementation: EnumImplementation):
        if enum_name in self._enums:
            raise RuntimeError("@TODO: Enum with this name already declared")

        self.register_type(enum_name, implementation)
        self._enums[enum_name] = implementation

    # endregion
