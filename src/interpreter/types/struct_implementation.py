from src.interpreter.types.typename import TypeName
from src.interpreter.types.type_implementation import TypeImplementation

type Fields = dict[str, TypeImplementation]


class StructImplementation(TypeImplementation):

    # region Dunder Methods

    def __init__(self, name: str):
        self._name = name
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
    def fields(self) -> Fields:
        return self._fields

    @fields.setter
    def fields(self, fields: Fields) -> None:
        self._fields = fields

    # endregion

    # region Methods

    def as_type(self) -> TypeName:
        return TypeName(self._name)

    def instantiate(self, *args, **kwargs) -> TypeImplementation:
        raise NotImplementedError()  # @TODO: Implement

    # endregion
