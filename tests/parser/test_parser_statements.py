import pytest

from src.common.location import Location
from src.common.position import Position
from src.parser.ast.constant import Constant
from src.parser.ast.expressions.binary_operation import BinaryOperation
from src.parser.ast.expressions.binary_operation_type import \
    EBinaryOperationType
from src.parser.ast.name import Name
from src.parser.ast.statements.assignment import Assignment
from src.parser.ast.statements.block import Block
from src.parser.ast.statements.fn_call import FnCall
from src.parser.ast.statements.if_statement import IfStatement
from src.parser.ast.statements.match_statement import MatchStatement
from src.parser.ast.statements.matcher import Matcher
from src.parser.ast.statements.new_struct_statement import NewStruct
from src.parser.ast.statements.return_statement import ReturnStatement
from src.parser.ast.statements.variable_declaration import VariableDeclaration
from src.parser.ast.statements.while_statement import WhileStatement
from src.parser.errors import NameExpectedError, TypeExpectedError, \
    ExpressionExpectedError, LetKeywordExpectedError, AssignExpectedError, \
    ParenthesisExpectedError, BraceExpectedError, SemicolonExpectedError, \
    BlockExpectedError, UnexpectedTokenError, BoldArrowExpectedError, \
    MatchersExpectedError
from tests.parser.test_parser import create_parser


# region Parse Block

def test_parse_block():
    parser = create_parser("{ let a; }", True)

    block = parser.parse_block()
    expected = Block(
        [
            VariableDeclaration(
                Name("a", Location(Position(1, 7), Position(1, 7))),
                False,
                None,
                None,
                Location(Position(1, 3), Position(1, 7))
            )
        ],
        Location(Position(1, 1), Position(1, 10))
    )

    assert block is not None
    assert block == expected
    assert block.location == expected.location


def test_parse_block__open_brace_expected():
    parser = create_parser(" let a; }", True)

    block = parser.parse_block()

    assert block is None


def test_parse_block__close_brace_expected():
    parser = create_parser("{ let a; ", True)

    with pytest.raises(BraceExpectedError):
        parser.parse_block()


# endregion

# region Parse Statements List

def test_parse_statements_list__missing_semicolon():
    parser = create_parser("let a; let b", True)

    with pytest.raises(SemicolonExpectedError):
        parser.parse_statements_list()


# endregion

# region Parse Statement

def test_parse_statement__declaration():
    parser = create_parser("let a", True)

    statement = parser.parse_statement()

    assert statement is not None
    assert isinstance(statement, VariableDeclaration)


def test_parse_statement__assignment():
    parser = create_parser("a = 3", True)

    statement = parser.parse_statement()

    assert statement is not None
    assert isinstance(statement, Assignment)


def test_parse_statement__fn_call():
    parser = create_parser("main()", True)

    statement = parser.parse_statement()

    assert statement is not None
    assert isinstance(statement, FnCall)


def test_parse_statement__block():
    parser = create_parser("{}", True)

    statement = parser.parse_statement()

    assert statement is not None
    assert isinstance(statement, Block)


def test_parse_statement__return_statement():
    parser = create_parser("return", True)

    statement = parser.parse_statement()

    assert statement is not None
    assert isinstance(statement, ReturnStatement)


def test_parse_statement__if_statement():
    parser = create_parser("if (a) {}", True)

    statement = parser.parse_statement()

    assert statement is not None
    assert isinstance(statement, IfStatement)


def test_parse_statement__while_statement():
    parser = create_parser("while (a) {}", True)

    statement = parser.parse_statement()

    assert statement is not None
    assert isinstance(statement, WhileStatement)


def test_parse_statement__match_statement():
    parser = create_parser("match(a) { i32 d => {}; }", True)

    statement = parser.parse_statement()

    assert statement is not None
    assert isinstance(statement, MatchStatement)


def test_parse_statement__unexpected_token():
    parser = create_parser("name", True)

    with pytest.raises(UnexpectedTokenError):
        parser.parse_statement()


# endregion

# region Parse Declaration

