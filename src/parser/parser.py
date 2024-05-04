from pprint import pprint
from typing import Optional

from src.common.location import Location
from src.lexer.lexer import Lexer
from src.lexer.token import Token
from src.lexer.token_kind import TokenKind
from src.parser.ast.access import Access
from src.parser.ast.cast import Cast
from src.parser.ast.common import Type
from src.parser.ast.constant import Constant
from src.parser.ast.declaration.enum_declaration import EnumDeclaration
from src.parser.ast.expressions.binary_operation import BinaryOperation
from src.parser.ast.expressions.binary_operation_type import \
    EBinaryOperationType
from src.parser.ast.expressions.bool_operation import BoolOperation
from src.parser.ast.expressions.bool_operation_type import EBoolOperationType
from src.parser.ast.expressions.compare import Compare
from src.parser.ast.expressions.compare_type import ECompareType
from src.parser.ast.expressions.term import Term
from src.parser.ast.expressions.unary_operation import UnaryOperation
from src.parser.ast.expressions.unary_operation_type import EUnaryOperationType
from src.parser.ast.declaration.field_declaration import FieldDeclaration
from src.parser.ast.declaration.function_declaration import FunctionDeclaration
from src.parser.ast.is_compare import IsCompare
from src.parser.ast.name import Name
from src.parser.ast.declaration.parameter import Parameter
from src.parser.ast.statements.assignment import Assignment
from src.parser.ast.statements.block import Block
from src.parser.ast.statements.declaration import Declaration
from src.parser.ast.statements.fn_call import FnCall
from src.parser.ast.statements.if_statement import IfStatement
from src.parser.ast.statements.new_struct_statement import NewStructStatement
from src.parser.ast.statements.return_statement import ReturnStatement
from src.parser.ast.statements.while_statement import WhileStatement
from src.parser.ast.declaration.struct_declaration import StructDeclaration
from src.parser.ast.variant_access import VariantAccess
from src.parser.ebnf import ebnf
from src.parser.errors import SyntaxExpectedTokenException, SyntaxException
from src.utils.buffer import StreamBuffer

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
    def parse(self) -> 'Program':
        body = []

        while True:
            if function_declaration := self.parse_function_declaration():
                body.append(function_declaration)
            elif struct_declaration := self.parse_struct_declaration():
                body.append(struct_declaration)
            elif enum_declaration := self.parse_enum_declaration():
                body.append(enum_declaration)
            else:
                break

        # Check if EOF
        # @TODO

        return body

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
    def parse_parameters(self) -> list[Parameter]:
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
        declared_type = self.parse_type()
        self.expect(TokenKind.Semicolon)

        return FieldDeclaration(
            Name(identifier.value, identifier.location),
            declared_type,
            Location(identifier.location.begin, declared_type.location.end)
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
    def parse_block(self) -> Optional['Block']:
        if not (open := self.consume_if(TokenKind.BraceOpen)):
            return None

        statements = self.parse_statements_list()

        close = self.expect(TokenKind.BraceClose)

        return Block(
            statements,
            Location(
                open.location.begin,
                close.location.end
            )
        )

    @ebnf(
        "StatementList",
        "{ Statement, ';'}"
    )
    def parse_statements_list(self) -> list['Statement']:
        statements = []

        while statement := self.parse_statement():
            statements.append(statement)
            self.expect(TokenKind.Semicolon)

        return statements

    @ebnf(
        "Statement",
        "Declaration | Assignment | FnCall | NewStruct "
        "| Block | ReturnStatement | IfStatement | WhileStatement"
    )
    def parse_statement(self) -> Optional['Statement']:
        if declaration := self.parse_declaration():
            return declaration

        if assignment := self.parse_assignment():
            return assignment

        if fn_call := self.parse_fn_call():
            return fn_call

        if new_struct := self.parse_new_struct():
            return new_struct

        if block := self.parse_block():
            return block

        if return_statement := self.parse_return_statement():
            return return_statement

        if if_statement := self.parse_if_statement():
            return if_statement

        if while_statement := self.parse_while_statement():
            return while_statement

        return None

    @ebnf(
        "Declaration",
        "[ 'mut' ], 'let', identifier, [ ':', Type ], [ '=', Expression ]"
    )
    def parse_declaration(self) -> Optional['Declaration']:
        mut = self.consume_if(TokenKind.Mut)

        if not (self.expect_conditional(TokenKind.Let, mut is not None)):
            return None

        identifier = self.expect(TokenKind.Identifier)
        name = Name(identifier.value, identifier.location)
        types = None
        expression = None
        end = name.location.end

        if colon := self.consume_if(TokenKind.Colon):
            if not (types := self.parse_type()):
                raise SyntaxException("Required type after ':'",
                                      colon.location.begin)

            end = types.location.end

        if assign := self.consume_if(TokenKind.Assign):
            if not (expression := self.parse_expression()):
                raise SyntaxException("Required expression after '='",
                                      assign.location.begin)

            end = expression.location.end

        return Declaration(
            name,
            mut is not None,
            types,
            expression,
            Location(
                name.location.begin,
                end
            )
        )

    @ebnf(
        "Assignment",
        "Access, '=', Expression"
    )
    def parse_assignment(self) -> Optional[Assignment]:
        if not (access := self.parse_access()):
            return None

        assign = self.expect(TokenKind.Assign)

        expression = self.parse_expression()
        if expression is None:
            raise SyntaxException("Required expression after assignment",
                                  assign.location.begin)

        return Assignment(access, expression, Location(
            access.location.begin,
            expression.location.end
        ))

    @ebnf(
        "FnCall",
        "identifier, '(', [ FnArguments ], ')'"
    )
    def parse_fn_call(self) -> Optional['FnCall']:
        if not (identifier := self.consume_if(TokenKind.Identifier)):
            return None

        name = Name(identifier.value, identifier.location)

        self.expect(TokenKind.ParenthesisOpen)
        arguments = self.parse_fn_arguments()
        close = self.expect(TokenKind.ParenthesisClose)

        return FnCall(
            name,
            arguments,
            Location(
                name.location.begin,
                close.location.end
            )
        )

    @ebnf(
        "FnArguments",
        "Expression, {, ',', Expression }"
    )
    def parse_fn_arguments(self) -> list['Expression']:
        arguments = []

        if not (expression := self.parse_expression()):
            return arguments

        arguments.append(expression)

        while comma := self.consume_if(TokenKind.Comma):
            if not (expression := self.parse_expression()):
                raise SyntaxException("Missing expression after comma",
                                      comma.location.begin)

            arguments.append(expression)

        return arguments

    @ebnf(
        "NewStruct",
        "VariantAccess, '{', [ Assignment, ';' ], '}'"
    )
    def parse_new_struct(self) -> Optional[NewStructStatement]:
        if not (variant_access := self.parse_variant_access()):
            return None

        self.expect(TokenKind.BraceOpen)

        assignments = []

        while assignment_statement := self.parse_assignment():
            assignments.append(assignment_statement)
            self.expect(TokenKind.Semicolon)

        close = self.expect(TokenKind.BraceClose)

        return NewStructStatement(
            variant_access,
            assignments,
            Location(
                variant_access.location.begin,
                close.location.end
            )
        )

    @ebnf(
        "ReturnStatement",
        "'return', [ Expression ]"
    )
    def parse_return_statement(self) -> Optional['ReturnStatement']:
        if not (return_kw := self.consume_if(TokenKind.Return)):
            return None

        value = None
        if exp := self.parse_expression():
            value = exp

        return ReturnStatement(
            value,
            Location(return_kw.location.begin, return_kw.location.end)
        )

    @ebnf(
        "IfStatement",
        "'if', '(', Expression, ')', Block, [ 'else', Block ]"
    )
    def parse_if_statement(self) -> Optional['IfStatement']:
        if not (if_kw := self.consume_if(TokenKind.If)):
            return None

        self.expect(TokenKind.ParenthesisOpen)

        if not (condition := self.parse_expression()):
            raise SyntaxException("Missing condifition for if",
                                  if_kw.location.begin)

        close = self.expect(TokenKind.ParenthesisClose)

        else_block = None
        if not (block := self.parse_block()):
            raise SyntaxException("Missing block for if",
                                  close.location.begin)
        end = block.location.end

        if else_kw := self.consume_if(TokenKind.Else):
            if not (else_block := self.parse_block()):
                raise SyntaxException("Missing block after else",
                                      else_kw.location.begin)

            end = else_block.location.end

        return IfStatement(
            condition,
            block,
            else_block,
            Location(
                if_kw.location.begin,
                end
            )
        )

    @ebnf(
        "WhileStatement",
        "'while', '(', Expression, ')', Block"
    )
    def parse_while_statement(self) -> Optional['WhileStatement']:
        if not (while_kw := self.consume_if(TokenKind.While)):
            return None

        self.expect(TokenKind.ParenthesisOpen)
        if not (condition := self.parse_expression()):
            raise SyntaxException("Missing condifition for while",
                                  while_kw.location.begin)

        close = self.expect(TokenKind.ParenthesisClose)

        if not (block := self.parse_block()):
            raise SyntaxException("Missing block for while",
                                  close.location.begin)

        return WhileStatement(
            condition,
            block,
            Location(
                while_kw.location.begin,
                block.location.end
            )
        )

    # endregion

    # region Parse Access

    @ebnf(
        "Access",
        "identifier, { '.', identifier }"
    )
    def parse_access(self) -> Optional[Name | Access]:
        if not (element := self.consume_if(TokenKind.Identifier)):
            return None

        access = Name(element.value, element.location)

        while self.consume_if(TokenKind.Period):
            element = self.expect(TokenKind.Identifier)

            access = Access(
                Name(element.value, element.location),
                access,
                Location(access.location.begin, element.location.end)
            )

        return access

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
                result,
                Location(result.location.begin, element.location.end)
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
                ECompareType.from_token_kind(op.kind),
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
    def parse_term(self) -> Optional[Term]:
        if literal := self.consume_match(self._literal_kinds):
            return Constant(literal.value, literal.location)

        if access := self.parse_access():
            if self.consume_if(TokenKind.As):
                to_type = self.parse_type()

                return Cast(access, to_type, Location(access.location.begin,
                                                      to_type.location.end))

            if self.consume_if(TokenKind.Is):
                to_type = self.parse_type()

                return IsCompare(access, to_type,
                                 Location(access.location.begin,
                                          to_type.location.end))

            return access

        if fn_call := self.parse_fn_call():
            return fn_call

        if new_struct := self.parse_new_struct():
            return new_struct

        if self.consume_if(TokenKind.ParenthesisOpen):
            if not (expression := self.parse_expression()):
                raise SyntaxException("Missing expression",
                                      self._token.location.begin)

            self.expect(TokenKind.ParenthesisClose)

            return expression

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
