import warnings
from pprint import pprint
from typing import Optional

from src.common.location import Location
from src.lexer.lexer import Lexer
from src.lexer.token import Token
from src.lexer.token_kind import TokenKind
from src.parser.ast.__old_program import Program
from src.parser.ast.access import Access
from src.parser.ast.cast import Cast
from src.parser.ast.common import Type, Parameters
from src.parser.ast.constant import Constant
from src.parser.ast.enum_declaration import EnumDeclaration
from src.parser.ast.expressions.binary_operation import BinaryOperation
from src.parser.ast.expressions.binary_operation_type import \
    EBinaryOperationType
from src.parser.ast.expressions.bool_operation import BoolOperation
from src.parser.ast.expressions.bool_operation_type import EBoolOperationType
from src.parser.ast.expressions.compare import Compare
from src.parser.ast.expressions.compare_type import ECompareMode
from src.parser.ast.expressions.unary_operation import UnaryOperation
from src.parser.ast.expressions.unary_operation_type import EUnaryOperationType
from src.parser.ast.field_declaration import FieldDeclaration
from src.parser.ast.function_declaration import FunctionDeclaration
from src.parser.ast.is_compare import IsCompare
from src.parser.ast.name import Name
from src.parser.ast.parameter import Parameter
from src.parser.ast.struct_declaration import StructDeclaration
from src.parser.ast.variant_access import VariantAccess
from src.parser.ebnf import ebnf
from src.parser.errors import SyntaxExpectedTokenException, SyntaxException
from src.utils.buffer import StreamBuffer


def untested():
    def wrapper(func):
        warnings.warn(f"This function {func.__name__} is not tested")
        return func

    return wrapper


type Term = Constant | Access | IsCompare | Cast
type Expression = Compare | BinaryOperation | UnaryOperation | Term


