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
    parser = create_parser("{ let a; }")

    block = parser.parse_block()
    expected = Block(
        body=[
            VariableDeclaration(
                name=Name(
                    identifier="a",
                    location=Location(Position(1, 7), Position(1, 7))
                ),
                mutable=False,
                declared_type=None,
                value=None,
                location=Location(Position(1, 3), Position(1, 7))
            )
        ],
        location=Location(Position(1, 1), Position(1, 10))
    )

    assert block is not None
    assert block == expected
    assert block.location == expected.location


def test_parse_block__open_brace_expected():
    parser = create_parser(" let a; }")

    block = parser.parse_block()

    assert block is None


def test_parse_block__close_brace_expected():
    parser = create_parser("{ let a; ")

    with pytest.raises(BraceExpectedError):
        parser.parse_block()


# endregion

# region Parse Statements List

def test_parse_statements_list__missing_semicolon():
    parser = create_parser("let a; let b")

    with pytest.raises(SemicolonExpectedError):
        parser.parse_statements_list()


# endregion

# region Parse Statement

def test_parse_statement__declaration():
    parser = create_parser("let a")

    statement = parser.parse_statement()

    assert statement is not None
    assert isinstance(statement, VariableDeclaration)


def test_parse_statement__assignment():
    parser = create_parser("a = 3")

    statement = parser.parse_statement()

    assert statement is not None
    assert isinstance(statement, Assignment)


def test_parse_statement__fn_call():
    parser = create_parser("main()")

    statement = parser.parse_statement()

    assert statement is not None
    assert isinstance(statement, FnCall)


def test_parse_statement__return_statement():
    parser = create_parser("return")

    statement = parser.parse_statement()

    assert statement is not None
    assert isinstance(statement, ReturnStatement)


def test_parse_statement__unexpected_token():
    parser = create_parser("name")

    with pytest.raises(UnexpectedTokenError):
        parser.parse_statement()


# endregion

# region Parse Block Statement

def test_parse_statement__block():
    parser = create_parser("{}")

    statement = parser.parse_block_statement()

    assert statement is not None
    assert isinstance(statement, Block)


def test_parse_statement__if_statement():
    parser = create_parser("if (a) {}")

    statement = parser.parse_block_statement()

    assert statement is not None
    assert isinstance(statement, IfStatement)


def test_parse_statement__while_statement():
    parser = create_parser("while (a) {}")

    statement = parser.parse_block_statement()

    assert statement is not None
    assert isinstance(statement, WhileStatement)


def test_parse_statement__match_statement():
    parser = create_parser("match(a) { i32 d => {}; }")

    statement = parser.parse_block_statement()

    assert statement is not None
    assert isinstance(statement, MatchStatement)


# endregion

# region Parse Declaration

def test_parse_declaration__empty():
    parser = create_parser("let a")

    declaration = parser.parse_declaration()
    expected = VariableDeclaration(
        name=Name(
            identifier="a",
            location=Location(Position(1, 5), Position(1, 5))
        ),
        mutable=False,
        declared_type=None,
        value=None,
        location=Location(Position(1, 1), Position(1, 5))
    )

    assert declaration is not None
    assert declaration == expected
    assert declaration.location == expected.location
    assert declaration.name.location == expected.name.location


def test_parse_declaration__mutable():
    parser = create_parser("mut let b")

    declaration = parser.parse_declaration()
    expected = VariableDeclaration(
        name=Name(
            identifier="b",
            location=Location(Position(1, 9), Position(1, 9))
        ),
        mutable=True,
        declared_type=None,
        value=None,
        location=Location(Position(1, 1), Position(1, 9))
    )

    assert declaration is not None
    assert declaration == expected
    assert declaration.location == expected.location


def test_parse_declaration__value():
    parser = create_parser("let c = 3")

    declaration = parser.parse_declaration()
    expected = VariableDeclaration(
        name=Name(
            identifier="c",
            location=Location(Position(1, 5), Position(1, 5))
        ),
        mutable=False,
        declared_type=None,
        value=Constant(
            value=3,
            location=Location(Position(1, 9), Position(1, 9))
        ),
        location=Location(Position(1, 1), Position(1, 9))
    )

    assert declaration is not None
    assert declaration == expected
    assert declaration.location == expected.location


