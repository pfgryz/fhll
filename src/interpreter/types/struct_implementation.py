from src.interpreter.stack.value import Value
from src.interpreter.types.typename import TypeName
from src.interpreter.types.type_implementation import TypeImplementation

type Fields = dict[str, TypeImplementation]


class StructImplementation(TypeImplementation):

    # region Dunder Methods

    def __init__(self, name: str, declared_type: TypeName):
        self._name = name
        self._declared_type = declared_type
        self._fields: Fields = {}

    def __repr__(self):
        return " ".join((
            self._name,
            "{",
            "; ".join((
                f"{name}: {declared_type}"
                for name, declared_type in self._fields.items()
            )),
            "}"
        ))

    # endregion

    # region Properties

    @property
    def name(self) -> str:
        return self._name

    @property
    def declared_type(self) -> TypeName:
        return self._declared_type

    @property
    def fields(self) -> Fields:
        return self._fields

    @fields.setter
    def fields(self, fields: Fields) -> None:
        self._fields = fields

    # endregion

    # region Methods

    def as_type(self) -> TypeName:
        return self._declared_type

    def instantiate(self, fields: dict[str, Value]) -> dict[str, Value]:
        return fields

    # endregion
