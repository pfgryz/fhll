from src.lexer.lexer import Lexer
from src.parser.ast.module import Module
from src.parser.parser import Parser
from src.utils.buffer import StreamBuffer


def load_module(program: str) -> Module:
    buffer = StreamBuffer.from_str(program)
    lexer = Lexer(buffer)
    parser = Parser(lexer)
    ast = parser.parse()

    return ast
