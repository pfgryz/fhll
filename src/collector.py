from src.interpreter.interpreter import Interpreter
from src.interpreter.types.enum_implementation import EnumImplementation
from src.interpreter.types.struct_implementation import StructImplementation
from src.interpreter.visitors.functions_collector import FunctionsCollector
from src.interpreter.visitors.types_collector import TypesCollector
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.utils.buffer import StreamBuffer


def types_collector():
    # program = """
    # struct Rectangle {
    #     width: i32;
    # }
    #
    # struct Square {
    #     side: i32;
    # }
    #
    # struct Complex {
    #     a: Square;
    # }
    #
    # struct Group {
    #     left: Square;
    #     right: Square;
    # }
    #
    # enum Std {
    #     struct String {};
    #     struct Optional {};
    # }
    #
    # enum UI {
    #     struct Window{
    #         name: Std::String;
    #         components: Std::Optional;
    #     };
    #     struct Square {};
    #     enum Color {
    #         struct Red {};
    #         struct Green{};
    #     };
    # }
    #
    # fn main() {
    #     let x = test(3);
    #     return;
    # }
    #
    # fn test(x: i32) -> i32 {
    #     return 3;
    # }
    #
    # fn d(mut x: i32, y: i32) -> i32 {
    #     return 3.4;
    # }
    #
    # fn ui(argc: i32, argv: Std::String) -> UI::Window {
    #     return UI::Window {};
    # }
    # """
    program = """
    fn main() {
        let x: i32 = 3;
        mut let y: i32 = x;
        y = 2 && 2;
    }
    """
    buffer = StreamBuffer.from_str(program)
    lexer = Lexer(buffer)
    parser = Parser(lexer)
    program = parser.parse()
    inter = Interpreter()
    inter.visit(program)
    inter.run("main")
    # collector = TypesCollector()
    # collector.visit(program)
    #
    # registry = collector._types_registry
    # for type, value in registry._types.items():
    #     # print(type, value)
    #     if isinstance(value, EnumImplementation):
    #         print('Enum: ', value.name, '|', type)
    #         for v in value.variants.values():
    #             print('\t', v.name, v.declared_type)
    #     elif isinstance(value, StructImplementation):
    #         print('Struct: ', value.name, "|", type)
    #         for k, v in value.fields.items():
    #             print('\t', k, ':', v)
    # print('TypesCollector Done!')
    #
    # print("\n\nFUNCTIONS\n\n")
    #
    # function_collector = FunctionsCollector(collector.types_registry)
    # function_collector.visit(program)
    # for function, impl in function_collector.functions_registry._functions.items():
    #     print('F', function, '->', impl.return_type)
    #     for (p, (m, t)) in impl.parameters.items():
    #         print('\t', m, p, t)


if __name__ == '__main__':
    types_collector()
