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
    
    fn main(argc: i32, argv: Sys::Args) {
        mut let m = 3;
        m = add(m, 5.2);
        println("Done");
    }
    """

    irrelevant = Location.at(Position(1, 1))

    expected = Module(
        [
            FunctionDeclaration(
                Name("add", irrelevant),
                [
                    Parameter(
                        Name("a", irrelevant),
                        Name("f32", irrelevant),
                        True,
                        irrelevant
                    ),
                    Parameter(
                        Name("b", irrelevant),
                        Name("f32", irrelevant),
                        False,
                        irrelevant
                    )
                ],
                Name("f32", irrelevant),
                Block(
                    [
                        Assignment(
                            Name("a", irrelevant),
                            BinaryOperation(
                                Name("a", irrelevant),
                                Name("b", irrelevant),
                                EBinaryOperationType.Add,
                                irrelevant
                            ),
                            irrelevant
                        ),
                        ReturnStatement(
                            Name("a", irrelevant),
                            irrelevant
                        )
                    ],
                    irrelevant
                ),
                irrelevant
            ),
            FunctionDeclaration(
                Name("main", irrelevant),
                [
                    Parameter(
                        Name("argc", irrelevant),
                        Name("i32", irrelevant),
                        False,
                        irrelevant
                    ),
                    Parameter(
                        Name("argv", irrelevant),
                        VariantAccess(
                            Name("Args", irrelevant),
                            Name("Sys", irrelevant),
                            irrelevant
                        ),
                        False,
                        irrelevant
                    )
                ],
                None,
                Block(
                    [
                        VariableDeclaration(
                            Name("m", irrelevant),
                            True,
                            None,
                            Constant(3, irrelevant),
                            irrelevant
                        ),
                        Assignment(
                            Name("m", irrelevant),
                            FnCall(
                                Name("add", irrelevant),
                                [
                                    Name("m", irrelevant),
                                    Constant(5.2, irrelevant)
                                ],
                                irrelevant
                            ),
                            irrelevant
                        ),
                        FnCall(
                            Name("println", irrelevant),
                            [
                                Constant("Done", irrelevant)
                            ],
                            irrelevant
                        )
                    ],
                    irrelevant
                ),
                irrelevant
            )
        ],
        [],
        []
    )

    parser = create_parser(program, False)

    module = parser.parse()

    assert module == expected

# endregion
