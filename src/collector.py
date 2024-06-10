from src.interpreter.interpreter import Interpreter
from src.interpreter.stack.value import Value
from src.interpreter.types.typename import TypeName
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.utils.buffer import StreamBuffer


def load_file(name: str):
    with open(name, "r") as handle:
        buffer = StreamBuffer.from_text_io(handle)
        lexer = Lexer(buffer)
        parser = Parser(lexer)
        return parser.parse()


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
    struct Std {}
    
    fn main(ARGC: i32) -> i32 {
        {
            let z: i32;
        }
        let x: i32 = 3;
        mut let y: i32 = x;
        y = -y as i32;
        y = y * 2;
        
        if (0) {
            let d: i32;
            return 5;
        } else {
            let IT_IS_ELSE: i32;
            return -10;
        }
        
        let iter: i32 = 0;
        while (iter < 5) {
            iter = iter + 1;
        }
        
        match (x) {
            i32 y => {
                let IN_MATCHER: i32 = 3;
            };
            i32 y => {
                let IN_SECOND: i32 = 2;
            };
        }
    }
    """
    program = """
    struct Item {
        amount: i32;
    }
    
    fn t(mut x: Item) -> Item {
        let z: f32 = 2.3;
        let r: i32 = 3 + z / 1;
        return r;
    }
    
    fn main(x: i32) -> i32 {
        let de = Item { amount = 5; };
        let v = t(de);
        println(v as str);
        let z = 2 && "";
        println(z as str);
        let result = readStr();
        if (result == "yes") {
            main(3);
        }
        return v;
    }
    """
    buffer = StreamBuffer.from_str(program)
    lexer = Lexer(buffer)
    parser = Parser(lexer)
    program = parser.parse()

    inter = Interpreter()

    std_module = load_file("../std/io.fhll")
    inter.visit(std_module)

    inter.visit(program)
    result = inter.run("main", Value(type_name=TypeName("i32"), value=-100))

    print(" == INTER == ")
    print(f"Result: {result}")

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