def test_parse_declaration__type():
    parser = create_parser("let d: i32")

    declaration = parser.parse_declaration()
    expected = VariableDeclaration(
        name=Name(
            identifier="d",
            location=Location(Position(1, 5), Position(1, 5))
        ),
        mutable=False,
        declared_type=Name(
            identifier="i32",
            location=Location(Position(1, 8), Position(1, 10))
        ),
        value=None,
        location=Location(Position(1, 1), Position(1, 10))
    )

    assert declaration is not None
    assert declaration == expected
    assert declaration.location == expected.location


def test_parse_declaration__complex():
    parser = create_parser("mut let e: Item = Item {}")

    declaration = parser.parse_declaration()
    expected = VariableDeclaration(
        name=Name(
            identifier="e",
            location=Location(Position(1, 9), Position(1, 9))
        ),
        mutable=True,
        declared_type=Name(
            identifier="Item",
            location=Location(Position(1, 12), Position(1, 15))
        ),
        value=NewStruct(
            variant=Name(
                identifier="Item",
                location=Location(Position(1, 19), Position(1, 22))
            ),
            assignments=[],
            location=Location(Position(1, 19), Position(1, 25))
        ),
        location=Location(Position(1, 1), Position(1, 25))
    )

    assert declaration is not None
    assert declaration == expected


def test_parse_declaration__name_expected():
    parser = create_parser("let =")

    with pytest.raises(NameExpectedError):
        parser.parse_declaration()


def test_parse_declaration__let_expected():
    parser = create_parser("mut e: Item = Item {}")

    with pytest.raises(LetKeywordExpectedError):
        parser.parse_declaration()


def test_parse_declaration__type_expected():
    parser = create_parser("let e: = Item {}")

    with pytest.raises(TypeExpectedError):
        parser.parse_declaration()


def test_parse_declaration__expression_expected():
    parser = create_parser("mut let e: Item = ")

    with pytest.raises(ExpressionExpectedError):
        parser.parse_declaration()


# endregion

# region Parse Assignment

def test_parse_assignment__simple():
    parser = create_parser("a = 3")

    assignment = parser.parse_assignment()
    expected = Assignment(
        access=Name(
            identifier="a",
            location=Location(Position(1, 1), Position(1, 1))
        ),
        value=Constant(
            value=3,
            location=Location(Position(1, 5), Position(1, 5))
        ),
        location=Location(Position(1, 1), Position(1, 5))
    )

    assert assignment is not None
    assert assignment == expected
    assert assignment.location == expected.location


def test_parse_assignment__assign_expected():
    parser = create_parser("a ")

    with pytest.raises(AssignExpectedError):
        parser.parse_assignment()


def test_parse_assignment__expression_expected():
    parser = create_parser("a = ")

    with pytest.raises(ExpressionExpectedError):
        parser.parse_assignment()


# endregion

# region Parse Fn Call

def test_parse_fn_call__zero_arguments():
    parser = create_parser("main()")

    fn_call = parser.parse_fn_call()
    expected = FnCall(
        name=Name(
            identifier="main",
            location=Location(Position(1, 1), Position(1, 4))
        ),
        arguments=[],
        location=Location(Position(1, 1), Position(1, 6))
    )

    assert fn_call is not None
    assert fn_call == expected
    assert fn_call.location == expected.location


def test_parse_fn_call__arguments():
    parser = create_parser("boot(4, \"test\")")

    fn_call = parser.parse_fn_call()
    expected = FnCall(
        name=Name(
            identifier="boot",
            location=Location(Position(1, 1), Position(1, 4))
        ),
        arguments=[
            Constant(
                value=4,
                location=Location(Position(1, 6), Position(1, 6))
            ),
            Constant(
                value="test",
                location=Location(Position(1, 9), Position(1, 14))
            ),
        ],
        location=Location(Position(1, 1), Position(1, 15))
    )

    assert fn_call is not None
    assert fn_call == expected
    assert fn_call.location == expected.location


def test_parse_fn_call__open_parenthesis_expected():
    parser = create_parser("main")

    with pytest.raises(ParenthesisExpectedError):
        parser.parse_fn_call()


def test_parse_fn_call__close_parenthesis_expected():
    parser = create_parser("main(")

    with pytest.raises(ParenthesisExpectedError):
        parser.parse_fn_call()


# endregion

# region Parse Fn Arguments