def test_parse_declaration__empty():
    parser = create_parser("let a", True)

    declaration = parser.parse_declaration()
    expected = VariableDeclaration(
        Name("a", Location(Position(1, 5), Position(1, 5))),
        False,
        None,
        None,
        Location(Position(1, 1), Position(1, 5))
    )

    assert declaration is not None
    assert declaration == expected
    assert declaration.location == expected.location
    assert declaration.name.location == expected.name.location


def test_parse_declaration__mutable():
    parser = create_parser("mut let b", True)

    declaration = parser.parse_declaration()
    expected = VariableDeclaration(
        Name("b", Location(Position(1, 9), Position(1, 9))),
        True,
        None,
        None,
        Location(Position(1, 1), Position(1, 9))
    )

    assert declaration is not None
    assert declaration == expected
    assert declaration.location == expected.location


def test_parse_declaration__value():
    parser = create_parser("let c = 3", True)

    declaration = parser.parse_declaration()
    expected = VariableDeclaration(
        Name("c", Location(Position(1, 5), Position(1, 5))),
        False,
        None,
        Constant(
            3,
            Location(Position(1, 9), Position(1, 9))
        ),
        Location(Position(1, 1), Position(1, 9))
    )

    assert declaration is not None
    assert declaration == expected
    assert declaration.location == expected.location


def test_parse_declaration__type():
    parser = create_parser("let d: i32", True)

    declaration = parser.parse_declaration()
    expected = VariableDeclaration(
        Name("d", Location(Position(1, 5), Position(1, 5))),
        False,
        Name("i32", Location(Position(1, 8), Position(1, 10))),
        None,
        Location(Position(1, 1), Position(1, 10))
    )

    assert declaration is not None
    assert declaration == expected
    assert declaration.location == expected.location


def test_parse_declaration__complex():
    parser = create_parser("mut let e: Item = Item {}", True)

    declaration = parser.parse_declaration()
    expected = VariableDeclaration(
        Name("e", Location(Position(1, 9), Position(1, 9))),
        True,
        Name("Item", Location(Position(1, 12), Position(1, 15))),
        NewStruct(
            Name("Item", Location(Position(1, 19), Position(1, 22))),
            [],
            Location(Position(1, 19), Position(1, 25))
        ),
        Location(Position(1, 1), Position(1, 25))
    )

    assert declaration is not None
    assert declaration == expected


def test_parse_declaration__name_expected():
    parser = create_parser("let =", True)

    with pytest.raises(NameExpectedError):
        parser.parse_declaration()


def test_parse_declaration__let_expected():
    parser = create_parser("mut e: Item = Item {}", True)

    with pytest.raises(LetKeywordExpectedError):
        parser.parse_declaration()


def test_parse_declaration__type_expected():
    parser = create_parser("let e: = Item {}", True)

    with pytest.raises(TypeExpectedError):
        parser.parse_declaration()


def test_parse_declaration__expression_expected():
    parser = create_parser("mut let e: Item = ", True)

    with pytest.raises(ExpressionExpectedError):
        parser.parse_declaration()


# endregion

# region Parse Assignment

def test_parse_assignment__simple():
    parser = create_parser("a = 3", True)

    assignment = parser.parse_assignment()
    expected = Assignment(
        Name("a", Location(Position(1, 1), Position(1, 1))),
        Constant(3, Location(Position(1, 5), Position(1, 5))),
        Location(Position(1, 1), Position(1, 5))
    )

    assert assignment is not None
    assert assignment == expected
    assert assignment.location == expected.location


def test_parse_assignment__assign_expected():
    parser = create_parser("a ", True)

    with pytest.raises(AssignExpectedError):
        parser.parse_assignment()


def test_parse_assignment__expression_expected():
    parser = create_parser("a = ", True)

    with pytest.raises(ExpressionExpectedError):
        parser.parse_assignment()


# endregion

# region Parse Fn Call

def test_parse_fn_call__zero_arguments():
    parser = create_parser("main()", True)

    fn_call = parser.parse_fn_call()
    expected = FnCall(
        Name("main", Location(Position(1, 1), Position(1, 4))),
        [],
        Location(Position(1, 1), Position(1, 6))
    )

    assert fn_call is not None
    assert fn_call == expected
    assert fn_call.location == expected.location


