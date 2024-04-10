from typing import Optional

from src.flags import Flags
from src.interface.ilexer import ILexer
from src.lexer.errors import IdentifierTooLongException, \
    IntegerOverflowException, \
    IntegerLeadingZerosException, StringTooLongException, \
    UnterminatedStringException, \
    InvalidEscapeSequenceException, ExpectingCharException
from src.lexer.iter import LexerIter
from src.lexer.location import Location
from src.lexer.position import Position
from src.lexer.token import Token
from src.lexer.token_kind import TokenKind
from src.utils.buffer import StreamBuffer
from src.utils.builder import StringBuilder


class Lexer(ILexer):
    """
    Lexer class
    """

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
        """
        Creates new lexer
        :param stream: input stream buffer
        :param flags: interpreter flags
        """
        self._stream = stream
        self._flags = flags if flags is not None else Flags()

        self._builders = {
            self._build_punctation,
            self._build_operator,
            self._build_comment_or_divide,
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

    def __iter__(self):
        return LexerIter(self)

    # endregion

    # region Properties

    @property
    def flags(self) -> Flags:
        """
        Interpreter flags
        :return: interpreter flags
        """
        return self._flags

    # endregion

    # region Methods

    def get_next_token(self) -> Token:
        """
        Get next token from stream
        :return: next token
        """

        # Read first char if stream is fresh
        if self._stream.char is None:
            self._stream.read_next_char()

        # Skip whitespaces
        while not self._stream.eof and self._stream.char.isspace():
            self._stream.read_next_char()

        # Return EOF token on end
        if self._stream.eof:
            return Token(TokenKind.EOF,
                         Location.at(self._stream.position))

        # Try build token
        for builder in self._builders:
            token = builder()
            if token is not None:
                return token

    # endregion

    # region Private Methods

    def _build_identifier_or_keyword(self) -> Optional[Token]:
        if not self.is_first_identifier_char(self._stream.char):
            return None

        builder = StringBuilder()
        begin = self._stream.position
        builder += self._stream.char
        self._stream.read_next_char()

        while builder.length <= self._flags.maximum_identifier_length and \
                self.is_identifier_char(self._stream.char) and \
                not self._stream.eof:
            builder += self._stream.char
            self._stream.read_next_char()

        end = self._stream.previous_position
        location = Location(begin, end)
        value = builder.build()

        if builder.length > self._flags.maximum_identifier_length:
            raise IdentifierTooLongException(location)

        if (builtin := self._builtin_types_map.get(value)) is not None:
            return Token(builtin, location)

        if (keyword := self._keywords_map.get(value)) is not None:
            return Token(keyword, location)

        if value == "true" or value == "false":
            return Token(TokenKind.Boolean, location, value == "true")

        return Token(TokenKind.Identifier, location, value)

    def _build_number_literal(self) -> Optional[Token]:
        if not self._stream.char.isdecimal():
            return None

        begin = self._stream.position
        value = self._internal_build_integer()
        end = self._stream.previous_position

        if self._stream.char != ".":
            location = Location(begin, end)

            if value > self._flags.maximum_integer_value or \
                    value < self._flags.minimum_integer_value:
                raise IntegerOverflowException(location)

            return Token(TokenKind.Integer, location, value)

        # Skip dot
        self._stream.read_next_char()

        fraction = self._internal_build_fraction()
        end = self._stream.previous_position
        value = value + fraction

        return Token(TokenKind.Float, Location(begin, end), value)

    def _internal_build_integer(self) -> int:
        value = 0
        length = 0
        begin = self._stream.position

        while self._stream.char.isdecimal() and not self._stream.eof:
            if length > 0 and value == 0:
                raise IntegerLeadingZerosException(
                    Location(begin, self._stream.previous_position))

            digit = int(self._stream.char)
            value = value * 10 + digit

            length += 1

            self._stream.read_next_char()

        return value

    def _internal_build_fraction(self) -> float:
        value = 0
        multiplier = 10

        while self._stream.char.isdecimal() and not self._stream.eof:
            digit = int(self._stream.char)
            value = value + digit / multiplier
            multiplier *= 10
            self._stream.read_next_char()

        return value

    def _build_string(self) -> Optional[Token]:
        if self._stream.char != self.string_delimiter:
            return None

        builder = StringBuilder()
        begin = self._stream.position
        self._stream.read_next_char()

        while builder.length <= self._flags.maximum_string_length and \
                self._stream.char != self.string_delimiter and \
                not self._stream.eof:

            char = self._stream.char

            if self._stream.char == "\\":
                self._stream.read_next_char()
                char = self._internal_build_escape_sequence(begin)

            builder += char
            self._stream.read_next_char()

        if builder.length > self._flags.maximum_string_length:
            raise StringTooLongException(
                Location(begin, self._stream.previous_position))

        if self._stream.char == self.string_delimiter:
            self._stream.read_next_char()
        else:
            raise UnterminatedStringException(
                Location(begin, self._stream.previous_position))

        value = builder.build()
        return Token(TokenKind.String,
                     Location(begin, self._stream.previous_position), value)

    def _internal_build_escape_sequence(self, begin: Position) -> str:
        if self._stream.eof:
            raise UnterminatedStringException(
                Location(begin, self._stream.position))

        match self._stream.char:
            case "n":
                return "\n"
            case "t":
                return "\t"
            case "\\":
                return "\\"
            case "\"":
                return "\""

        raise InvalidEscapeSequenceException(self._stream.position)

    def _build_punctation(self) -> Optional[Token]:
        token = \
            self._build_single_char("(", TokenKind.ParenthesisOpen) \
            or self._build_single_char(")", TokenKind.ParenthesisClose) \
            or self._build_single_char("{", TokenKind.BraceOpen) \
            or self._build_single_char("}", TokenKind.BraceClose) \
            or self._build_single_char("}", TokenKind.BraceClose) \
            or self._build_single_char(".", TokenKind.Comma) \
            or self._build_single_char(",", TokenKind.Period) \
            or self._build_single_char(";", TokenKind.Semicolon) \
            or self._build_multiple_char(":", TokenKind.Colon, [
                (":", TokenKind.DoubleColon)
            ])

        return token

    def _build_operator(self) -> Optional[Token]:
        token = \
            self._build_single_char(">", TokenKind.Greater) \
            or self._build_single_char("<", TokenKind.Less) \
            or self._build_single_char("+", TokenKind.Plus) \
            or self._build_single_char("*", TokenKind.Multiply) \
            or self._build_double_char("&", TokenKind.And) \
            or self._build_double_char("|", TokenKind.Or) \
            or self._build_multiple_char("!", TokenKind.Negate, [
                ("=", TokenKind.NotEqual)
            ]) \
            or self._build_multiple_char("=", TokenKind.Assign, [
                ("=", TokenKind.Equal),
                (">", TokenKind.BoldArrow)
            ]) \
            or self._build_multiple_char("-", TokenKind.Minus, [
                (">", TokenKind.Arrow)
            ])

        return token

    def _build_single_char(self, char: str, kind: TokenKind
                           ) -> Optional[Token]:
        if self._stream.char == char:
            begin = self._stream.position
            self._stream.read_next_char()
            return Token(kind, Location(begin, begin))

        return None

    def _build_double_char(self, char: str, kind: TokenKind) -> \
            Optional[Token]:
        if self._stream.char == char:
            begin = self._stream.position

            self._stream.read_next_char()
            if self._stream.char != char or self._stream.eof:
                raise ExpectingCharException(char, self._stream.char, kind,
                                             self._stream.position)

            end = self._stream.position
            self._stream.read_next_char()

            return Token(kind, Location(begin, end))

        return None

    def _build_multiple_char(self, char: str, default: TokenKind,
                             predicates: list[tuple] = None
                             ) -> Optional[Token]:
        if self._stream.char != char:
            return None

        predicates = [] if predicates is None else predicates

        begin = self._stream.position
        self._stream.read_next_char()

        if self._stream.eof:
            return Token(default, Location(begin, begin))

        for predicate in predicates:
            (predicate_char, predicate_kind) = predicate

            if self._stream.char == predicate_char:
                end = self._stream.position
                self._stream.read_next_char()
                return Token(predicate_kind, Location(begin, end))

        return Token(default, Location(begin, begin))

    def _build_comment_or_divide(self) -> Optional[Token]:
        if self._stream.char != "/":
            return None

        begin = self._stream.position
        self._stream.read_next_char()

        if self._stream.char == "/" and not self._stream.eof:
            return self._internal_build_comment()

        return Token(TokenKind.Divide, Location(begin, begin))

    def _internal_build_comment(self) -> Optional[Token]:
        begin = self._stream.previous_position
        self._stream.read_next_char()

        builder = StringBuilder()
        while self._stream.char != "\n" and not self._stream.eof:
            builder += self._stream.char
            self._stream.read_next_char()

        return Token(TokenKind.Comment,
                     Location(begin, self._stream.previous_position),
                     builder.build())

    # endregion

    # region Static Methods

    @staticmethod
    def is_first_identifier_char(char: str) -> bool:
        return char.isalpha() or char == "_"

    @staticmethod
    def is_identifier_char(char: str) -> bool:
        return char.isalnum() or char == "_"

    # endregion
