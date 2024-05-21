from src.interpreter.interpreter import Interpreter
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.utils.buffer import StreamBuffer


def test_interpreter():
    program = """
    struct Rectangle {
        width: i32;
        height: i32;
    }
    """
    buffer = StreamBuffer.from_str(program)
    lexer = Lexer(buffer)
    parser = Parser(lexer)
    interpreter = Interpreter()
    interpreter.visit(parser.parse())