def test_parse_fn_call__arguments():
    parser = create_parser("boot(4, \"test\")", True)

    fn_call = parser.parse_fn_call()
    expected = FnCall(
        Name("boot", Location(Position(1, 1), Position(1, 4))),
        [
            Constant(4, Location(Position(1, 6), Position(1, 6))),
            Constant("test", Location(Position(1, 10), Position(1, 13))),
        ],
        Location(Position(1, 1), Position(1, 15))
    )

    assert fn_call is not None
    assert fn_call == expected
    assert fn_call.location == expected.location


def test_parse_fn_call__open_parenthesis_expected():
    parser = create_parser("main", True)

    with pytest.raises(ParenthesisExpectedError):
        parser.parse_fn_call()


def test_parse_fn_call__close_parenthesis_expected():
    parser = create_parser("main(", True)

    with pytest.raises(ParenthesisExpectedError):
        parser.parse_fn_call()


# endregion

# region Parse Fn Arguments

def test_parse_fn_arguments__empty():
    parser = create_parser("", True)

    arguments = parser.parse_fn_arguments()
    expected = []

    assert arguments is not None
    assert arguments == expected


def test_parse_fn_arguments__single():
    parser = create_parser("3 + 4", True)

    arguments = parser.parse_fn_arguments()
    expected = [
        BinaryOperation(
            Constant(3, Location(Position(1, 1), Position(1, 1))),
            Constant(4, Location(Position(1, 5), Position(1, 5))),
            EBinaryOperationType.Add,
            Location(Position(1, 1), Position(1, 5))
        )
    ]

    assert arguments is not None
    assert arguments == expected


def test_parse_fn_arguments__many():
    parser = create_parser("3 * 5, 10 / 3 - 3", True)

    arguments = parser.parse_fn_arguments()

    assert arguments is not None
    assert len(arguments) == 2


def test_parse_fn_arguments__expression_expected():
    parser = create_parser("1, ", True)

    with pytest.raises(ExpressionExpectedError):
        parser.parse_fn_arguments()


# endregion

# region Parse New Struct

def test_parse_new_struct__empty():
    parser = create_parser("Item { }", True)

    new_struct = parser.parse_new_struct()
    expected = NewStruct(
        Name("Item", Location(Position(1, 1), Position(1, 4))),
        [],
        Location(Position(1, 1), Position(1, 8))
    )

    assert new_struct is not None
    assert new_struct == expected
    assert new_struct.location == expected.location


def test_parse_new_struct__fields():
    parser = create_parser("Item { amount = 3; cost = 5; }", True)

    new_struct = parser.parse_new_struct()
    expected = NewStruct(
        Name("Item", Location(Position(1, 1), Position(1, 4))),
        [
            Assignment(
                Name("amount", Location(Position(1, 8), Position(1, 13))),
                Constant(3, Location(Position(1, 17), Position(1, 17))),
                Location(Position(1, 8), Position(1, 17))
            ),
            Assignment(
                Name("cost", Location(Position(1, 20), Position(1, 23))),
                Constant(5, Location(Position(1, 27), Position(1, 27))),
                Location(Position(1, 20), Position(1, 27))
            )
        ],
        Location(Position(1, 1), Position(1, 30))
    )

    assert new_struct is not None
    assert new_struct == expected
    assert new_struct.location == expected.location


def test_parse_new_struct__open_brace_expected():
    parser = create_parser("Item ", True)

    with pytest.raises(BraceExpectedError):
        parser.parse_new_struct()


def test_parse_new_struct__close_brace_expected():
    parser = create_parser("Item {", True)

    with pytest.raises(BraceExpectedError):
        parser.parse_new_struct()


def test_parse_new_struct__semicolon_after_assignment_expected():
    parser = create_parser("Item { amount = 3 }", True)

    with pytest.raises(SemicolonExpectedError):
        parser.parse_new_struct()


# endregion

# region Parse Return Statement

def test_parse_return_statement__nothing():
    parser = create_parser("return", True)

    return_statement = parser.parse_return_statement()
    expected = ReturnStatement(
        None,
        Location(Position(1, 1), Position(1, 6))
    )

    assert return_statement is not None
    assert return_statement == expected
    assert return_statement.location == expected.location


