from abc import ABC, abstractmethod

from src.interface.itoken import IToken


class ILexer(ABC):

    @abstractmethod
    def get_next_token(self) -> IToken:
        pass
