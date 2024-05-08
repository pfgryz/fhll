import typing
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
from src.parser.ast.expressions.expression import Expression
from src.parser.ast.expressions.term import Term
from src.parser.ast.expressions.unary_operation import UnaryOperation
from src.parser.ast.expressions.unary_operation_type import EUnaryOperationType
from src.parser.ast.declaration.field_declaration import FieldDeclaration
from src.parser.ast.declaration.function_declaration import FunctionDeclaration
from src.parser.ast.is_compare import IsCompare
from src.parser.ast.module import Module
from src.parser.ast.name import Name
from src.parser.ast.declaration.parameter import Parameter
from src.parser.ast.statements.assignment import Assignment
from src.parser.ast.statements.block import Block
from src.parser.ast.statements.variable_declaration import VariableDeclaration
from src.parser.ast.statements.fn_call import FnCall
from src.parser.ast.statements.if_statement import IfStatement
from src.parser.ast.statements.new_struct_statement import NewStruct
from src.parser.ast.statements.return_statement import ReturnStatement
from src.parser.ast.statements.statement import Statement
from src.parser.ast.statements.while_statement import WhileStatement
from src.parser.ast.declaration.struct_declaration import StructDeclaration
from src.parser.ast.variant_access import VariantAccess
from src.parser.ebnf import ebnf
from src.parser.errors import SyntaxExpectedTokenException, SyntaxException, \
    NameExpectedError, SemicolonExpectedError, ColonExpectedError, \
    BlockExpectedError, ParenthesisExpectedError, TypeExpectedError, \
    ParameterExpectedError, ExpressionExpectedError, LetKeywordExpectedError, \
    AssignExpectedError, BraceExpectedError, UnexpectedTokenError
from src.utils.buffer import StreamBuffer

type SyntaxExceptionType = Optional[typing.Type[SyntaxException]]