def test_parse_return_statement__value():
    parser = create_parser("return 5", True)

    return_statement = parser.parse_return_statement()
    expected = ReturnStatement(
        Constant(5, Location(Position(1, 8), Position(1, 8))),
        Location(Position(1, 1), Position(1, 8))
    )

    assert return_statement is not None
    assert return_statement == expected
    assert return_statement.location == expected.location


# endregion

# region Parse If Statement

def test_parse_if_statement__simple():
    parser = create_parser("if (a) {}", True)

    if_statement = parser.parse_if_statement()
    expected = IfStatement(
        Name("a", Location(Position(1, 5), Position(1, 5))),
        Block(
            [],
            Location(Position(1, 8), Position(1, 9))
        ),
        None,
        Location(Position(1, 1), Position(1, 9))
    )

    assert if_statement is not None
    assert if_statement == expected
    assert if_statement.location == expected.location


def test_parse_if_statement_with_else():
    parser = create_parser("if (a) { let b; } else { let c; }", True)

    if_statement = parser.parse_if_statement()
    expected = IfStatement(
        Name("a", Location(Position(1, 5), Position(1, 5))),
        Block(
            [
                VariableDeclaration(
                    Name("b", Location(Position(1, 14), Position(1, 14))),
                    False,
                    None,
                    None,
                    Location(Position(1, 10), Position(1, 14))
                )
            ],
            Location(Position(1, 8), Position(1, 17))
        ),
        Block(
            [
                VariableDeclaration(
                    Name("c", Location(Position(1, 30), Position(1, 30))),
                    False,
                    None,
                    None,
                    Location(Position(1, 26), Position(1, 26))
                )
            ],
            Location(Position(1, 24), Position(1, 33))
        ),
        Location(Position(1, 1), Position(1, 33))
    )

    assert if_statement is not None
    assert if_statement == expected
    assert if_statement.location == expected.location


def test_parse_if_statement__open_parenthesis_expected():
    parser = create_parser("if a)", True)

    with pytest.raises(ParenthesisExpectedError):
        parser.parse_if_statement()


def test_parse_if_statement__close_parenthesis_expected():
    parser = create_parser("if (a", True)

    with pytest.raises(ParenthesisExpectedError):
        parser.parse_if_statement()


def test_parse_if_statement__expression_expected():
    parser = create_parser("if ()", True)

    with pytest.raises(ExpressionExpectedError):
        parser.parse_if_statement()


def test_parse_if_statement__block_expected():
    parser = create_parser("if (a)", True)

    with pytest.raises(BlockExpectedError):
        parser.parse_if_statement()


def test_parse_if_statement__block_for_else_expected():
    parser = create_parser("if (a) {} else", True)

    with pytest.raises(BlockExpectedError):
        parser.parse_if_statement()


# endregion

# region Parse While Statement

def test_parse_while_statement__basic():
    parser = create_parser("while (true) {}", True)

    while_statement = parser.parse_while_statement()
    expected = WhileStatement(
        Constant(True, Location(Position(1, 8), Position(1, 11))),
        Block(
            [],
            Location(Position(1, 14), Position(1, 15))
        ),
        Location(Position(1, 1), Position(1, 15))
    )

    assert while_statement is not None
    assert while_statement == expected
    assert while_statement.location == expected.location


def test_parse_while_statement__open_parenthesis_expected():
    parser = create_parser("while true) {}", True)

    with pytest.raises(ParenthesisExpectedError):
        parser.parse_while_statement()


def test_parse_while_statement__close_parenthesis_expected():
    parser = create_parser("while (true {}", True)

    with pytest.raises(ParenthesisExpectedError):
        parser.parse_while_statement()


def test_parse_while_statement__expression_expected():
    parser = create_parser("while () {}", True)

    with pytest.raises(ExpressionExpectedError):
        parser.parse_while_statement()


def test_parse_while_statement__block_expected():
    parser = create_parser("while (a)", True)

    with pytest.raises(BlockExpectedError):
        parser.parse_while_statement()


# endregion

# region Parse Match Statement

