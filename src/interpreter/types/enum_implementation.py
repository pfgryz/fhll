from src.interpreter.types.struct_implementation import StructImplementation
from src.interpreter.types.type_implementation import TypeImplementation
from src.interpreter.types.typename import TypeName

type Variants = dict[str, StructImplementation | 'EnumImplementation']


class EnumImplementation(TypeImplementation):

    # region Dunder Methods

    def __init__(self, name: str, declared_type: TypeName):
        self._name = name
        self._declared_type = declared_type
        self._variants: Variants = {}

    def __repr__(self):
        return f"enum {self._name}"

    # endregion

    # region Properties

    @property
    def name(self) -> str:
        return self._name

    @property
    def declared_type(self) -> TypeName:
        return self._declared_type

    @property
    def variants(self) -> Variants:
        return self._variants

    # endregion

    # region Methods

    def as_type(self) -> TypeName:
        return self._declared_type

    def can_instantiate(self) -> bool:
        return False

    def instantiate(self, *args, **kwargs) -> TypeImplementation:
        raise NotImplementedError()

    # endregion
