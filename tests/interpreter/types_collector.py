from src.interpreter.types_collector import TypesCollector
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.utils.buffer import StreamBuffer


def test_types_collector():
    program = """
    struct Rectangle {
        width: i32;
    }
    
    struct Square {
        side: i32;
    }
    
    struct Complex {
        a: Square;
    }
    
    struct Group {
        left: Square;
        right: Square;
    }
    """
    buffer = StreamBuffer.from_str(program)
    lexer = Lexer(buffer)
    parser = Parser(lexer)
    collector = TypesCollector()
    collector.visit(parser.parse())