def test_parse_match_statement():
    parser = create_parser("match (a) { i32 g => {}; }", True)

    match_statement = parser.parse_match_statement()
    expected = MatchStatement(
        Name("a", Location(Position(1, 8), Position(1, 8))),
        [
            Matcher(
                Name("i32", Location(Position(1, 13), Position(1, 15))),
                Name("g", Location(Position(1, 17), Position(1, 17))),
                Block(
                    [],
                    Location(Position(1, 22), Position(1, 23))
                ),
                Location(Position(1, 13), Position(1, 23))
            )
        ],
        Location(Position(1, 1), Position(1, 26))
    )

    assert match_statement is not None
    assert match_statement == expected
    assert match_statement.location == expected.location


def test_parse_match_statement__expected_open_parenthesis():
    parser = create_parser("match a) { i32 f => {}; }", True)

    with pytest.raises(ParenthesisExpectedError):
        parser.parse_match_statement()


def test_parse_match_statement__expected_expression():
    parser = create_parser("match () { i32 d => {}; }", True)

    with pytest.raises(ExpressionExpectedError):
        parser.parse_match_statement()


def test_parse_match_statement__expected_close_parenthesis():
    parser = create_parser("match (4 { i32 z => {}; }", True)

    with pytest.raises(ParenthesisExpectedError):
        parser.parse_match_statement()


def test_parse_match_statement__expected_open_brace():
    parser = create_parser("match (a) i32 y => {}; }", True)

    with pytest.raises(BraceExpectedError):
        parser.parse_match_statement()


def test_parse_match_statement__expected_matchers():
    parser = create_parser("match (a) { }", True)

    with pytest.raises(MatchersExpectedError):
        parser.parse_match_statement()


def test_parse_match_statement__expected_close_brace():
    parser = create_parser("match (a) { i32 x => {}; ", True)

    with pytest.raises(BraceExpectedError):
        parser.parse_match_statement()


def test_parse_matchers__single():
    parser = create_parser("f32 g => {};", True)

    matchers = parser.parse_matchers()
    expected = [
        Matcher(
            Name("f32", Location(Position(1, 1), Position(1, 3))),
            Name("g", Location(Position(1, 5), Position(1, 5))),
            Block(
                [],
                Location(Position(1, 10), Position(1, 11))
            ),
            Location(Position(1, 1), Position(1, 11))
        )
    ]

    assert matchers is not None
    assert matchers == expected


def test_parse_matchers__many():
    parser = create_parser("f32 h => {}; i32 x => {};", True)

    matchers = parser.parse_matchers()
    expected = [
        Matcher(
            Name("f32", Location(Position(1, 1), Position(1, 3))),
            Name("h", Location(Position(1, 5), Position(1, 5))),
            Block(
                [],
                Location(Position(1, 10), Position(1, 11))
            ),
            Location(Position(1, 1), Position(1, 11))
        ),
        Matcher(
            Name("i32", Location(Position(1, 14), Position(1, 16))),
            Name("x", Location(Position(1, 18), Position(1, 18))),
            Block(
                [],
                Location(Position(1, 23), Position(1, 24))
            ),
            Location(Position(1, 12), Position(1, 24))
        )
    ]

    assert matchers is not None
    assert matchers == expected


def test_parse_matcher__base():
    parser = create_parser("i32 x => {};", True)

    matcher = parser.parse_matcher()
    expected = Matcher(
        Name("i32", Location(Position(1, 1), Position(1, 3))),
        Name("x", Location(Position(1, 5), Position(1, 5))),
        Block(
            [],
            Location(Position(1, 10), Position(1, 11))
        ),
        Location(Position(1, 1), Position(1, 11))
    )

    assert matcher is not None
    assert matcher == expected
    assert matcher.location == expected.location


def test_parse_matcher__name_expected():
    parser = create_parser("i32  => {}", True)

    with pytest.raises(NameExpectedError):
        parser.parse_matcher()


def test_parse_matcher__arrow_expected():
    parser = create_parser("i32 h {}", True)

    with pytest.raises(BoldArrowExpectedError):
        parser.parse_matcher()


def test_parse_matcher__block_expected():
    parser = create_parser("i32 g => ", True)

    with pytest.raises(BlockExpectedError):
        parser.parse_matcher()


def test_parse_matcher__semicolon_expected():
    parser = create_parser("i32 y => {}", True)

    with pytest.raises(SemicolonExpectedError):
        parser.parse_matcher()

# endregion
