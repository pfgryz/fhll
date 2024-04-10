from typing import Iterator

from src.lexer.token import Token
from src.lexer.token_kind import TokenKind


class LexerIter:

    # region Dunder Methods
    def __init__(self, lexer: "Lexer"):
        self._lexer = lexer
        self._eof = False
        self._count = 0

    def __iter__(self) -> Iterator[Token]:
        return self

    def __next__(self) -> Token:
        if self._eof:
            raise StopIteration

        token = self._lexer.get_next_token()
        self._count += 1
        if token.kind == TokenKind.EOF:
            self._eof = True

        return token

    # endregion

    # region Properties
    @property
    def count(self) -> int:
        return self._count

    @property
    def eof(self) -> bool:
        return self._eof

    # endregion
