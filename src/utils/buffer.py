from io import StringIO, TextIOWrapper
from typing import TextIO, BinaryIO

from src.lexer.position import Position


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
        self._line = 1
        self._column = 1
        self._char = None
        self._previous_position = None
        self._eof = False

    def __iter__(self):
        return self

    def __next__(self):
        while not self.eof:
            char = self.read_next_char()
            return char

        raise StopIteration

    def __str__(self) -> str:
        return f"StreamBuffer(position={self.position}, eof={self._eof})"

    # endregion

    # region Properties

    @property
    def line(self) -> int:
        """
        Last character line number in buffer
        :return: line number
        """
        return self._line

    @property
    def column(self) -> int:
        """
        Last character column number in buffer
        :return: column number
        """
        return self._column

    @property
    def position(self) -> Position:
        """
        Last character position in buffer
        :return: position in buffer
        """
        return Position(self.line, self.column)

    @property
    def previous_position(self) -> Position:
        """
        Previous character position in buffer
        :return: previous position in buffer
        """
        return self._previous_position

    @property
    def eof(self) -> bool:
        """
        Indicates if the eof has been reached
        :return: True if eof has been reached, False otherwise
        """
        return self._eof

    @property
    def char(self) -> str:
        """
        Last read character from the buffer
        :return: Last read character from the buffer
        """
        return self._char

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
            raise TypeError("Stream is not a TextIOWrapper")

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

    def read_next_char(self) -> str:
        """
        Reads next character from input stream.
        Returns "" if end of file is reached.
        :return: next character read from input stream
        """
        if not self._stream.readable():
            raise RuntimeError("Stream is not readable")

        char = self._stream.read(1)
        position = self.position

        if char == "":
            self._eof = True
            return char

        if self._char is not None:
            self._column += 1

        if self._char == "\n":
            self._line += 1
            self._column = 1

        self._char = char
        self._previous_position = position

        return char

    # endregion
