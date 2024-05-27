from src.common.location import Location
from src.common.position import Position
from src.parser.ast.constant import Constant
from src.parser.ast.declaration.function_declaration import FunctionDeclaration
from src.parser.ast.declaration.parameter import Parameter
from src.parser.ast.expressions.binary_operation import BinaryOperation
from src.parser.ast.expressions.binary_operation_type import \
    EBinaryOperationType
from src.parser.ast.module import Module
from src.parser.ast.name import Name
from src.parser.ast.statements.assignment import Assignment
from src.parser.ast.statements.block import Block
from src.parser.ast.statements.fn_call import FnCall
from src.parser.ast.statements.return_statement import ReturnStatement
from src.parser.ast.statements.variable_declaration import VariableDeclaration
from src.parser.ast.variant_access import VariantAccess
from tests.parser.test_parser import create_parser


# region Parse Program - Functions
def test_parser_parse__function():
    program = """
    fn add(mut a: f32, b: f32) -> f32 {
        a = a + b;
        return a;
    }
    
    fn main(argc: i32, argv_: Sys::Args) {
        mut let m = 3;
        m = add(m, 5.2);
        println("Done");
    }
    """

    location = irrelevant = Location.at(Position(1, 1))

    expected = Module(
        name="",
        path="",
        function_declarations=[
            FunctionDeclaration(
                name=Name(
                    identifier="add",
                    location=Location(Position(2, 8), Position(2, 10))
                ),
                parameters=[
                    Parameter(
                        name=Name(
                            identifier="a",
                            location=Location(Position(2, 16), Position(2, 16))
                        ),
                        declared_type=Name(
                            identifier="f32",
                            location=Location(Position(2, 19), Position(2, 21))
                        ),
                        mutable=True,
                        location=Location(Position(2, 12), Position(2, 21))
                    ),
                    Parameter(
                        name=Name(
                            identifier="b",
                            location=Location(Position(2, 24), Position(2, 24))
                        ),
                        declared_type=Name(
                            identifier="f32",
                            location=Location(Position(2, 27), Position(2, 29))
                        ),
                        mutable=False,
                        location=Location(Position(2, 24), Position(2, 29))
                    )
                ],
                return_type=Name(
                    identifier="f32",
                    location=Location(Position(2, 35), Position(2, 37))
                ),
                block=Block(
                    body=[
                        Assignment(
                            access=Name(
                                identifier="a",
                                location=Location(Position(3, 9),
                                                  Position(3, 9))
                            ),
                            value=BinaryOperation(
                                left=Name(
                                    identifier="a",
                                    location=Location(Position(3, 13),
                                                      Position(3, 13))
                                ),
                                right=Name(
                                    identifier="b",
                                    location=Location(Position(3, 17),
                                                      Position(3, 17))
                                ),
                                op=EBinaryOperationType.Add,
                                location=Location(Position(3, 13),
                                                  Position(3, 17))
                            ),
                            location=Location(Position(3, 9), Position(3, 17))
                        ),
                        ReturnStatement(
                            value=Name(
                                identifier="a",
                                location=Location(Position(4, 16),
                                                  Position(4, 16))
                            ),
                            location=Location(Position(4, 9), Position(4, 16))
                        )
                    ],
                    location=Location(Position(2, 39), Position(5, 5))
                ),
                location=Location(Position(2, 5), Position(2, 37))
            ),
            FunctionDeclaration(
                name=Name(
                    identifier="main",
                    location=Location(Position(7, 8), Position(7, 11))
                ),
                parameters=[
                    Parameter(
                        name=Name(
                            identifier="argc",
                            location=Location(Position(7, 13), Position(7, 16))
                        ),
                        declared_type=Name(
                            identifier="i32",
                            location=Location(Position(7, 19), Position(7, 21))
                        ),
                        mutable=False,
                        location=Location(Position(7, 13), Position(7, 21))
                    ),
                    Parameter(
                        name=Name(
                            identifier="argv_",
                            location=Location(Position(7, 24), Position(7, 28))
                        ),
                        declared_type=VariantAccess(
                            name=Name(
                                identifier="Args",
                                location=Location(Position(7, 36),
                                                  Position(7, 39))
                            ),
                            parent=Name(
                                identifier="Sys",
                                location=Location(Position(7, 31),
                                                  Position(7, 33))
                            ),
                            location=Location(Position(7, 31), Position(7, 39))
                        ),
                        mutable=False,
                        location=Location(Position(7, 24), Position(7, 39))
                    )
                ],
                return_type=None,
                block=Block(
                    body=[
                        VariableDeclaration(
                            name=Name(
                                identifier="m",
                                location=Location(Position(8, 17),
                                                  Position(8, 17))
                            ),
                            mutable=True,
                            declared_type=None,
                            value=Constant(
                                value=3,
                                location=Location(Position(8, 21),
                                                  Position(8, 21))
                            ),
                            location=Location(Position(8, 9), Position(8, 21))
                        ),
                        Assignment(
                            access=Name(
                                identifier="m",
                                location=Location(Position(9, 9),
                                                  Position(9, 9))
                            ),
                            value=FnCall(
                                name=Name(
                                    identifier="add",
                                    location=Location(Position(9, 13),
                                                      Position(9, 15))
                                ),
                                arguments=[
                                    Name(
                                        identifier="m",
                                        location=Location(Position(9, 17),
                                                          Position(9, 17))
                                    ),
                                    Constant(
                                        value=5.2,
                                        location=Location(Position(9, 20),
                                                          Position(9, 22))
                                    )
                                ],
                                location=Location(Position(9, 13),
                                                  Position(9, 23))
                            ),
                            location=Location(Position(9, 9), Position(9, 23))
                        ),
                        FnCall(
                            name=Name(
                                identifier="println",
                                location=Location(Position(10, 9),
                                                  Position(10, 15))
                            ),
                            arguments=[
                                Constant(
                                    value="Done",
                                    location=Location(Position(10, 17),
                                                      Position(10, 22))
                                )
                            ],
                            location=Location(Position(10, 9),
                                              Position(10, 23))
                        )
                    ],
                    location=Location(Position(7, 42), Position(11, 5))
                ),
                location=Location(Position(7, 5), Position(7, 40))
            )
        ],
        struct_declarations=[],
        enum_declarations=[],
        location=Location.at(Position(1, 1))
    )

    parser = create_parser(program, False)

    module = parser.parse()

    assert module == expected

# endregion
