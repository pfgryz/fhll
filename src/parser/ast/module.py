from src.common.location import Location
from src.common.position import Position
from src.parser.ast.declaration.enum_declaration import EnumDeclaration
from src.parser.ast.declaration.function_declaration import FunctionDeclaration
from src.parser.ast.declaration.struct_declaration import StructDeclaration
from src.parser.ast.node import Node


class Module(Node):

    # region Dunder Methods

    def __init__(
            self,
            function_declarations: list[FunctionDeclaration],
            struct_declarations: list[StructDeclaration],
            enum_declarations: list[EnumDeclaration]
    ):
        super().__init__(Location.at(Position(1, 1)))

        self._name = ""
        self._path = ""
        self._function_declarations = function_declarations
        self._struct_declarations = struct_declarations
        self._enum_declarations = enum_declarations

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Module) \
            and self.name == other.name \
            and self.path == other.path \
            and self.function_declarations == other.function_declarations \
            and self.struct_declarations == other.struct_declarations \
            and self.enum_declarations == other.enum_declarations \
            and super().__eq__(other)

    # endregion

    # region Properties

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, path: str) -> None:
        self._path = path

    @property
    def function_declarations(self) -> list[FunctionDeclaration]:
        return self._function_declarations

    @property
    def struct_declarations(self) -> list[StructDeclaration]:
        return self._struct_declarations

    @property
    def enum_declarations(self) -> list[EnumDeclaration]:
        return self._enum_declarations

    # endregion
