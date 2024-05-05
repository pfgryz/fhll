import pytest

from src.lexer.lexer import Lexer
from src.parser.ast.access import Access
from src.parser.ast.cast import Cast
from src.parser.ast.expressions.binary_operation_type import \
    EBinaryOperationType
from src.parser.ast.expressions.bool_operation_type import EBoolOperationType
from src.parser.ast.expressions.compare_type import ECompareType
from src.parser.ast.expressions.unary_operation_type import EUnaryOperationType
from src.parser.ast.is_compare import IsCompare
from src.parser.ast.statements.fn_call import FnCall
from src.parser.ast.statements.new_struct_statement import NewStructStatement
from src.parser.errors import SyntaxExpectedTokenException, SyntaxException
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

# region Parse Methods

def test_parse():
    parser = create_parser("""
    enum Element {
        struct Button {
            clickCount: i32;
        };
        struct Text {
            text: str;
        };
    }
    
    struct Window {
        nextElement: Element;
    }
    
    fn main() {
        render = 3;
    }
    """, True)

    program = parser.parse()


# endregion


# region Parse Statements

def test_parse_block():
    parser = create_parser("{ let a; }", True)

    block = parser.parse_block()

    assert block is not None
    assert len(block.body) == 1


def test_parse_declaration_simple():
    parser = create_parser("let a", True)

    declaration = parser.parse_declaration()

    assert declaration is not None
    assert declaration.name.identifier == "a"
    assert not declaration.mutable
    assert declaration.type is None
    assert declaration.value is None


def test_parse_declaration_mutable():
    parser = create_parser("mut let b", True)

    declaration = parser.parse_declaration()

    assert declaration is not None
    assert declaration.name.identifier == "b"
    assert declaration.mutable


def test_parse_declaration_with_value():
    parser = create_parser("let c = 3", True)

    declaration = parser.parse_declaration()

    assert declaration is not None
    assert declaration.name.identifier == "c"
    assert declaration.value.value == 3


def test_parse_declaration_with_type():
    parser = create_parser("let d: i32", True)

    declaration = parser.parse_declaration()

    assert declaration is not None
    assert declaration.name.identifier == "d"
    assert declaration.type.identifier == "i32"


def test_parse_declaration_complex():
    parser = create_parser("mut let e: Item = Item {}", True)

    declaration = parser.parse_declaration()

    assert declaration is not None
    assert declaration.name.identifier == "e"
    assert declaration.mutable
    assert declaration.type.identifier == "Item"
    print(declaration.value)
    assert declaration.value.variant.identifier == "Item"


def test_parse_assignment_simple():
    parser = create_parser("a = 3", True)

    assignment = parser.parse_assignment()

    assert assignment is not None
    assert assignment.value.value == 3


def test_parse_assignment_missing_expression():
    parser = create_parser("a = ", True)

    with pytest.raises(SyntaxException):
        parser.parse_assignment()


def test_parse_fn_call_no_arguments():
    parser = create_parser("main()", True)

    fn_call = parser.parse_fn_call()

    assert fn_call is not None
    assert fn_call.name.identifier == "main"
    assert len(fn_call.arguments) == 0


def test_parse_fn_call_with_arguments():
    parser = create_parser("boot(4, \"test\")", True)

    fn_call = parser.parse_fn_call()

    assert fn_call is not None
    assert fn_call.name.identifier == "boot"
    assert len(fn_call.arguments) == 2


def test_parse_fn_arguments_empty():
    parser = create_parser("", True)

    arguments = parser.parse_fn_arguments()

    assert arguments is not None
    assert len(arguments) == 0


def test_parse_fn_arguments_single():
    parser = create_parser("3 + 4", True)

    arguments = parser.parse_fn_arguments()

    assert arguments is not None
    assert len(arguments) == 1


def test_parse_fn_arguments_many():
    parser = create_parser("3 * 5, 10 / 3 - 3", True)

    arguments = parser.parse_fn_arguments()

    assert arguments is not None
    assert len(arguments) == 2


def test_parse_fn_arguments_missing_expression():
    parser = create_parser("1, ", True)

    with pytest.raises(SyntaxException):
        parser.parse_fn_arguments()


def test_parse_new_struct_no_fields():
    parser = create_parser("Item { }", True)

    new_struct = parser.parse_new_struct()

    assert new_struct is not None
    assert new_struct.variant.identifier == "Item"
    assert len(new_struct.assignments) == 0


def test_parse_new_struct_with_fields():
    parser = create_parser("Item { amount = 3; cost = 5; }", True)

    new_struct = parser.parse_new_struct()

    assert new_struct is not None
    assert new_struct.variant.identifier == "Item"
    assert len(new_struct.assignments) == 2