class Parser:
    _builtin_types_kinds = [
        TokenKind.I32,
        TokenKind.F32,
        TokenKind.Bool,
        TokenKind.Str
    ]

    _literal_kinds = [
        TokenKind.Integer,
        TokenKind.Float,
        TokenKind.String,
        TokenKind.Boolean
    ]

    _and_op = TokenKind.And

    _or_op = TokenKind.Or

    _relation_op = [
        TokenKind.Equal,
        TokenKind.NotEqual,
        TokenKind.Less,
        TokenKind.Greater
    ]

    _additive_op = [
        TokenKind.Plus,
        TokenKind.Minus
    ]

    _multiplicative_op = [
        TokenKind.Multiply,
        TokenKind.Divide
    ]

    _unary_op = [
        TokenKind.Minus,
        TokenKind.Negate
    ]

    # region Dunder Methods
    def __init__(self, lexer: Lexer):
        self._lexer = lexer
        self._token = None

    # endregion

    # region Helper Methods

    def consume(self) -> Token:
        token = self._token
        self._token = self._lexer.get_next_token()
        return token

    def consume_if(self, kind: TokenKind) -> Optional[Token]:
        if self._token.kind == kind:
            return self.consume()

        return None

    def consume_match(self, kinds: list[TokenKind]) -> Optional[Token]:
        for kind in kinds:
            if token := self.consume_if(kind):
                return token

        return None

    def expect(self, kind: TokenKind) -> Token:
        return self.expect_conditional(kind, True)

    def expect_conditional(self, kind: TokenKind, condition: bool) \
            -> Optional[Token]:
        if token := self.consume_if(kind):
            return token

        if condition:
            raise SyntaxExpectedTokenException(kind, self._token.kind,
                                               self._token.location.begin)

        return None

    def expect_match(self, kinds: list[TokenKind]) -> Optional[Token]:
        if token := self.consume_match(kinds):
            return token

        raise SyntaxExpectedTokenException(kinds, self._token.kind,
                                           self._token.location.begin)

    # endregion

    # region Parse Methods

    @ebnf(
        "Program",
        "{ FunctionDeclaration | StructDeclaration | EnumDeclaration }"
    )
    @untested()
    def parse(self) -> 'Program':
        raise NotImplementedError()

    # region Parse Functions

    @ebnf(
        "FunctionDeclaration",
        "'fn', identifier, '(', [ Parameters ], ')', [ '->', Type ], Block"
    )
    def parse_function_declaration(self) -> Optional['FunctionDeclaration']:
        if not (fn := self.consume_if(TokenKind.Fn)):
            return None

        name = self.expect(TokenKind.Identifier)

        # Parameters
        self.expect(TokenKind.ParenthesisOpen)
        parameters = self.parse_parameters()
        close = self.expect(TokenKind.ParenthesisClose)

        # Return Type
        returns = None
        if self.consume_if(TokenKind.Arrow):
            returns = self.parse_type()

        # Block
        block = None  # @TODO: self.parse_block()

        return FunctionDeclaration(
            Name(name.value, name.location),
            parameters,
            returns,
            Location(
                fn.location.begin,
                close.location.end
            )
        )

    @ebnf(
        "Parameters", "{ ',', Parameter }"
    )
    def parse_parameters(self) -> Parameters:
        parameters = []

        if parameter := self.parse_parameter():
            parameters.append(parameter)

        while self.consume_if(TokenKind.Comma):
            if parameter := self.parse_parameter():
                parameters.append(parameter)
            else:
                raise SyntaxException("Expected parameter",
                                      self._token.location.begin)

        return parameters

    @ebnf(
        "Parameter", "[ 'mut' ], identifier, ':', Type"
    )
    def parse_parameter(self) -> Optional[Parameter]:
        mut = self.consume_if(TokenKind.Mut)
        mutable = mut is not None

        if not (identifier := self.expect_conditional(TokenKind.Identifier,
                                                      mutable)):
            return None

        self.expect(TokenKind.Colon)

        typ = self.parse_type()

        return Parameter(
            Name(identifier.value, identifier.location),
            typ,
            mutable,
            Location(
                mut.location.begin if mutable else identifier.location.begin,
                typ.location.end
            )
        )

    # endregion

    # region Parse Structs

    @ebnf(
        "StructDeclaration",
        "'struct', identifier, '{', { FieldDeclaration }, '}'"
    )
    def parse_struct_declaration(self) -> Optional['StructDeclaration']:
        if not (struct := self.consume_if(TokenKind.Struct)):
            return None

        identifier = self.expect(TokenKind.Identifier)

        self.expect(TokenKind.BraceOpen)

        fields = []
        while field := self.parse_field_declaration():
            fields.append(field)

        close = self.expect(TokenKind.BraceClose)

        return StructDeclaration(
            Name(identifier.value, identifier.location),
            fields,
            Location(
                struct.location.begin,
                close.location.end
            )
        )

    @ebnf(
        "FieldDeclaration",
        "identifier, ':', Type, ';'"
    )
    def parse_field_declaration(self) -> Optional[FieldDeclaration]:
        if not (identifier := self.consume_if(TokenKind.Identifier)):
            return None

        self.expect(TokenKind.Colon)
        typ = self.parse_type()
        self.expect(TokenKind.Semicolon)

        return FieldDeclaration(
            Name(identifier.value, identifier.location),
            typ
        )

    # endregion

    # region Parse Enum

    @ebnf(
        "EnumDeclaration",
        "'enum', identifier, "
        "'{', { (EnumDeclaration | StructDeclaration) }, '}'"
    )
    def parse_enum_declaration(self) -> Optional[EnumDeclaration]:
        if not (enum := self.consume_if(TokenKind.Enum)):
            return None

        identifier = self.consume_if(TokenKind.Identifier)

        self.expect(TokenKind.BraceOpen)

        variants = []
        while variant := self.parse_struct_declaration() \
                         or self.parse_enum_declaration():
            variants.append(variant)
            self.expect(TokenKind.Semicolon)

        close = self.expect(TokenKind.BraceClose)

        return EnumDeclaration(
            Name(identifier.value, identifier.location),
            variants,
            Location(
                enum.location.begin,
                close.location.end
            )
        )

    # endregion

    # region Parse Statements

    @ebnf(
        "Block",
        "'{', StatementList, '}'"
    )
    @untested()
    def parse_block(self) -> Optional['Block']:
        raise NotImplementedError()

    @ebnf(
        "StatementList",
        "{ Statement, ';'}"
    )
    @untested()
    def parse_statements_list(self) -> list['Statement']:
        raise NotImplementedError()

    @ebnf(
        "Statement",
        "Declaration | Assignment | FnCall | NewStruct "
        "| Block | ReturnStatement | IfStatement | WhileStatement"
    )
    @untested()
    def parse_statement(self) -> Optional['Statement']:
        raise NotImplementedError()

    @ebnf(
        "Declaration",
        "[ 'mut' ], 'let', identifier, [ ':', Type ], [ '=', Expression ]"
    )
    @untested()
    def parse_declaration(self) -> Optional['Declaration']:
        raise NotImplementedError()

    @ebnf(
        "Assignment",
        "Access, '=', Expression"
    )
    @untested()
    def parse_assignment(self) -> Optional['Assignment']:
        raise NotImplementedError()

    @ebnf(
        "FnCall",
        "identifier, '(', [ FnArguments ], ')'"
    )
    @untested()
    def parse_fn_call(self) -> Optional['FnCall']:
        raise NotImplementedError()

    @ebnf(
        "FnArguments",
        "Expression, {, ',', Expression }"
    )
    @untested()
    def parse_fn_arguments(self) -> list['FnArgument']:
        raise NotImplementedError()

    @ebnf(
        "NewStruct",
        "VariantAccess, '{', [ Assignment, ';' ], '}'"
    )
    @untested()
    def parse_new_struct(self) -> Optional['NewStruct']:
        pass

    @ebnf(
        "ReturnStatement",
        "'return', [ Expression ]"
    )
    @untested()
    def parse_return_statement(self) -> Optional['ReturnStatement']:
        raise NotImplementedError()

    @ebnf(
        "IfStatement",
        "'if', '(', Expression, ')', Block, [ 'else', Block ]"
    )
    @untested()
    def parse_if_statement(self) -> Optional['IfStatement']:
        raise NotImplementedError()

    @ebnf(
        "WhileStatement",
        "'while', '(', Expression, ')', Block"
    )
    @untested()
    def parse_while_statement(self) -> Optional['WhileStatement']:
        raise NotImplementedError()

    # endregion

    # region Parse Access

    @ebnf(
        "Access",
        "identifier, { '.', identifier }"
    )
    def parse_access(self) -> Optional[Name | Access]:
        if not (element := self.consume_if(TokenKind.Identifier)):
            return None

        result = Name(element.value, element.location)

        while self.consume_if(TokenKind.Period):
            element = self.expect(TokenKind.Identifier)

            result = Access(
                Name(element.value, element.location),
                result
            )

        return result

    @ebnf(
        "VariantAccess",
        "identifier, { '::', identifier }"
    )
    def parse_variant_access(self) -> Optional[Name | VariantAccess]:
        if not (element := self.consume_if(TokenKind.Identifier)):
            return None

        result = Name(element.value, element.location)

        while self.consume_if(TokenKind.DoubleColon):
            element = self.expect(TokenKind.Identifier)

            result = VariantAccess(
                Name(element.value, element.location),
                result
            )

        return result

    @ebnf(
        "Type",
        "builtin_type | VariantAccess"
    )
    def parse_type(self) -> Optional[Type]:
        if builtin := self.consume_match(self._builtin_types_kinds):
            return Name(builtin.kind.value, builtin.location)

        return self.parse_variant_access()

    # endregion

    # region Parse Expressions

    @ebnf(
        "Expression",
        "AndExpression, { or_op, AndExpression }"
    )
    @untested()
    def parse_expression(self) -> Optional['Expression']:
        left = self.parse_and_expression()

        while op := self.consume_if(self._or_op):
            if not (right := self.parse_and_expression()):
                raise SyntaxException("Missing term after operator",
                                      self._token.location.begin)

            left = BoolOperation(
                left,
                right,
                EBoolOperationType.from_token_kind(op.kind),
                Location(
                    left.location.begin,
                    right.location.end
                )
            )

        return left

    @ebnf(
        "AndExpression",
        "RelationExpression, { and_op, RelationExpression }"
    )
    @untested()
    def parse_and_expression(self) -> Optional['Expression']:
        left = self.parse_relation_expression()

        while op := self.consume_if(self._and_op):
            if not (right := self.parse_relation_expression()):
                raise SyntaxException("Missing term after operator",
                                      self._token.location.begin)

            left = BoolOperation(
                left,
                right,
                EBoolOperationType.from_token_kind(op.kind),
                Location(
                    left.location.begin,
                    right.location.end
                )
            )

        return left

    @ebnf(
        "RelationExpression",
        "AdditiveTerm, [ relation_op, AdditiveTerm ]"
    )
    def parse_relation_expression(self) -> Optional['Expression']:
        left = self.parse_additive_term()

        if op := self.consume_match(self._relation_op):
            if not (right := self.parse_additive_term()):
                raise SyntaxException("Missing term after operator",
                                      self._token.location.begin)

            left = Compare(
                left,
                right,
                ECompareMode.from_token_kind(op.kind),
                Location(
                    left.location.begin,
                    right.location.end
                )
            )

        return left

    @ebnf(
        "AdditiveTerm",
        "MultiplicativeTerm, { additive_op, MultiplicativeTerm }"
    )
    def parse_additive_term(self) -> Optional['Expression']:
        left = self.parse_multiplicative_term()

        while op := self.consume_match(self._additive_op):
            if not (right := self.parse_multiplicative_term()):
                raise SyntaxException("Missing term after operator",
                                      self._token.location.begin)

            left = BinaryOperation(
                left,
                right,
                EBinaryOperationType.from_token_kind(op.kind),
                Location(
                    left.location.begin,
                    right.location.end
                )
            )

        return left

    @ebnf(
        "MultiplicativeTerm",
        "UnaryTerm, { multiplicative_op, UnaryTerm }"
    )
    def parse_multiplicative_term(self) -> Optional['Expression']:
        left = self.parse_unary_term()

        while op := self.consume_match(self._multiplicative_op):
            if not (right := self.parse_unary_term()):
                raise SyntaxException("Missing term after operator",
                                      self._token.location.begin)

            left = BinaryOperation(
                left,
                right,
                EBinaryOperationType.from_token_kind(op.kind),
                Location(
                    left.location.begin,
                    right.location.end
                )
            )

        return left

    @ebnf(
        "UnaryTerm",
        "[ unary_op ], Term"
    )
    def parse_unary_term(self) -> Optional[Expression]:
        if op := self.consume_match(self._unary_op):
            value = self.parse_term()

            return UnaryOperation(
                value,
                EUnaryOperationType.from_token_kind(op.kind),
                Location(
                    op.location.begin,
                    value.location.end
                )
            )

        return self.parse_term()

    @ebnf(
        "Term",
        "literal | Access, ( [ 'is', Type ] | [ 'as', Type ] )"
        "| FnCall | NewStruct | '(', Expression, ')'"
    )
    @untested()
    def parse_term(self) -> Optional[Term]:
        if literal := self.consume_match(self._literal_kinds):
            return Constant(literal.value, literal.location)

        if access := self.parse_access():
            if self.consume_if(TokenKind.As):
                typ = self.parse_type()

                return Cast(access, typ)

            if self.consume_if(TokenKind.Is):
                typ = self.parse_type()

                return IsCompare(access, typ)

            return access

        # @TODO: FnCall

        # @TODO: NewStruct

        # @TODO: ( Expression )

        return None

    # endregion


if __name__ == "__main__":
    lexer = Lexer(StreamBuffer.from_str(
        # "fn main(x: i32, mut y: f32) { }"
        "struct Player { health: i32; }"
    ))
    parser = Parser(lexer)
    program = parser.parse()

    pprint(program)
