from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.utils.buffer import StreamBuffer


# region Utilities

def create_parser(content: str, consume_first: bool = False) -> Parser:
    buffer = StreamBuffer.from_str(content)
    lexer = Lexer(buffer)
    parser = Parser(lexer)

    # Read first token
    if consume_first:
        parser.consume()

    return parser

# endregion