def test_parse_return_statement_void():
    parser = create_parser("return", True)

    return_statement = parser.parse_return_statement()

    assert return_statement is not None
    assert return_statement.value is None


def test_parse_return_statement_with_value():
    parser = create_parser("return 5", True)

    return_statement = parser.parse_return_statement()

    assert return_statement is not None
    assert return_statement.value is not None
    assert return_statement.value.value == 5


def test_parse_if_statement_basic():
    parser = create_parser("if (a) {}", True)

    if_statement = parser.parse_if_statement()

    assert if_statement is not None
    assert if_statement.condition.identifier == "a"
    assert len(if_statement.block.body) == 0
    assert if_statement.else_block is None


def test_parse_if_statement_with_else():
    parser = create_parser("if (a) { let b; } else { let c; let d; }", True)

    if_statement = parser.parse_if_statement()

    assert if_statement is not None
    assert if_statement.condition.identifier == "a"
    assert len(if_statement.block.body) == 1
    assert if_statement.else_block is not None
    assert len(if_statement.else_block.body) == 2


def test_parse_while_statement():
    parser = create_parser("while (true) { let b; }", True)

    while_statement = parser.parse_while_statement()

    assert while_statement is not None
    assert while_statement.condition.value == True
    assert len(while_statement.block.body) == 1


# endregion


# region Parse Expressions

def test_parse_or_expression_pure():
    parser = create_parser("34", True)

    term = parser.parse_expression()

    assert term is not None
    assert term.value == 34


def test_parse_or_expression_default():
    parser = create_parser("7 || 9", True)

    term = parser.parse_expression()

    assert term is not None
    assert term.op == EBoolOperationType.Or
    assert term.left.value == 7
    assert term.right.value == 9


def test_parse_or_expression_many():
    parser = create_parser("0 || 4 || 5", True)

    term = parser.parse_expression()

    assert term is not None
    assert term.op == EBoolOperationType.Or
    assert term.left.op == EBoolOperationType.Or


def test_parse_or_expression_hierarchy():
    parser = create_parser("0 || 4 && 5", True)

    term = parser.parse_expression()

    assert term is not None
    assert term.op == EBoolOperationType.Or
    assert term.right.op == EBoolOperationType.And


def test_parse_or_expression_missing_right():
    parser = create_parser("10 || ", True)

    with pytest.raises(SyntaxException):
        parser.parse_expression()


def test_parse_and_expression_pure():
    parser = create_parser("34", True)

    term = parser.parse_and_expression()

    assert term is not None
    assert term.value == 34


def test_parse_and_expression_default():
    parser = create_parser("7 && 9", True)

    term = parser.parse_and_expression()

    assert term is not None
    assert term.op == EBoolOperationType.And
    assert term.left.value == 7
    assert term.right.value == 9


def test_parse_and_expression_many():
    parser = create_parser("0 && 4 && 5", True)

    term = parser.parse_and_expression()

    assert term is not None
    assert term.op == EBoolOperationType.And
    assert term.left.op == EBoolOperationType.And


def test_parse_and_expression_missing_right():
    parser = create_parser("10 && ", True)

    with pytest.raises(SyntaxException):
        parser.parse_and_expression()


def test_parse_relation_expression_pure():
    parser = create_parser("34", True)

    term = parser.parse_relation_expression()

    assert term is not None
    assert term.value == 34


def test_parse_relation_expression_equal():
    parser = create_parser("3 == 4", True)

    term = parser.parse_relation_expression()

    assert term is not None
    assert term.mode == ECompareType.Equal
    assert term.left.value == 3
    assert term.right.value == 4


def test_parse_relation_expression_not_equal():
    parser = create_parser("3 != 4", True)

    term = parser.parse_relation_expression()

    assert term is not None
    assert term.mode == ECompareType.NotEqual


def test_parse_relation_expression_greater():
    parser = create_parser("3 > 4", True)

    term = parser.parse_relation_expression()

    assert term is not None
    assert term.mode == ECompareType.Greater


def test_parse_relation_expression_less():
    parser = create_parser("3 < 4", True)

    term = parser.parse_relation_expression()

    assert term is not None
    assert term.mode == ECompareType.Less


def test_parse_relation_expression_missing_right():
    parser = create_parser("10 == ", True)

    with pytest.raises(SyntaxException):
        parser.parse_relation_expression()


def test_parse_additive_term_pure():
    parser = create_parser("34", True)

    term = parser.parse_additive_term()

    assert term is not None
    assert term.value == 34