class Parser:
    # region Language Definition (builtin-types)

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

    # endregion

    # region Language Definition (operators)

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

    # endregion

    # region Dunder Methods

    def __init__(self, lexer: Lexer):
        self._lexer = lexer
        self._token = None
        self._last = None

    # endregion

    # region Helper Methods

    def check_if(self, kind: TokenKind) -> bool:
        if self._token is None:
            return False

        return self._token.kind == kind

    def consume(self) -> Token:
        token = self._token
        self._token = self._lexer.get_next_token()
        return token

    def consume_if(self, kind: TokenKind) -> Optional[Token]:
        if self.check_if(kind):
            return self.consume()

        return None

    def consume_match(self, kinds: list[TokenKind]) -> Optional[Token]:
        for kind in kinds:
            if token := self.consume_if(kind):
                return token

        return None

    def expect(
            self, kind: TokenKind,
            exception: SyntaxExceptionType = None
    ) -> Token:
        return self.expect_conditional(kind, True, exception)

    def expect_conditional(
            self, kind: TokenKind, condition: bool,
            exception: SyntaxExceptionType = None
    ) -> Optional[Token]:
        if token := self.consume_if(kind):
            return token

        if condition:
            if exception:
                raise exception(self._token.location.begin)
            raise SyntaxExpectedTokenException(
                kind, self._token.kind, self._token.location.begin
            )

        return None

    def expect_match(self, kinds: list[TokenKind]) -> Optional[Token]:
        if token := self.consume_match(kinds):
            return token

        raise SyntaxExpectedTokenException(
            kinds, self._token.kind, self._token.location.begin
        )

    # endregion

    # region Parse Program
    @ebnf(
        "Program",
        "{ FunctionDeclaration | StructDeclaration | EnumDeclaration }"
    )
    def parse(self) -> Module:
        function_declarations = []
        struct_declarations = []
        enum_declarations = []

        # Start consuming tokens
        if self._token is None:
            self.consume()

        while True:
            if function_declaration := self.parse_function_declaration():
                function_declarations.append(function_declaration)
            elif struct_declaration := self.parse_struct_declaration():
                struct_declarations.append(struct_declaration)
            elif enum_declaration := self.parse_enum_declaration():
                enum_declarations.append(enum_declaration)
            else:
                break

        if (token := self.consume()) and token.kind != TokenKind.EOF:
            raise UnexpectedTokenError(token.location.begin)

        return Module(
            function_declarations,
            struct_declarations,
            enum_declarations
        )

    # endregion

    # region Parse Functions

    @ebnf(
        "FunctionDeclaration",
        "'fn', identifier, '(', [ Parameters ], ')', [ '->', Type ], Block"
    )
    def parse_function_declaration(self) -> Optional[FunctionDeclaration]:
        if not (fn_kw := self.consume_if(TokenKind.Fn)):
            return None

        name = self.expect(TokenKind.Identifier, NameExpectedError)

        # Parameters
        self.expect(TokenKind.ParenthesisOpen, ParenthesisExpectedError)
        parameters = self.parse_parameters()
        close = self.expect(
            TokenKind.ParenthesisClose, ParenthesisExpectedError
        )
        end = close.location.end

        # Return Type
        returns = None
        if arrow := self.consume_if(TokenKind.Arrow):
            if not (returns := self.parse_type()):
                raise TypeExpectedError(arrow.location.end)
            end = returns.location.end

        if not (block := self.parse_block()):
            raise BlockExpectedError(end)

        return FunctionDeclaration(
            Name(name.value, name.location),
            parameters,
            returns,
            block,
            Location(
                fn_kw.location.begin,
                end
            )
        )

    @ebnf(
        "Parameters", "{ ',', Parameter }"
    )
    def parse_parameters(self) -> list[Parameter]:
        parameters = []

        if parameter := self.parse_parameter():
            parameters.append(parameter)

        while comma := self.consume_if(TokenKind.Comma):
            if parameter := self.parse_parameter():
                parameters.append(parameter)
            else:
                raise ParameterExpectedError(comma.location.end)

        return parameters

    @ebnf(
        "Parameter", "[ 'mut' ], identifier, ':', Type"
    )
    def parse_parameter(self) -> Optional[Parameter]:
        mut = self.consume_if(TokenKind.Mut)
        mutable = mut is not None

        if not (identifier := self.expect_conditional(
                TokenKind.Identifier, mutable, NameExpectedError
        )):
            return None

        self.expect(TokenKind.Colon, ColonExpectedError)

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

        colon = self.expect(TokenKind.Colon, ColonExpectedError)
        if not (declared_type := self.parse_type()):
            raise TypeExpectedError(colon.location.end)
        self.expect(TokenKind.Semicolon, SemicolonExpectedError)

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
        if not (enum_kw := self.consume_if(TokenKind.Enum)):
            return None

        identifier = self.consume_if(TokenKind.Identifier)

        self.expect(TokenKind.BraceOpen)

        variants = []
        while variant := self.parse_struct_declaration() \
                         or self.parse_enum_declaration():
            variants.append(variant)
            self.expect(TokenKind.Semicolon, SemicolonExpectedError)

        close = self.expect(TokenKind.BraceClose)

        return EnumDeclaration(
            Name(identifier.value, identifier.location),
            variants,
            Location(
                enum_kw.location.begin,
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
        if not (open_paren := self.consume_if(TokenKind.BraceOpen)):
            return None

        statements = self.parse_statements_list()

        close_paren = self.expect(TokenKind.BraceClose, BraceExpectedError)

        return Block(
            statements,
            Location(
                open_paren.location.begin,
                close_paren.location.end
            )
        )

    @ebnf(
        "StatementList",
        "{ Statement, ';'}"
    )
    def parse_statements_list(self) -> list[Statement]:
        statements = []

        while statement := self.parse_statement():
            statements.append(statement)
            self.expect(TokenKind.Semicolon, SemicolonExpectedError)

        return statements

    @ebnf(
        "Statement",
        "Declaration | Assignment | FnCall | Block"
        " | ReturnStatement | IfStatement | WhileStatement"
    )
    def parse_statement(self) -> Optional[Statement]:
        if declaration := self.parse_declaration():
            return declaration

        if block := self.parse_block():
            return block

        if return_statement := self.parse_return_statement():
            return return_statement

        if if_statement := self.parse_if_statement():
            return if_statement

        if while_statement := self.parse_while_statement():
            return while_statement

        if identifier := self.consume_if(TokenKind.Identifier):
            self._last = identifier
            if self.check_if(TokenKind.Comma) \
                    or self.check_if(TokenKind.Assign):
                assignment = self.parse_assignment()
                return assignment
            elif self.check_if(TokenKind.ParenthesisOpen):
                fn_call = self.parse_fn_call()
                return fn_call
            else:
                raise UnexpectedTokenError(identifier.location.begin)

        return None

    @ebnf(
        "Declaration",
        "[ 'mut' ], 'let', identifier, [ ':', Type ], [ '=', Expression ]"
    )
    def parse_declaration(self) -> Optional[VariableDeclaration]:
        mut = self.consume_if(TokenKind.Mut)

        if not (let := self.expect_conditional(
                TokenKind.Let, mut is not None, LetKeywordExpectedError
        )):
            return None

        begin = let.location.begin if mut is None else mut.location.begin

        identifier = self.expect(TokenKind.Identifier, NameExpectedError)
        name = Name(identifier.value, identifier.location)
        types = None
        expression = None
        end = name.location.end

        if colon := self.consume_if(TokenKind.Colon):
            if not (types := self.parse_type()):
                raise TypeExpectedError(colon.location.end)

            end = types.location.end

        if assign := self.consume_if(TokenKind.Assign):
            if not (expression := self.parse_expression()):
                raise ExpressionExpectedError(assign.location.end)

            end = expression.location.end

        return VariableDeclaration(
            name,
            mut is not None,
            types,
            expression,
            Location(
                begin,
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

        assign = self.expect(TokenKind.Assign, AssignExpectedError)

        expression = self.parse_expression()
        if expression is None:
            raise ExpressionExpectedError(assign.location.end)

        return Assignment(access, expression, Location(
            access.location.begin,
            expression.location.end
        ))

    @ebnf(
        "FnCall",
        "identifier, '(', [ FnArguments ], ')'"
    )
    def parse_fn_call(self) -> Optional[FnCall]:
        if self._last is not None:
            identifier = self._last
            self._last = identifier
        else:
            identifier = self.consume_if(TokenKind.Identifier)

        if not identifier:
            return None

        name = Name(identifier.value, identifier.location)

        self.expect(TokenKind.ParenthesisOpen, ParenthesisExpectedError)
        arguments = self.parse_fn_arguments()
        close = self.expect(
            TokenKind.ParenthesisClose, ParenthesisExpectedError
        )

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
    def parse_fn_arguments(self) -> list[Expression]:
        arguments = []

        if not (expression := self.parse_expression()):
            return arguments

        arguments.append(expression)

        while comma := self.consume_if(TokenKind.Comma):
            if not (expression := self.parse_expression()):
                raise ExpressionExpectedError(comma.location.end)

            arguments.append(expression)

        return arguments

    @ebnf(
        "NewStruct",
        "VariantAccess, '{', { Assignment, ';' }, '}'"
    )
    def parse_new_struct(self) -> Optional[NewStruct]:
        if not (variant_access := self.parse_variant_access()):
            return None

        self.expect(TokenKind.BraceOpen, BraceExpectedError)

        assignments = []

        while assignment_statement := self.parse_assignment():
            assignments.append(assignment_statement)
            self.expect(TokenKind.Semicolon, SemicolonExpectedError)

        close = self.expect(TokenKind.BraceClose, BraceExpectedError)

        return NewStruct(
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
    def parse_return_statement(self) -> Optional[ReturnStatement]:
        if not (return_kw := self.consume_if(TokenKind.Return)):
            return None

        value = None
        if expression := self.parse_expression():
            value = expression

        return ReturnStatement(
            value,
            Location(
                return_kw.location.begin,
                return_kw.location.end if value is None else value.location.end
            )
        )

    @ebnf(
        "IfStatement",
        "'if', '(', Expression, ')', Block, [ 'else', Block ]"
    )
    def parse_if_statement(self) -> Optional[IfStatement]:
        if not (if_kw := self.consume_if(TokenKind.If)):
            return None

        open_paren = self.expect(
            TokenKind.ParenthesisOpen, ParenthesisExpectedError
        )

        if not (condition := self.parse_expression()):
            raise ExpressionExpectedError(open_paren.location.end)

        close_paren = self.expect(
            TokenKind.ParenthesisClose, ParenthesisExpectedError
        )

        else_block = None
        if not (block := self.parse_block()):
            raise BlockExpectedError(close_paren.location.end)
        end = block.location.end

        if else_kw := self.consume_if(TokenKind.Else):
            if not (else_block := self.parse_block()):
                raise BlockExpectedError(else_kw.location.end)

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

        open_paren = self.expect(
            TokenKind.ParenthesisOpen, ParenthesisExpectedError
        )

        if not (condition := self.parse_expression()):
            raise ExpressionExpectedError(open_paren.location.end)

        close = self.expect(TokenKind.ParenthesisClose,
                            ParenthesisExpectedError)

        if not (block := self.parse_block()):
            raise BlockExpectedError(close.location.end)

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
        if self._last is not None:
            element = self._last
            self._last = None
        else:
            element = self.consume_if(TokenKind.Identifier)

        if not element:
            return None

        access = Name(element.value, element.location)

        while self.consume_if(TokenKind.Period):
            element = self.expect(TokenKind.Identifier, NameExpectedError)

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
        if self._last is not None:
            element = self._last
            self._last = None
        else:
            element = self.consume_if(TokenKind.Identifier)

        if not element:
            return None

        result = Name(element.value, element.location)

        while self.consume_if(TokenKind.DoubleColon):
            element = self.expect(TokenKind.Identifier, NameExpectedError)

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
    def parse_expression(self) -> Optional[Expression]:
        left = self.parse_and_expression()

        while op := self.consume_if(self._or_op):
            if not (right := self.parse_and_expression()):
                raise ExpressionExpectedError(op.location.end)

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
    def parse_and_expression(self) -> Optional[Expression]:
        left = self.parse_relation_expression()

        while op := self.consume_if(self._and_op):
            if not (right := self.parse_relation_expression()):
                raise ExpressionExpectedError(op.location.end)

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
    def parse_relation_expression(self) -> Optional[Expression]:
        left = self.parse_additive_term()

        if op := self.consume_match(self._relation_op):
            if not (right := self.parse_additive_term()):
                raise ExpressionExpectedError(op.location.end)

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
    def parse_additive_term(self) -> Optional[Expression]:
        left = self.parse_multiplicative_term()

        while op := self.consume_match(self._additive_op):
            if not (right := self.parse_multiplicative_term()):
                raise ExpressionExpectedError(op.location.end)

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
    def parse_multiplicative_term(self) -> Optional[Expression]:
        left = self.parse_unary_term()

        while op := self.consume_match(self._multiplicative_op):
            if not (right := self.parse_unary_term()):
                raise ExpressionExpectedError(op.location.end)

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
            if not (term := self.parse_term()):
                raise ExpressionExpectedError(op.location.end)

            return UnaryOperation(
                term,
                EUnaryOperationType.from_token_kind(op.kind),
                Location(
                    op.location.begin,
                    term.location.end
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

        if open_paren := self.consume_if(TokenKind.ParenthesisOpen):
            if not (expression := self.parse_expression()):
                raise ExpressionExpectedError(open_paren.location.end)

            self.expect(TokenKind.ParenthesisClose, ParenthesisExpectedError)

            return expression

        """
                Conflict of first symbol for constructions:
                    Access := identifier, { '.', identifier };
                    FnCall := identifier, '(', [ FnArguments ], ')';
                    NewStruct := VariantAccess, '{', { Assignment, ';' }, '}'
                    VariantAccess := identifier, { '::', identifier };

                Solution:
                    - identifier in NewStruct is followed by ':' or '{'
                    - identifier in FnCall is followed by '('
                    - identifier in Access can be single or followed by '.'
                """
        if identifier := self.consume_if(TokenKind.Identifier):
            self._last = identifier

            if self.check_if(TokenKind.DoubleColon) \
                    or self.check_if(TokenKind.BraceOpen):
                return self.parse_new_struct()
            elif self.check_if(TokenKind.ParenthesisOpen):
                return self.parse_fn_call()
            else:
                access = self.parse_access()

                if as_kw := self.consume_if(TokenKind.As):
                    if not (to_type := self.parse_type()):
                        raise TypeExpectedError(as_kw.location.end)

                    return Cast(
                        access, to_type,
                        Location(access.location.begin, to_type.location.end)
                    )

                if is_kw := self.consume_if(TokenKind.Is):
                    if not (to_type := self.parse_type()):
                        raise TypeExpectedError(is_kw.location.end)

                    return IsCompare(
                        access, to_type,
                        Location(access.location.begin, to_type.location.end)
                    )

                return access

        return None

    # endregion


if __name__ == "__main__":
    lexer = Lexer(StreamBuffer.from_str(
        # "fn main(x: i32, mut y: f32) { }"
        "struct Player { health: i32; }"
    ))
    parser = Parser(lexer)
    try:
        program = parser.parse()
    except:
        print(parser._token, parser._lexer._stream.position)

    pprint(program)
