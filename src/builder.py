import codecs
from io import StringIO


class StringBuilder:
    """
    String builder
    """

    def __init__(self, init: str = None):
        """
        Creates new string builder
        :param init: initial value of string builder
        """
        self._stream = StringIO(init)
        self._length = len(init) if init is not None else 0

    @property
    def length(self) -> int:
        """
        Length of eaten chars
        :return: length of builder
        """
        return self._length

    def __add__(self, value: str) -> 'StringBuilder':
        """
        Add string to builder
        :param value: string to add to builder
        :return: StringBuilder
        """
        self._stream.write(value)
        self._length += len(value)
        return self

    def build(self) -> str:
        """
        Build string, consuming string builder
        :return: built string
        """
        self._stream.seek(0)
        value = self._stream.read()
        return value
