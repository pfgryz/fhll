from typing import Optional

from src.buffer import StreamBuffer
from src.builder import StringBuilder
from src.errors import IdentifierTooLongError, IntegerOverflowError, \
    IntegerLeadingZerosError, StringTooLongError, UnterminatedStringError, \
    InvalidEscapeSequenceError
from src.flags import Flags
from src.location import Location
from src.position import Position
from src.token import Token
from src.token_kind import TokenKind


class Lexer:
    builtin_types = (
        TokenKind.U16,
        TokenKind.U32,
        TokenKind.U64,
        TokenKind.I16,
        TokenKind.I32,
        TokenKind.I64,
        TokenKind.F32,
        TokenKind.Bool,
        TokenKind.Str
    )

    keywords = (
        TokenKind.Fn,
        TokenKind.Struct,
        TokenKind.Enum,
        TokenKind.Mut,
        TokenKind.Let,
        TokenKind.Is,
        TokenKind.If,
        TokenKind.While,
        TokenKind.While,
        TokenKind.Return,
        TokenKind.As,
        TokenKind.Match
    )

    string_delimiter = "\""

    # region Dunder Methods

    def __init__(self, stream: StreamBuffer, flags: Flags = None):
        self._stream = stream
        self._flags = flags if flags is not None else Flags()

        self._builders = {
            self._build_identifier_or_keyword,
            self._build_number_literal,
            self._build_string
        }

        self._builtin_types_map = {
            builtin.value: builtin
            for builtin in self.builtin_types
        }
        self._keywords_map = {
            keyword.value: keyword
            for keyword in self.keywords
        }

    # endregion

    # region Properties

    @property
    def char(self) -> str:
        return self._stream.char

    @property
    def flags(self) -> Flags:
        return self._flags

    # endregion

    # region Methods

    def get_next_token(self) -> Token:
        # Read first char if stream is fresh
        if self._stream.char is None:
            self._stream.read_next_char()

        # Skip whitespaces
        while self._stream.char.isspace():
            self._stream.read_next_char()

        for builder in self._builders:
            token = builder()
            if token is not None:
                return token

    # endregion

    # region Private Methods

    def _build_identifier_or_keyword(self) -> Optional[Token]:
        if not self.is_first_identifier_char(self.char):
            return None

        builder = StringBuilder()
        begin = self._stream.position
        end = self._stream.position

        while builder.length <= self._flags.maximum_identifier_length and \
                self.is_identifier_char(self.char) and \
                not self._stream.eof:
            builder += self.char
            end = self._stream.position
            self._stream.read_next_char()

        location = Location(begin, end)
        value = builder.build()

        if builder.length > self._flags.maximum_identifier_length:
            raise IdentifierTooLongError(location)

        if (builtin := self._builtin_types_map.get(value)) is not None:
            return Token(builtin, location)

        if (keyword := self._keywords_map.get(value)) is not None:
            return Token(keyword, location)

        if value == "true" or value == "false":
            return Token(TokenKind.Boolean, location, value == "true")

        return Token(TokenKind.Identifier, location, value)

    def _build_number_literal(self) -> Optional[Token]:
        if not self.char.isdecimal():
            return None

        begin = self._stream.position
        value, end = self._internal_build_integer()

        if self.char != ".":
            location = Location(begin, end)

            if value > self._flags.maximum_integer_value:
                raise IntegerOverflowError(location)

            return Token(TokenKind.Integer, location, value)

        self._stream.read_next_char()

        fraction, end = self._internal_build_fraction()
        value = value + fraction

        return Token(TokenKind.Float, Location(begin, end), value)

    def _internal_build_integer(self) -> tuple[int, Position]:
        value = 0
        length = 0
        begin = self._stream.position
        end = self._stream.position

        while self.char.isdecimal() and not self._stream.eof:
            if length > 0 and value == 0:
                raise IntegerLeadingZerosError(Location(begin, end))

            digit = int(self.char)
            value = value * 10 + digit

            length += 1
            end = self._stream.position

            self._stream.read_next_char()

        return value, end

    def _internal_build_fraction(self) -> tuple[float, Position]:
        value = 0
        multiplier = 10
        end = self._stream.position

        while self.char.isdecimal() and not self._stream.eof:
            digit = int(self.char)
            value = value + digit / multiplier
            multiplier *= 10
            end = self._stream.position
            self._stream.read_next_char()

        return value, end

    def _build_string(self) -> Optional[Token]:
        if self.char != self.string_delimiter:
            return None

        builder = StringBuilder()
        begin = self._stream.position
        end = self._stream.position
        self._stream.read_next_char()

        while builder.length <= self._flags.maximum_string_length and \
                self.char != self.string_delimiter and \
                not self._stream.eof:

            char = self.char

            if self.char == "\\":
                self._stream.read_next_char()
                char = self._internal_build_escape_sequence(begin)

            builder += char
            end = self._stream.position
            self._stream.read_next_char()

        if builder.length > self._flags.maximum_string_length:
            raise StringTooLongError(Location(begin, end))

        if self.char == self.string_delimiter:
            end = self._stream.position
            self._stream.read_next_char()
        else:
            raise UnterminatedStringError(Location(begin, end))

        value = builder.build()
        return Token(TokenKind.String, Location(begin, end), value)

    def _internal_build_escape_sequence(self, begin: Position) -> str:
        if self._stream.eof:
            raise UnterminatedStringError(
                Location(begin, self._stream.position))

        match self.char:
            case "n":
                return "\n"
            case "t":
                return "\t"
            case "\\":
                return "\\"
            case "\"":
                return "\""

        raise InvalidEscapeSequenceError(self._stream.position)

    # endregion

    # region Static Methods

    @staticmethod
    def is_first_identifier_char(char: str) -> bool:
        return char.isalpha() or char == "_"

    @staticmethod
    def is_identifier_char(char: str) -> bool:
        return char.isalnum() or char == "_"

    # endregion
