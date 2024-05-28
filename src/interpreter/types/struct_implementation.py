from src.interpreter.typing.type import Type


class StructImplementation:

    def __init__(self, name: str, fields: dict[str, Type]):
        self._name = name
        self._fields = fields

    @property
    def name(self) -> str:
        return self._name

    @property
    def fields(self) -> dict[str, Type]:
        return self._fields

    @fields.setter
    def fields(self, fields: dict[str, Type]) -> None:
        self._fields = fields

    def as_type(self) -> Type:
        return Type(self._name)
