from src.interpreter.types.type import Type
from src.interpreter.types.type_implementation import TypeImplementation


class StructImplementation(TypeImplementation):

    def __init__(self, name: str):
        self._name = name
        self._fields: dict[str, TypeImplementation] = {}

    def __repr__(self):
        return self._name + " fields: " + "".join([
            str(f) + ":" + str(ft) for f, ft in self._fields.items()
        ])

    @property
    def name(self) -> str:
        return self._name

    @property
    def fields(self) -> dict[str, TypeImplementation]:
        return self._fields

    @fields.setter
    def fields(self, fields: dict[str, TypeImplementation]) -> None:
        self._fields = fields

    def as_type(self) -> Type:
        return Type(self._name)

    def create(self, fields: dict[str, TypeImplementation]):
        raise NotImplementedError()