def test_parse_fn_arguments__empty():
    parser = create_parser("")

    arguments = parser.parse_fn_arguments()
    expected = []

    assert arguments is not None
    assert arguments == expected


def test_parse_fn_arguments__single():
    parser = create_parser("3 + 4")

    arguments = parser.parse_fn_arguments()
    expected = [
        BinaryOperation(
            left=Constant(
                value=3,
                location=Location(Position(1, 1), Position(1, 1))
            ),
            right=Constant(
                value=4,
                location=Location(Position(1, 5), Position(1, 5))
            ),
            op=EBinaryOperationType.Add,
            location=Location(Position(1, 1), Position(1, 5))
        )
    ]

    assert arguments is not None
    assert arguments == expected


def test_parse_fn_arguments__many():
    parser = create_parser("3 * 5, 10 / 3 - 3")

    arguments = parser.parse_fn_arguments()

    assert arguments is not None
    assert len(arguments) == 2


def test_parse_fn_arguments__expression_expected():
    parser = create_parser("1, ")

    with pytest.raises(ExpressionExpectedError):
        parser.parse_fn_arguments()


# endregion

# region Parse New Struct

def test_parse_new_struct__empty():
    parser = create_parser("Item { }")

    new_struct = parser.parse_new_struct()
    expected = NewStruct(
        variant=Name(
            identifier="Item",
            location=Location(Position(1, 1), Position(1, 4))
        ),
        assignments=[],
        location=Location(Position(1, 1), Position(1, 8))
    )

    assert new_struct is not None
    assert new_struct == expected
    assert new_struct.location == expected.location


def test_parse_new_struct__fields():
    parser = create_parser("Item { amount = 3; cost = 5; }")

    new_struct = parser.parse_new_struct()
    expected = NewStruct(
        variant=Name(
            identifier="Item",
            location=Location(Position(1, 1), Position(1, 4))
        ),
        assignments=[
            Assignment(
                access=Name(
                    identifier="amount",
                    location=Location(Position(1, 8), Position(1, 13))
                ),
                value=Constant(
                    value=3,
                    location=Location(Position(1, 17), Position(1, 17))
                ),
                location=Location(Position(1, 8), Position(1, 17))
            ),
            Assignment(
                access=Name(
                    identifier="cost",
                    location=Location(Position(1, 20), Position(1, 23))
                ),
                value=Constant(
                    value=5,
                    location=Location(Position(1, 27), Position(1, 27))
                ),
                location=Location(Position(1, 20), Position(1, 27))
            )
        ],
        location=Location(Position(1, 1), Position(1, 30))
    )

    assert new_struct is not None
    assert new_struct == expected
    assert new_struct.location == expected.location


def test_parse_new_struct__open_brace_expected():
    parser = create_parser("Item ")

    with pytest.raises(BraceExpectedError):
        parser.parse_new_struct()


def test_parse_new_struct__close_brace_expected():
    parser = create_parser("Item {")

    with pytest.raises(BraceExpectedError):
        parser.parse_new_struct()


def test_parse_new_struct__semicolon_after_assignment_expected():
    parser = create_parser("Item { amount = 3 }")

    with pytest.raises(SemicolonExpectedError):
        parser.parse_new_struct()


# endregion

# region Parse Return Statement

def test_parse_return_statement__nothing():
    parser = create_parser("return")

    return_statement = parser.parse_return_statement()
    expected = ReturnStatement(
        value=None,
        location=Location(Position(1, 1), Position(1, 6))
    )

    assert return_statement is not None
    assert return_statement == expected
    assert return_statement.location == expected.location


def test_parse_return_statement__value():
    parser = create_parser("return 5")

    return_statement = parser.parse_return_statement()
    expected = ReturnStatement(
        value=Constant(
            value=5,
            location=Location(Position(1, 8), Position(1, 8))
        ),
        location=Location(Position(1, 1), Position(1, 8))
    )

    assert return_statement is not None
    assert return_statement == expected
    assert return_statement.location == expected.location


# endregion

# region Parse If Statement

def test_parse_if_statement__simple():
    parser = create_parser("if (a) {}")

    if_statement = parser.parse_if_statement()
    expected = IfStatement(
        condition=Name(
            identifier="a",
            location=Location(Position(1, 5), Position(1, 5))
        ),
        block=Block(
            body=[],
            location=Location(Position(1, 8), Position(1, 9))
        ),
        else_block=None,
        location=Location(Position(1, 1), Position(1, 9))
    )

    assert if_statement is not None
    assert if_statement == expected
    assert if_statement.location == expected.location


