from io import StringIO, TextIOWrapper
from typing import TextIO, BinaryIO


class StreamBuffer:
    """
    Stream Buffer class
    - enforces same "\n" newlines
    - automatically calculates line number and column
    - detects and indicates eof
    """

    # region Dunder methods
    def __init__(self, stream: TextIOWrapper):
        """
        Creates new instance of StreamBuffer

        :param stream: TextIOWrapper Configured stream
        """
        self._stream = stream
        self._last = ""
        self._line = 1
        self._column = 0
        self._eof = False

    def __iter__(self):
        return self

    def __next__(self):
        while not self.eof:
            char = self.read_char()
            return char

        raise StopIteration

    # endregion

    # region Properties

    @property
    def line(self) -> int:
        """
        Line Number of the buffer
        :return: line number
        """
        return self._line

    @property
    def column(self) -> int:
        """
        Column number of the buffer
        :return: column number
        """
        return self._column

    @property
    def eof(self) -> bool:
        """
        Indicates if the eof has been reached
        :return: True if eof has been reached, False otherwise
        """
        return self._eof

    # endregion

    # region Class Methods

    @classmethod
    def from_str(cls, string: str) -> 'StreamBuffer':
        """
        Creates new instance of StreamBuffer from a string
        :param string: input string
        :return: new instance of StreamBuffer
        """
        stream = StringIO(string, newline=None)
        return cls(stream)

    @classmethod
    def from_text_io(cls, stream: TextIO,
                     encoding: str = "utf-8") -> 'StreamBuffer':
        """
        Creates new instance of StreamBuffer from a text i/o.
        Reconfigures stream to use given encoding and enforces unified newlines
        :param stream: input text stream
        :param encoding: encoding of input stream, defaults to utf-8
        :return: new instance of StreamBuffer
        """
        if not isinstance(stream, TextIOWrapper):
            raise ValueError("Stream is not a TextIOWrapper")

        stream.reconfigure(newline=None, encoding=encoding, errors="strict")
        return cls(stream)

    @classmethod
    def from_binary_io(cls, stream: BinaryIO,
                       encoding: str = "utf-8") -> 'StreamBuffer':
        """
        Creates new instance of StreamBuffer from a binary i/o.
        Reconfigures stream to use given encoding and enforces unified newlines
        :param stream: input binary stream
        :param encoding: encoding of input stream, defaults to utf-8
        :return: new instance of StreamBuffer
        """
        return cls(TextIOWrapper(stream, newline=None, encoding=encoding,
                                 errors="strict"))

    # endregion

    # region Methods

    def read_char(self) -> str:
        """
        Reads next character from input stream.
        Returns "" if end of file is reached.
        :return: next character read from input stream
        """
        if not self._stream.readable:
            raise RuntimeError("Stream is not readable")

        char = self._stream.read(1)

        if char == "":
            self._eof = True
            return char

        if self._last == "\n":
            self._line += 1
            self._column = 0

        self._column += 1
        self._last = char

        return char

    # endregion