def test_parse_additive_term_add():
    parser = create_parser("7 + 9", True)

    term = parser.parse_additive_term()

    assert term is not None
    assert term.op == EBinaryOperationType.Add
    assert term.left.value == 7
    assert term.right.value == 9


def test_parse_additive_term_sub():
    parser = create_parser("0 - 4", True)

    term = parser.parse_additive_term()

    assert term is not None
    assert term.op == EBinaryOperationType.Sub
    assert term.left.value == 0
    assert term.right.value == 4


def test_parse_additive_term_nested_hierarchy():
    parser = create_parser("0 - 4 * 5", True)

    term = parser.parse_additive_term()

    assert term is not None
    assert term.op == EBinaryOperationType.Sub
    assert term.right.op == EBinaryOperationType.Multiply


def test_parse_additive_term_missing_right():
    parser = create_parser("10 - ", True)

    with pytest.raises(SyntaxException):
        parser.parse_additive_term()


def test_parse_multiplicative_term_pure():
    parser = create_parser("34", True)

    term = parser.parse_multiplicative_term()

    assert term is not None
    assert term.value == 34


def test_parse_multiplicative_term_multiply():
    parser = create_parser("3 * 4", True)

    term = parser.parse_multiplicative_term()

    assert term is not None
    assert term.left.value == 3
    assert term.right.value == 4
    assert term.op == EBinaryOperationType.Multiply


def test_parse_multiplicative_term_divide():
    parser = create_parser("10 / 5", True)

    term = parser.parse_multiplicative_term()

    assert term is not None
    assert term.left.value == 10
    assert term.right.value == 5
    assert term.op == EBinaryOperationType.Divide


def test_parse_multiplicative_term_nested():
    parser = create_parser("3 / 4 * 5", True)

    term = parser.parse_multiplicative_term()

    assert term is not None
    assert term.right.value == 5
    assert term.op == EBinaryOperationType.Multiply
    assert term.left.op == EBinaryOperationType.Divide
    assert term.left.left.value == 3
    assert term.left.right.value == 4


def test_parse_multiplicative_term_missing_right():
    parser = create_parser("10 * ", True)

    with pytest.raises(SyntaxException):
        parser.parse_multiplicative_term()


def test_parse_unary_term_pure():
    parser = create_parser("34", True)

    term = parser.parse_unary_term()

    assert term is not None
    assert term.value == 34


def test_parse_unary_term_minus():
    parser = create_parser("- 4", True)

    term = parser.parse_unary_term()

    assert term is not None
    assert term.operand.value == 4
    assert term.op == EUnaryOperationType.Minus


def test_parse_unary_term_negate():
    parser = create_parser("! true", True)

    term = parser.parse_unary_term()

    assert term is not None
    assert term.operand.value == True
    assert term.op == EUnaryOperationType.Negate


def test_parse_term_int_literal():
    parser = create_parser("34", True)

    term = parser.parse_term()

    assert term is not None
    assert term.value == 34


def test_parse_term_float_literal():
    parser = create_parser("3.14", True)

    term = parser.parse_term()

    assert term is not None
    assert term.value == 3.14


def test_parse_term_string_literal():
    parser = create_parser("\"Hello World\"", True)

    term = parser.parse_term()

    assert term is not None
    assert term.value == "Hello World"


def test_parse_term_boolean_literal():
    parser = create_parser("false", True)

    term = parser.parse_term()

    assert term is not None
    assert not term.value


def test_parse_term_access():
    parser = create_parser("user.name", True)

    term = parser.parse_term()

    assert term is not None
    assert isinstance(term, Access)
    assert term.name.identifier == "name"


def test_parse_term_cast():
    parser = create_parser("user.name as Name", True)

    term = parser.parse_term()

    assert term is not None
    assert isinstance(term, Cast)
    assert term.value.name.identifier == "name"
    assert term.type.identifier == "Name"


def test_parse_term_is_compare():
    parser = create_parser("user.name is Name", True)

    term = parser.parse_term()

    assert term is not None
    assert isinstance(term, IsCompare)
    assert term.value.name.identifier == "name"
    assert term.type.identifier == "Name"


def test_parse_term_fn_call():
    parser = create_parser("main()", True)

    term = parser.parse_term()

    assert term is not None
    assert isinstance(term, FnCall)
    assert term.name.identifier == "main"


def test_parse_term_new_struct():
    parser = create_parser("Item {}", True)

    term = parser.parse_term()

    assert term is not None
    print(term)
    assert isinstance(term, NewStructStatement)
    assert term.variant.identifier == "Item"


def test_parse_term_expression_in_parentheses():
    parser = create_parser("( ( 5 ) )", True)

    term = parser.parse_term()

    assert term is not None
    assert term.value == 5

# endregion