def test_parse_if_statement_with_else():
    parser = create_parser("if (a) { let b; } else { let c; }")

    if_statement = parser.parse_if_statement()
    expected = IfStatement(
        condition=Name(
            identifier="a",
            location=Location(Position(1, 5), Position(1, 5))
        ),
        block=Block(
            body=[
                VariableDeclaration(
                    name=Name(
                        identifier="b",
                        location=Location(Position(1, 14), Position(1, 14))
                    ),
                    mutable=False,
                    declared_type=None,
                    value=None,
                    location=Location(Position(1, 10), Position(1, 14))
                )
            ],
            location=Location(Position(1, 8), Position(1, 17))
        ),
        else_block=Block(
            body=[
                VariableDeclaration(
                    name=Name(
                        identifier="c",
                        location=Location(Position(1, 30), Position(1, 30))
                    ),
                    mutable=False,
                    declared_type=None,
                    value=None,
                    location=Location(Position(1, 26), Position(1, 30))
                )
            ],
            location=Location(Position(1, 24), Position(1, 33))
        ),
        location=Location(Position(1, 1), Position(1, 33))
    )

    assert if_statement is not None
    assert if_statement == expected
    assert if_statement.location == expected.location


def test_parse_if_statement__open_parenthesis_expected():
    parser = create_parser("if a)")

    with pytest.raises(ParenthesisExpectedError):
        parser.parse_if_statement()


def test_parse_if_statement__close_parenthesis_expected():
    parser = create_parser("if (a")

    with pytest.raises(ParenthesisExpectedError):
        parser.parse_if_statement()


def test_parse_if_statement__expression_expected():
    parser = create_parser("if ()")

    with pytest.raises(ExpressionExpectedError):
        parser.parse_if_statement()


def test_parse_if_statement__block_expected():
    parser = create_parser("if (a)")

    with pytest.raises(BlockExpectedError):
        parser.parse_if_statement()


def test_parse_if_statement__block_for_else_expected():
    parser = create_parser("if (a) {} else")

    with pytest.raises(BlockExpectedError):
        parser.parse_if_statement()


# endregion

# region Parse While Statement

def test_parse_while_statement__basic():
    parser = create_parser("while (true) {}")

    while_statement = parser.parse_while_statement()
    expected = WhileStatement(
        condition=Constant(
            value=True,
            location=Location(Position(1, 8), Position(1, 11))
        ),
        block=Block(
            body=[],
            location=Location(Position(1, 14), Position(1, 15))
        ),
        location=Location(Position(1, 1), Position(1, 15))
    )

    assert while_statement is not None
    assert while_statement == expected
    assert while_statement.location == expected.location


def test_parse_while_statement__open_parenthesis_expected():
    parser = create_parser("while true) {}")

    with pytest.raises(ParenthesisExpectedError):
        parser.parse_while_statement()


def test_parse_while_statement__close_parenthesis_expected():
    parser = create_parser("while (true {}")

    with pytest.raises(ParenthesisExpectedError):
        parser.parse_while_statement()


def test_parse_while_statement__expression_expected():
    parser = create_parser("while () {}")

    with pytest.raises(ExpressionExpectedError):
        parser.parse_while_statement()


def test_parse_while_statement__block_expected():
    parser = create_parser("while (a)")

    with pytest.raises(BlockExpectedError):
        parser.parse_while_statement()


# endregion

# region Parse Match Statement

def test_parse_match_statement():
    parser = create_parser("match (a) { i32 g => {}; }")

    match_statement = parser.parse_match_statement()
    expected = MatchStatement(
        expression=Name(
            identifier="a",
            location=Location(Position(1, 8), Position(1, 8))
        ),
        matchers=[
            Matcher(
                checked_type=Name(
                    identifier="i32",
                    location=Location(Position(1, 13), Position(1, 15))
                ),
                name=Name(
                    identifier="g",
                    location=Location(Position(1, 17), Position(1, 17))
                ),
                block=Block(
                    body=[],
                    location=Location(Position(1, 22), Position(1, 23))
                ),
                location=Location(Position(1, 13), Position(1, 23))
            )
        ],
        location=Location(Position(1, 1), Position(1, 26))
    )

    assert match_statement is not None
    assert match_statement == expected
    assert match_statement.location == expected.location


def test_parse_match_statement__expected_open_parenthesis():
    parser = create_parser("match a) { i32 f => {}; }")

    with pytest.raises(ParenthesisExpectedError):
        parser.parse_match_statement()


def test_parse_match_statement__expected_expression():
    parser = create_parser("match () { i32 d => {}; }")

    with pytest.raises(ExpressionExpectedError):
        parser.parse_match_statement()


def test_parse_match_statement__expected_close_parenthesis():
    parser = create_parser("match (4 { i32 z => {}; }")

    with pytest.raises(ParenthesisExpectedError):
        parser.parse_match_statement()


def test_parse_match_statement__expected_open_brace():
    parser = create_parser("match (a) i32 y => {}; }")

    with pytest.raises(BraceExpectedError):
        parser.parse_match_statement()


def test_parse_match_statement__expected_matchers():
    parser = create_parser("match (a) { }")

    with pytest.raises(MatchersExpectedError):
        parser.parse_match_statement()


def test_parse_match_statement__expected_close_brace():
    parser = create_parser("match (a) { i32 x => {}; ")

    with pytest.raises(BraceExpectedError):
        parser.parse_match_statement()


def test_parse_matchers__single():
    parser = create_parser("f32 g => {};")

    matchers = parser.parse_matchers()
    expected = [
        Matcher(
            checked_type=Name(
                identifier="f32",
                location=Location(Position(1, 1), Position(1, 3))
            ),
            name=Name(
                identifier="g",
                location=Location(Position(1, 5), Position(1, 5))
            ),
            block=Block(
                body=[],
                location=Location(Position(1, 10), Position(1, 11))
            ),
            location=Location(Position(1, 1), Position(1, 11))
        )
    ]

    assert matchers is not None
    assert matchers == expected


def test_parse_matchers__many():
    parser = create_parser("f32 h => {}; i32 x => {};")

    matchers = parser.parse_matchers()
    expected = [
        Matcher(
            checked_type=Name(
                identifier="f32",
                location=Location(Position(1, 1), Position(1, 3))
            ),
            name=Name(
                identifier="h",
                location=Location(Position(1, 5), Position(1, 5))
            ),
            block=Block(
                body=[],
                location=Location(Position(1, 10), Position(1, 11))
            ),
            location=Location(Position(1, 1), Position(1, 11))
        ),
        Matcher(
            checked_type=Name(
                identifier="i32",
                location=Location(Position(1, 14), Position(1, 16))
            ),
            name=Name(
                identifier="x",
                location=Location(Position(1, 18), Position(1, 18))
            ),
            block=Block(
                body=[],
                location=Location(Position(1, 23), Position(1, 24))
            ),
            location=Location(Position(1, 14), Position(1, 24))
        )
    ]

    assert matchers is not None
    assert matchers == expected


def test_parse_matcher__base():
    parser = create_parser("i32 x => {};")

    matcher = parser.parse_matcher()
    expected = Matcher(
        checked_type=Name(
            identifier="i32",
            location=Location(Position(1, 1), Position(1, 3))
        ),
        name=Name(
            identifier="x",
            location=Location(Position(1, 5), Position(1, 5))
        ),
        block=Block(
            body=[],
            location=Location(Position(1, 10), Position(1, 11))
        ),
        location=Location(Position(1, 1), Position(1, 11))
    )

    assert matcher is not None
    assert matcher == expected
    assert matcher.location == expected.location


def test_parse_matcher__name_expected():
    parser = create_parser("i32  => {}")

    with pytest.raises(NameExpectedError):
        parser.parse_matcher()


def test_parse_matcher__arrow_expected():
    parser = create_parser("i32 h {}")

    with pytest.raises(BoldArrowExpectedError):
        parser.parse_matcher()


def test_parse_matcher__block_expected():
    parser = create_parser("i32 g => ")

    with pytest.raises(BlockExpectedError):
        parser.parse_matcher()


def test_parse_matcher__semicolon_expected():
    parser = create_parser("i32 y => {}")

    with pytest.raises(SemicolonExpectedError):
        parser.parse_matcher()

# endregion
